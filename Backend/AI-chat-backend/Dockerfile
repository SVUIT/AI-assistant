# Stage 1: Build stage using a slim Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /data

# Copy the requirements file and install the required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "response.py"]
