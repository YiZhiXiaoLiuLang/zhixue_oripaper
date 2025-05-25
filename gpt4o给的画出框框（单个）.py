import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# 假设画布大小（以topPercent等字段为参考估计，假设整体高度为1555px，宽度为1118px）
canvas_width = 1118
canvas_height = 1555

# 原始数据
rect_data = {
    'strokeStyle': 'rgba(7, 193, 175, 1)',
    'topPercent': 0.4045016077170418,
    'lineWidth': 1,
    'pTop': 0,
    'widthPercent': 0.11896243291592129,
    'top': 629,
    'left': 140,
    'width': 133,
    'pLeft': 0,
    'ID': 'edcda71c-4049-45eb-af08-db33549618dd',
    'ErrorCode': 0,
    'leftPercent': 0.1252236135957066,
    'height': 129,
    'heightPercent': 0.08295819935691319
}

# 创建空白图像
image = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
draw = ImageDraw.Draw(image)

# 解析颜色
rgba = (7, 193, 175, 255)  # 转换为不透明的 RGBA

# 获取矩形框位置和大小
left = rect_data['left']
top = rect_data['top']
right = left + rect_data['width']
bottom = top + rect_data['height']

# 绘制矩形
draw.rectangle([left, top, right, bottom], outline=rgba, width=rect_data['lineWidth'])

# 显示图像
plt.figure(figsize=(6, 9))
plt.imshow(image)
plt.axis("off")
plt.title("Rectangle Drawn on Canvas")
plt.show()
