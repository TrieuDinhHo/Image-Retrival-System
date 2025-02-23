import zipfile
import os
import gradio as gr
import csv
import json
import speech_recognition as sr  # Add speech recognition library
from my_faiss import MyFaiss

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

result_num = 20
bin_file_v2 = './aic/faiss_clipv2_cosine.bin'
json_path = './aic/image_paths.json'
cosine_faiss = MyFaiss(
    bin_clipv2_file=bin_file_v2,
    json_path=json_path
)

def retrieve_images(query):
    scores, idx_image, infos_query, image_paths, ranked_image_paths = cosine_faiss.text_search(query, k=result_num, model_type='clipv2', index=None)
    file_names = [file_path.split("/")[-3] + "_" + file_path.split("/")[-2] + "_" + file_path.split("/")[-1][:-4] for file_path in image_paths]
    images_with_labels = [(image_path, file_name) for image_path, file_name in zip(image_paths, file_names)]
    return images_with_labels, file_names

def toggle_selected_index(evt: gr.SelectData, selected_indices, selection_mode):
    index = evt.index
    if selection_mode == "single":
        selected_indices = [index]
    else:
        if index in selected_indices:
            selected_indices.remove(index)
        else:
            selected_indices.append(index)
    return selected_indices

def toggle_selection_mode(current_mode):
    if current_mode == "single":
        return "multiple", "Switch to Single Select Mode"
    else:
        return "single", "Switch to Multiple Select Mode"

# Function to get the selected index and print the corresponding file name
def get_select_index(evt: gr.SelectData, file_names, selected_indices, selection_mode):
    index = evt.index
    if selection_mode == "single":
        selected_indices = [file_names[index]]
        dir_component = file_names[index].split("_")
        file_path = f'./aic/media-info/{dir_component[0]}_{dir_component[1]}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        watch_url = data.get('watch_url')
    else:
        if file_names[index] in selected_indices:
            selected_indices.remove(file_names[index])
        else:
            selected_indices.append(file_names[index])
        watch_url = ""  # No specific URL for multiple selections

    return selected_indices, watch_url

# Function to export selected images to CSV
def export_to_csv(selected_indices):
    file_path = "selected_images.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["Image Prefix", "Image Suffix"])  # CSV header

        for name in selected_indices:
            parts = name.split("_")
            prefix = parts[0] + "_" + parts[1]  # e.g., "L09_V027"
            suffix = parts[2]  # e.g., "11676"
            writer.writerow([prefix, suffix])

    return file_path  # Return the path to the CSV file

# Function to transcribe audio
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results; check your network connection."

# Gradio interface
with gr.Blocks(fill_width=True, fill_height=True) as demo:
    file_names = gr.State()  # Store file names as a state
    selected_indices = gr.State([])  # State to store the indices of selected images
    selection_mode = gr.State("multiple")

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            query_input = gr.Textbox(label="Enter your query")
            audio_input = gr.Audio(type="filepath", label="Or speak your query")  # Add audio input
            transcribe_button = gr.Button("Convert Speech to Text")
            submit_button = gr.Button("Search")
            link_ytb = gr.Textbox(show_label=True, label="Link Youtube")
            video_output = gr.HTML(label="Click the button to watch the video")
            selected = gr.Textbox(label="Selected Images", placeholder="Selected image names will appear here")  # Changed to Textbox
            mode_button = gr.Button("Switch to Single Select Mode")  # Button to switch modes
            export_button = gr.Button("Export Selected to CSV")  # Button to export to CSV
            download_link = gr.File(label="Download CSV")  # File component for downloading the CSV
        with gr.Column(scale=10, min_width=100):
            image_gallery = gr.Gallery(
                allow_preview=False,
                label="Retrieved Images",
                show_label=False,
                elem_id="gallery",
                columns=[7],
                rows=[200],
                object_fit="cover",
                height="900px",
            )

    submit_button.click(retrieve_images, inputs=query_input, outputs=[image_gallery, file_names])
    image_gallery.select(get_select_index, inputs=[file_names, selected_indices, selection_mode], outputs=[selected, link_ytb])
    mode_button.click(toggle_selection_mode, selection_mode, [selection_mode, mode_button])

    # Trigger the export_to_csv function when the export_button is clicked and update the download link
    export_button.click(export_to_csv, inputs=selected_indices, outputs=download_link)

    # Add transcription functionality for audio input
    transcribe_button.click(transcribe_audio, inputs=audio_input, outputs=query_input)

demo.launch(server_name="0.0.0.0")