#!/bin/bash

# Kiểm tra nếu người dùng không nhập đủ tham số
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Cách dùng: $0 <URL_VIDEO> <NGÀY_ĐĂNG (ddmmyyyy)>"
    exit 1
fi

# Lấy URL và ngày đăng từ tham số đầu vào
url="$1"
upload_date="$2"

python download_video.py "$url" 

kaggle datasets version -p ./videos/ -m "$upload_date"

# Xóa các file video, giữ lại metadata
echo "Xóa video đã upload..."
find ./videos -type f ! -name 'dataset-metadata.json' -delete

# bash download_video.sh "https://www.youtube.com/watch?v=-9DDpOaMlbU" 11022025  # Ví dụ cách dùng
