import re
import os
import clip
import open_clip
import torch
import json
import glob
import faiss
import numpy as np
from gg_trans import Translation


class MyFaiss:
    def __init__(self, bin_clipv2_file: str, json_path: str):
#         self.index_clip = self.load_bin_file(bin_clip_file)
        self.index_clipv2 = self.load_bin_file(bin_clipv2_file)

        self.id2img_fps = self.load_json_file(json_path)

        self.translater = Translation()
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model, _ = clip.load("ViT-B/16", device=self.__device)
        self.clipv2_model, _, _ = open_clip.create_model_and_transforms('ViT-L-14', device=self.__device, pretrained='datacomp_xl_s13b_b90k')
        self.clipv2_tokenizer = open_clip.get_tokenizer('ViT-L-14')

    def load_json_file(self, json_path: str):
        with open(json_path, 'r') as f:
            js = json.load(f)
        return {int(k):v for k,v in js.items()}

    def load_bin_file(self, bin_file: str):
        return faiss.read_index(bin_file)

    def text_search(self, text, index, k, model_type):
        text = self.translater(text)

        ###### TEXT FEATURES EXTRACTING ######
        if model_type == 'clip':
            text = clip.tokenize([text]).to(self.__device)
            text_features = self.clip_model.encode_text(text)
        else:
            text = self.clipv2_tokenizer([text]).to(self.__device)
            text_features = self.clipv2_model.encode_text(text)

        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_features = text_features.cpu().detach().numpy().astype(np.float32)

        ###### SEARCHING #####
        if model_type == 'clip':
#             index_choosed = self.index_clip
            pass
        else:
            index_choosed = self.index_clipv2

        if index is None:
            scores, idx_image = index_choosed.search(text_features, k=k)

        else:
            id_selector = faiss.IDSelectorArray(index)
            scores, idx_image = index_choosed.search(text_features, k=k,
                                                   params=faiss.SearchParametersIVF(sel=id_selector))
        idx_image = idx_image.flatten()
        # Rerank the images based on text similarity
        ranked_indices, rerank_scores = self.rerank_images(torch.tensor(text_features, device=self.__device), idx_image)

        # Get the corresponding image paths after reranking
        ranked_image_paths = [self.id2img_fps[idx_image[i]]['image_path'] for i in ranked_indices]

        ###### GET INFOS KEYFRAMES_ID ######
        infos_query = list(map(self.id2img_fps.get, list(idx_image)))
        image_paths = [info['image_path'] for info in infos_query]
        return scores.flatten(), idx_image, infos_query, image_paths, ranked_image_paths

    def rerank_images(self, text_features, idx_image):
        """
        Rerank images based on similarity to the provided text features.

        Parameters:
        - text_features: The encoded features of the text query.
        - idx_image: The indices of images retrieved from the initial search.

        Returns:
        - ranked_indices: A list of indices ranked by similarity to the text query.
        - similarity_scores: The similarity scores for the ranked frames.
        """
        # Reconstruct the image features from the FAISS index using idx_image
        image_features = np.vstack([self.index_clipv2.reconstruct(int(idx)) for idx in idx_image])
        image_features = torch.tensor(image_features, device=self.__device)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        similarity_scores = (image_features @ text_features.T).squeeze(1)
        ranked_indices = similarity_scores.argsort(descending=True).cpu().numpy()

        return ranked_indices, similarity_scores.cpu().numpy()

    def reranking(self, prev_result, lst_pos_vote_idxs, lst_neg_vote_idxs, k):
        '''
        Perform reranking using user feedback

        Parameters:
         - prev_result: (idx, score)
         - lst_pos_vote_idxs: id of positive sample
         - lst_neg_vote_idxs: id of negative sample

        Return:

        '''
        lst_vote_idxs = []
        lst_vote_idxs.extend(lst_pos_vote_idxs)
        lst_vote_idxs.extend(lst_neg_vote_idxs)
        lst_vote_idxs = np.array(lst_vote_idxs).astype('int64')
        len_pos = len(lst_pos_vote_idxs)

        result = dict()
        for id, score in prev_result:
            result[id] = score

        for key in lst_neg_vote_idxs:
            result.pop(key)

        id_selector = faiss.IDSelectorArray(np.array(list(result.keys())).astype('int64'))
        query_feats = self.index_clipv2.reconstruct_batch(lst_vote_idxs)
        lst_scores, lst_idx_images = self.index_clipv2.search(query_feats, k=min(k, len(result)),
                                                            params=faiss.SearchParametersIVF(sel=id_selector))

        for i, (scores, idx_images) in enumerate(zip(lst_scores, lst_idx_images)):
            for score, idx_image in zip(scores, idx_images):
                if 0 <= i < len_pos:
                    result[idx_image] += score
                else:
                    result[idx_image] -= score

        result = sorted(result.items(), key=lambda x:x[1], reverse=True)
        list_ids = [item[0] for item in result]
        lst_scores = [item[1] for item in result]
        infos_query = list(map(self.id2img_fps.get, list(list_ids)))
        list_image_paths = [info['image_path'] for info in infos_query]

        return lst_scores, list_ids, infos_query, list_image_paths