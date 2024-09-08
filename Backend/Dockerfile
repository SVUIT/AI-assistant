# Sử dụng Python slim làm base image
FROM python:3.9-slim

# Cài đặt các công cụ cần thiết cho Docker
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Thêm khóa GPG cho Docker
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/keyrings/docker.asc

# Thêm Docker repository
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Cài đặt Docker CLI
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements vào container
COPY requirements.txt /app

# Cài đặt các gói Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . /app

# Mở cổng 5000
EXPOSE 5000

# Chạy ứng dụng bằng Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "eventlet", "--workers", "1", "app:app"]
