import requests
from tqdm import tqdm


def download_video(url, filename):
    # 发起GET请求，stream=True表示流式读取
    response = requests.get(url, stream=True)

    # 获取视频文件的总大小（Content-Length），以便显示进度条
    total_size = int(response.headers.get('Content-Length', 0))

    # 检查响应状态码
    if response.status_code == 200:

        # 打开文件并写入
        with open(filename, 'wb') as f:
            # 使用tqdm显示进度条
            for chunk in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB',
                              desc="Downloading"):
                if chunk:
                    f.write(chunk)
        print(f'视频已成功下载到 {filename}')
    else:
        print('视频下载失败，状态码:', response.status_code)


if __name__ == '__main__':
    url = 'https://play.xfvod.pro/Y/Y-%E6%B8%B8%E6%88%8F%E4%BA%BA%E7%94%9F/TV/01.mp4'
    download_video(url, "../test.mp4")
