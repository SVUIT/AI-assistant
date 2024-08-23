# Use the official Python image as a base image
FROM python:3.9.17-bookworm AS build-env

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=True

# Set environment variable for the port
ENV PORT=5000

# Set the working directory in the container
WORKDIR /app

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

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
&& pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Use the official Python image as a base image
FROM python:alpine3.20

WORKDIR /app

COPY --from=build-env /app /app

RUN pip install --no-cache-dir -r /app/requirements.txt
# Make port 5000 available to the world outside this container

EXPOSE 5000

# Run the application by gunicorn because it serve for production environment
# If you want to run the application in development enviroment, you can use the cmd ["python3", "filename.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
