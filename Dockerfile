# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update --fix-missing && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libmariadb-dev \
    pkg-config \
    && apt-get clean

# Copy the current directory contents into the container at /src
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements-docker.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=src.app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]
