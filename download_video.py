from pytubefix import YouTube
from pytubefix.cli import on_progress
import sys

# Kiểm tra nếu không có tham số URL được truyền vào
if len(sys.argv) < 2:
    print("Cách dùng: python script.py <URL_VIDEO>")
    sys.exit(1)

# Lấy URL từ tham số dòng lệnh
url = sys.argv[1]

# Tải video
yt = YouTube(url, on_progress_callback=on_progress)
print(f"Tiêu đề video: {yt.title}")

# Tải video với độ phân giải cao nhất
ys = yt.streams.get_highest_resolution()
ys.download(output_path="./videos")

print(f"Video đã được tải xuống và lưu tại: ./videos")