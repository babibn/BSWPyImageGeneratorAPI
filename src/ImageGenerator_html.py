from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal, Optional
import imgkit
import io
import tempfile
import os

app = FastAPI()

class ImageRequest(BaseModel):
    width: int = 800
    height: int = 600
    text: str
    wrap_text: bool = True
    bg_color: str = "linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d)"
    fg_color: str = "#ffffff"
    font: str = "Arial"
    font_size: int = 36
    text_shadow: Optional[str] = "2px 2px 4px rgba(0,0,0,0.5)"
    text_direction: Literal["ltr", "rtl"] = "ltr"
    line_spacing: float = 1.5
    escape_text: bool = True

def generate_html(params: dict) -> str:
    # Escape text and handle newlines
    from html import escape
    if 'escape_text' not in params:
        params['escape_text'] = True
    if params['escape_text'] == True:
        safe_text = escape(params['text']).replace('\n', '<br>')
    else:
     safe_text=params['text']
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: {params['width']}px;
                height: {params['height']}px;
            }}
            body {{
                background: {params['bg_color']};
                width: 100vw;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: {params['font']};
                color: {params['fg_color']};
                direction: {params['text_direction']};
            }}
            .content {{
                max-width: {params['width'] - 40}px;
                padding: 20px;
                white-space: {'pre-wrap' if params['wrap_text'] else 'nowrap'};
                font-size: {params['font_size']}px;
                line-height: {params['line_spacing']}em;
                text-shadow: {params['text_shadow']};
                word-break: break-word;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <div class="content">{safe_text}</div>
    </body>
    </html>
    '''

def html_to_image(params: dict) -> bytes:
    html_content = generate_html(params)
    options = {
        'format': 'png',
        'width': params['width'],
        'height': params['height'],
        'enable-local-file-access': None,
        'quiet': ''
    }
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        f.write(html_content.encode('utf-8'))
        html_path = f.name
    try:
        return imgkit.from_file(html_path, False, options=options)
    finally:
        os.unlink(html_path)

@app.post("/generate")
async def generate_image(params: ImageRequest = Body(...)):
    config = {
        'width': params.width,
        'height': params.height,
        'text': params.text,
        'wrap_text': params.wrap_text,
        'bg_color': params.bg_color,
        'fg_color': params.fg_color,
        'font': params.font,
        'font_size': params.font_size,
        'text_shadow': params.text_shadow or "none",
        'text_direction': params.text_direction,
        'line_spacing': params.line_spacing,
        'escape_text': params.escape_text if hasattr(params, 'escape_text') else True
    }
    image_bytes = html_to_image(config)
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
