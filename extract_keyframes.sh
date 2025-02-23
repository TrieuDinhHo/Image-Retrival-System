#!/bin/bash

# Push kernel lên Kaggle
echo "Đang push kernel lên Kaggle..."
kaggle_output=$(kaggle kernels push -p ./extract_keyframes_from_video 2>&1)
if [ $? -ne 0 ]; then
    echo "Lỗi khi push kernel: $kaggle_output"
    exit 1
fi
echo "$kaggle_output"

# Định nghĩa kernel name
kernel_name="hodinhtrieu/extract-the-keyframes"

# Vòng lặp kiểm tra trạng thái
while true; do
    # Lấy trạng thái kernel
    status=$(kaggle kernels status "$kernel_name" 2>&1)
    if [ $? -ne 0 ]; then
        echo "Lỗi khi kiểm tra trạng thái: $status"
        exit 1
    fi
    echo "$status"

    # Kiểm tra nếu kernel hoàn thành
    if echo "$status" | grep -q 'has status "complete"'; then
        echo "Kernel đã hoàn thành."
        break
    fi

    # Kiểm tra nếu kernel gặp lỗi
    if echo "$status" | grep -q 'has status "error"'; then
        echo "Kernel gặp lỗi."
        exit 1
    fi

    # Đợi 10 giây trước khi kiểm tra lại
    sleep 10
done

kaggle kernels output hodinhtrieu/extract-the-keyframes -p ./extract_keyframes_from_video/result/