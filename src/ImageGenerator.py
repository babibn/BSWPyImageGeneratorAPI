from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Literal, Tuple
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = FastAPI()

class ImageDefinition(BaseModel):
    width: int = 600
    height: int = 400
    text: str
    wrap_text: bool = True
    bg_color: List[str] = ["#222222"]  # One for solid, two+ for gradient
    fg_color: List[str] = ["#ffffff"]
    background_type: Literal["solid", "gradient-linear", "gradient-radial"] = "solid"
    text_shadow: bool = False
    text_direction: Literal["ltr", "rtl"] = "ltr"
    text_align: Literal["left", "center", "right"] = "center"
    font: str = "arial.ttf"
    font_size: int = 40
    shadow_color: str = "#000000"
    shadow_offset: Tuple[int, int] = (2, 2)
    line_spacing: int = 10

def make_gradient(size, colors, mode="linear"):
    base = Image.new("RGB", size, colors[0])
    draw = ImageDraw.Draw(base)
    if mode == "linear" and len(colors) > 1:
        top, bottom = colors[0], colors[1]
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(int(top[1:3], 16) * (1 - ratio) + int(bottom[1:3], 16) * ratio)
            g = int(int(top[3:5], 16) * (1 - ratio) + int(bottom[3:5], 16) * ratio)
            b = int(int(top[5:7], 16) * (1 - ratio) + int(bottom[5:7], 16) * ratio)
            draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    elif mode == "radial" and len(colors) > 1:
        center = (size[0] // 2, size[1] // 2)
        max_radius = max(center)
        for i in range(max_radius, 0, -1):
            ratio = i / max_radius
            r = int(int(colors[0][1:3], 16) * ratio + int(colors[1][1:3], 16) * (1 - ratio))
            g = int(int(colors[0][3:5], 16) * ratio + int(colors[1][3:5], 16) * (1 - ratio))
            b = int(int(colors[0][5:7], 16) * ratio + int(colors[1][5:7], 16) * (1 - ratio))
            draw.ellipse(
                [center[0] - i, center[1] - i, center[0] + i, center[1] + i],
                fill=(r, g, b)
            )
    return base


    # Check if text contains Persian/Arabic characters
    persian_arabic_ranges = [
        (0x0600, 0x06FF),  # Arabic
        (0x0750, 0x077F),  # Arabic Supplement
        (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
    ]
    return any(ord(char) in range(start, end + 1) 
              for char in text 
              for start, end in persian_arabic_ranges)

def wrap_text(text, font, max_width, draw, text_direction="ltr"):
    if text_direction == "rtl":
        words = text.split(' ')[::-1]  # Reverse words for RTL
    else:
        words = text.split(' ')
    
    lines = []
    current_words = []
    
    for word in words:
        current_words.append(word)
        test_line = ' '.join(current_words)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width > max_width:
            if len(current_words) > 1:
                current_words.pop()
                lines.append(' '.join(current_words))
                current_words = [word]
            else:
                lines.append(word)
                current_words = []
    
    if current_words:
        lines.append(' '.join(current_words))
    
    return lines

@app.post("/generate")
def generate_image(defn: ImageDefinition = Body(...)):
    # Background
    if defn.background_type == "solid":
        img = Image.new("RGB", (defn.width, defn.height), defn.bg_color[0])
    else:
        mode = "linear" if defn.background_type == "gradient-linear" else "radial"
        img = make_gradient((defn.width, defn.height), defn.bg_color, mode)

    draw = ImageDraw.Draw(img)
    try:
        font_path = defn.font
        if not os.path.isfile(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # fallback for Linux
        font = ImageFont.truetype(font_path, defn.font_size)
    except Exception:
        font = ImageFont.load_default()

    # Text wrapping with direction
    if defn.wrap_text:
        lines = wrap_text(defn.text, font, defn.width - 40, draw, defn.text_direction)
    else:
        lines = defn.text.split("\n")

    # Calculate total text box dimensions
    max_width = 0
    total_height = 0
    line_dimensions = []
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        max_width = max(max_width, width)
        total_height += height + defn.line_spacing
        line_dimensions.append((width, height))
    
    total_height -= defn.line_spacing  # Remove extra spacing after last line
    
    # Calculate starting position to center the entire text box
    start_x = (defn.width - max_width) // 2
    start_y = (defn.height - total_height) // 2
    y = start_y

    # Draw each line
    # Calculate x position based on alignment only
    for i, line in enumerate(lines):
        width, height = line_dimensions[i]
        
        # Handle alignment independently of direction
        if defn.text_align == "left":
            x = start_x
        elif defn.text_align == "right":
            x = start_x + (max_width - width)
        else:  # center
            x = start_x + (max_width - width) // 2
        
        # Only reverse the individual line if it contains RTL text and direction is RTL
        display_line = line
        if defn.text_shadow:
            draw.text((x + defn.shadow_offset[0], y + defn.shadow_offset[1]), 
                     display_line, font=font, fill=defn.shadow_color)
        draw.text((x, y), display_line, font=font, fill=defn.fg_color[0])
        y += height + defn.line_spacing

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# Example usage: POST JSON to /generate
# {
#   "width": 600,
#   "height": 400,
#   "text": "سلام\nHello world!",
#   "wrap_text": true,
#   "bg_color": ["#222222", "#00ffcc"],
#   "fg_color": ["#ffffff"],
#   "background_type": "gradient-linear",
#   "text_shadow": true,
#   "text_direction": "rtl",
#   "font": "arial.ttf",
#   "font_size": 40
# }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
