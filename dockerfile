# Use the official Python base image with the latest tag
FROM python:3.13-slim

# Install sudo for apt-get access
RUN apt-get update && apt-get install -y \
    sudo \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the working directory
COPY src/ImageGenerator_html.py /app/src/ImageGenerator_html.py

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "src.ImageGenerator_html:app", "--host", "0.0.0.0", "--port", "8000"]

