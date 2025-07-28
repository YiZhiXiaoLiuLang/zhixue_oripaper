def generate_image_gallery(image_urls,OUTPUT_SERVER_HOST='http://39.99.41.233:65002/'
):
    """
    生成包含图片和下载按钮的HTML代码
    
    参数:
        image_urls (list): 图片URL列表
        
    返回:
        str: 包含图片和下载按钮的HTML字符串
    """
    html_parts = []
    
    # 添加基础HTML结构
    html_parts.append("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>图片库</title>
        <style>
            .gallery {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                padding: 20px;
            }
            .image-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                background: #f9f9f9;
                max-width: 300px;
            }
            .image-container {
                height: 200px;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }
            .image-container img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
            }
            .download-btn {
                display: block;
                margin-top: 10px;
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                text-align: center;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
            }
            .download-btn:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="gallery">
    """)
    
    # 为每张图片生成卡片
    for i, url in enumerate(image_urls):
        # 从URL提取文件名
        filename = url.split('/')[-1].split('?')[0]  # 移除查询参数
        if '.' not in filename:  # 确保有扩展名
            filename = f"image_{i+1}.jpg"
        
        html_parts.append(f"""
            <div class="image-card">
                <div class="image-container">
                    <img src="{OUTPUT_SERVER_HOST+url}" alt="图片 {i+1}" onerror="this.src='https://via.placeholder.com/300x200?text=图片加载失败'">
                </div>
                <a href="{OUTPUT_SERVER_HOST+url}" download="{filename}" class="download-btn">
                    下载图片 {i+1}
                </a>
            </div>
        """)
    
    # 闭合HTML结构
    html_parts.append("""
        </div>
    </body>
    </html>
    """)
    
    return ''.join(html_parts)

# 使用示例
if __name__ == "__main__":
    example_urls = [
        "http://localhost:50001/output/tmp1748494675.5771117_1.jpg",
        "http://localhost:50001/output/tmp1748494675.5771117_2.jpg"
    ]
    
    html_output = generate_image_gallery(example_urls)
    print(html_output)