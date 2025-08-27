# Use the official Python base image with the latest tag
FROM python:3.11-slim-buster


# #Install sudo for apt-get access
# RUN apt-get update && apt-get install -y \
#     sudo \
#     wkhtmltopdf \
#     && rm -rf /var/lib/apt/lists/*

# Replace deb.debian.org URLs with archive.debian.org in sources.list
# Disable valid-until check and allow insecure archive repository for apt
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
 && sed -i 's|http://deb.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list \
 && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99archive \
 && echo 'Acquire::AllowInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99archive \
 && apt-get update



 # Install dependencies
RUN apt-get update && \
    apt-get install -y sudo wget && \
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb && \
    apt install -y ./wkhtmltox_0.12.5-1.buster_amd64.deb && \
    rm -rf /var/lib/apt/lists/* wkhtmltox_0.12.5-1.buster_amd64.deb



    
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

