# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install yt-dlp and ffmpeg
RUN apt-get update && apt-get install -y ffmpeg \
    && pip install --no-cache-dir yt-dlp

# Run the Python script when the container launches
CMD ["python", "./download.py"]
