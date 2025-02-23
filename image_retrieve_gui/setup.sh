#!/bin/bash

# Install required Python packages
pip install -q gradio==4.44.0 
pip install -q git+https://github.com/openai/CLIP.git
pip install -q pyvi ftfy tqdm flask regex numpy pandas faiss-cpu clip rapidfuzz matplotlib flask-cors opencv-python langdetect==1.0.9 googletrans==3.1.0a0 sentence_transformers transformers scikit-learn open_clip_torch
pip install -q kaggle
pip install -q SpeechRecognition

# Download datasets from Kaggle
kaggle datasets download -d hodinhtrieu/metadata-aic
kaggle datasets download -d hodinhtrieu/bin-file-batch1
kaggle datasets download -d hodinhtrieu/image-paths
kaggle datasets download -d hodinhtrieu/keyframes-aic

# Create required directory
mkdir -p ./aic/

# Unzip files and delete them after extraction
python3 - <<EOF
import zipfile
import os

zip_files = [
    './bin-file-batch1.zip',
    './keyframes-aic.zip',
    './metadata-aic.zip',
    './image-paths.zip'
]

unzip_dir = './aic/'

for zip_file_path in zip_files:
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
        print(f'Unzipped {zip_file_path} to {unzip_dir}')
        os.remove(zip_file_path)
        print(f'Deleted {zip_file_path}')
    except FileNotFoundError:
        print(f"File not found: {zip_file_path}")
    except zipfile.BadZipFile:
        print(f"Corrupted zip file: {zip_file_path}")
EOF

echo "Setup completed successfully."
