# Use the official Python base image with the latest tag
FROM python:3.10-slim

# Install sudo for apt-get access
# RUN apt-get update && apt-get install -y \
#     sudo \
#     wkhtmltopdf \
#     && rm -rf /var/lib/apt/lists/*

# # Install dependencies
# RUN apt-get update && \
#     apt-get install -y sudo wget && \
#     wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.focal_amd64.deb && \
#     apt install -y ./wkhtmltox_0.12.5-1.focal_amd64.deb && \
#     rm -rf /var/lib/apt/lists/* wkhtmltox_0.12.5-1.focal_amd64.deb



    # Remove any previous wkhtmltopdf install lines, and use:
RUN apt-get update && \
    apt-get install -y wget xfonts-75dpi && \
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox-0.12.6-1.amd64.tar.xz && \
    tar -xJf wkhtmltox-0.12.6-1.amd64.tar.xz && \
    cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/ && \
    cp wkhtmltox/bin/wkhtmltoimage /usr/local/bin/ && \
    chmod +x /usr/local/bin/wkhtmltopdf /usr/local/bin/wkhtmltoimage && \
    rm -rf wkhtmltox*
# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the working directory
COPY src /app/src

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "src.ImageGenerator_html:app", "--host", "0.0.0.0", "--port", "8000"]

