import requests

def downloade(urls, filenames):
    if len(urls) != len(filenames):
        print("Error: 数量不匹配，URLs 和文件名长度应一致。")
        return

    for url, filename in zip(urls, filenames):
        try:
            print(f"正在下载: {filename}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"下载完成: {filename}")
        except Exception as e:
            print(f"下载失败: {filename}，错误信息：{e}")
