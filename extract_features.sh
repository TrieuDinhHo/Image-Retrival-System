kaggle kernels push -p ./extract_features_from_keyframe

kernel_name="hodinhtrieu/extract-the-features"

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

    sleep 10
done

kaggle kernels output hodinhtrieu/extract-the-features -p ./extract_features_from_keyframe/result/
