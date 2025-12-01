import requests
from tqdm import tqdm
from fake_useragent import UserAgent
import time

class DownloadSpeedTooLowException(Exception):
    pass

def download_video(url, filename):
    ua = UserAgent()

    # 获取一个随机的 User-Agent 字符串
    headers = {
        'User-Agent': ua.random  # 使用随机的 User-Agent
    }

    # 发起GET请求，stream=True表示流式读取
    response = requests.get(url, stream=True, headers=headers,timeout=30)

    # 获取视频文件的总大小（Content-Length），以便显示进度条
    total_size = int(response.headers.get('Content-Length', 0))

    # 检查响应状态码
    if response.status_code == 200:

        # 打开文件并写入
        with open(filename, 'wb') as f:
            # 记录开始时间
            start_time = time.time()
            # 初始化已下载的大小
            downloaded_size = 0
            # 初始化 flag
            flag = 0
            # 使用 tqdm 显示进度条
            for chunk in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB',
                              desc="Downloading"):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    download_progress = int((f.tell() / total_size) * 100)

                # 每 5 秒钟检查一次下载速度
                elapsed_time = time.time() - start_time
                if elapsed_time >= 5:
                    download_speed = downloaded_size / 1024 / elapsed_time  # KB/s

                    # 判断下载速度是否小于 150 KB/s
                    if download_speed < 150:
                        flag += 1
                        print(f"下载速度小于 150 KB/s，flag 增加到 {flag}")

                    # 如果 flag 达到 10，抛出异常
                    if flag >= int(download_progress/2)+5:
                        raise DownloadSpeedTooLowException(f"下载速度过低，超过 {int(download_progress/2)+5} 次检测未达到 150 KB/s，下载被中止。")

                    start_time = time.time()  # 重置开始时间
                    downloaded_size = 0  # 重置已下载的大小

        print(f'\n视频已成功下载到 {filename}')
    else:
        print('视频下载失败，状态码:', response.status_code)


if __name__ == '__main__':
    try:
        url = 'https://play.xfvod.pro/Y/Y-%E6%B8%B8%E6%88%8F%E4%BA%BA%E7%94%9F/TV/01.mp4'
        download_video(url, "../test.mp4")
    except DownloadSpeedTooLowException as e:
        print(e)
