## Overview
A simple API server for generating images from HTML using FastAPI. Supports various text styling options including background colors, fonts, sizes, and more.

## Parameters
| Parameter    | Type   | Description                                                                 |
|--------------|--------|-----------------------------------------------------------------------------|
| width        | int    | Width of the output image in pixels (default: 800)                         |
| height       | int    | Height of the output image in pixels (default: 600)                        |
| text         | str    | Text content to be displayed on the image                                 |
| wrap_text    | bool   | Whether to allow text wrapping (default: true)                            |
| bg_color     | str    | Background color using CSS gradients or hex code                         |
| fg_color     | str    | Foreground/text color in hex format (default: #ffffff)                   |
| font         | str    | Font family name (default: Arial)                                        |
| font_size    | int   | Text size in pixels (default: 36)                                        |
| text_shadow  | str   | CSS text shadow effect (default: "2px 2px 4px rgba(0,0,0,0.5)")          |
| text_direction | string| Text direction ("ltr" or "rtl")                                         |
| line_spacing | float  | Line height multiplier (default: 1.5)                                   |
| escape_text  | bool   | Escape HTML characters in the text (default: true)                      |

## Usage Examples
### Simple usage:
```python
import requests

url = "http://localhost:8000/generate"
data = {
    "text": "Hello, World!",
    "width": 800,
    "height": 600,
    "font_size": 24
}

response = requests.post(url, json=data)
with open("output.png", "wb") as f:
    f.write(response.content)


```
 

## Running the API Server Locally
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn src.ImageGenerator_html:app --host 0.0.0.0 --port 8000
   ```

## Running with Docker
### Building the Docker Image
1. Navigate to the project directory containing your `Dockerfile`.
2. Build the Docker image:
   ```bash
   docker build -t image-generator .
   ```
3. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 --name image-gen image-generator
   ```
4. The API will be accessible at `http://localhost:8000/generate`.

### Using Docker Compose (Optional)
1. Create a `docker-compose.yml` file in the project directory with the following content:
   ```yaml
   version: '3'
   services:
     image_generator:
       build: .
       ports:
         - "8000:8000"
   ```
2. Run the Docker Compose setup:
   ```bash
   docker-compose up -d
   ```
3. The API will be accessible at `http://localhost:8000/generate`.

## Calling the API via cURL
To generate an image, use the following cURL command:
```sh
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{
    "text": "Hello, World!",
    "width": 800,
    "height": 600,
    "font_size": 24
}'
```

## JSON for n8n Node Integration
To integrate this API with n8n (an automation tool), you can use the following JSON structure in your workflow:
```json
{
    "text": "Hello, World!",
    "width": 800,
    "height": 600,
    "font_size": 24
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This README provides a detailed guide on how to set up and run the API server locally or using Docker, as well as examples of calling the API via cURL and JSON format suitable for integration with n8n.