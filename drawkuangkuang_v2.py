from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Optional
import os

def create_blank_canvas(width: int = 1118, height: int = 1555, color=(255, 255, 255)) -> Image.Image:
    return Image.new("RGB", (width, height), color)

def rgba_string_to_rgb(rgba_str: str) -> tuple:
    parts = rgba_str.replace('rgba(', '').replace(')', '').split(',')
    return tuple(map(int, parts[:3]))

def draw_rectangle(draw: ImageDraw.ImageDraw, rect_data: Dict, font: Optional[ImageFont.ImageFont] = None, font_size: int = 16):
    left = rect_data['left']
    top = rect_data['top']
    width = rect_data['width']
    height = rect_data['height']
    right = left + width
    bottom = top + height

    line_width = 5  # 固定线条粗细为5

    color = rgba_string_to_rgb(rect_data.get('strokeStyle', 'rgba(0,0,0,1)'))

    # 绘制矩形
    draw.rectangle([left, top, right, bottom], outline=color, width=line_width)

    # 添加文字（左上角）
    text = rect_data.get('addtext', '')
    if text:
        text_position = (left+5, max(0, top - font_size - 2))  # 避免文字出界
        draw.text(text_position, text, fill=color, font=font)

def draw_rectangles_on_canvas(
    rectangles: List[Dict],
    canvas: Optional[Image.Image] = None,
    canvas_width: int = 1118,
    canvas_height: int = 1555,
    save_path: Optional[str] = None,
    show: bool = False,
    font_path: Optional[str] = None,
    font_size: int = 20
) -> Image.Image:
    if canvas is None:
        if save_path and os.path.isfile(save_path):
            # 文件存在，打开图片作为画布
            canvas = Image.open(save_path).convert("RGB")
        else:
            # 文件不存在，创建空白画布
            canvas = create_blank_canvas(canvas_width, canvas_height)

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype(font_path if font_path else "arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()

    for rect in rectangles:
        draw_rectangle(draw, rect, font=font, font_size=font_size)

    if save_path:
        canvas.save(save_path)

    if show:
        try:
            import matplotlib.pyplot as plt
            plt.imshow(canvas)
            plt.axis('off')
            plt.show()
        except ImportError:
            print("matplotlib 未安装，无法显示图像。")

    return canvas
