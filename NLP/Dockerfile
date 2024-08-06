# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install system dependencies including gcc, g++, build-essential, and pkg-config
RUN apt-get update && \
    apt-get install -y gcc g++ build-essential pkg-config

# Set up a working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

# Run app.py when the container launches
CMD ["python", "app.py", "--port=5005"]
