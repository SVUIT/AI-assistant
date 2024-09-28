# Use the official Python image as a base image
FROM python:3.9.17-bookworm

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=True

# Set environment variable for the port
ENV PORT=5000

# Set the working directory in the container
WORKDIR /Backend

# Copy the current directory contents into the container at /app
COPY . /Backend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Docker CLI and Docker Compose V2
RUN apt-get update \
    && apt-get install -y \
       ca-certificates \
       curl \
       gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" | tee /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "eventlet", "--workers", "1", "app:app"]