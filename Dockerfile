FROM n8nio/n8n

WORKDIR /app

# Copy toàn bộ file từ thư mục hiện tại vào container
COPY . /app
COPY kaggle.json /home/node/.config/kaggle/kaggle.json

USER root

# Cài đặt các phụ thuộc
RUN apk add --update bash python3 py3-pip nano

# Tạo virtual environment
RUN python3 -m venv /venv

# Cài đặt các thư viện Python
RUN . /venv/bin/activate && pip install --no-cache-dir -r requirements.txt
RUN . /venv/bin/activate && pip install --upgrade pip

# Cấp quyền cho toàn bộ file và thư mục trong /app
RUN chown -R node:node /app && \
    chmod -R 755 /app

# Tạo thư mục cấu hình Kaggle và copy file kaggle.json
RUN mkdir -p /home/node/.config/kaggle && \
    chown -R node:node /home/node/.config

RUN chmod 600 /home/node/.config/kaggle/kaggle.json

# Thiết lập PATH và chuyển về user node
ENV PATH="/venv/bin:$PATH"
USER node

# docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
# docker run -it --rm --name my_n8n -p 5678:5678 -e GENERIC_TIMEZONE="Asia/Ho_Chi_Minh" -e TZ="Asia/Ho_Chi_Minh" -v C:/Users/Trieu/OneDrive/Documents/n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n