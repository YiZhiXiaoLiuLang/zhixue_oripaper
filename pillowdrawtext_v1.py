from PIL import Image, ImageDraw, ImageFont
import os

def pillowdrawtext(image_path, lines, font_path=None, font_size=20, line_spacing=5):
    # 打开图像
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 设置字体路径，默认使用 Windows 黑体（simhei.ttf）
    if font_path is None:
        font_path = "C:/Windows/Fonts/simhei.ttf"
        if not os.path.exists(font_path):
            raise FileNotFoundError("找不到默认字体，请手动指定一个支持中文的 .ttf 字体路径。")

    font = ImageFont.truetype(font_path, font_size)

    # 从 (0, 0) 开始写字
    x, y = 0, 0

    for line in lines:
        draw.text((x, y), line, font=font, fill=(0, 0, 0))
        y += font.getsize(line)[1] + line_spacing

    # 直接覆盖原图
    image.save(image_path)
    print(f"原图已成功覆盖：{image_path}")
