import re

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_video_url(url):
    """

    :param url(str):视频页信息
    :return:video_url(str):视频下载地址
    """

    def get_html(url):
        """

        :param url(str)
        :return: html(str)
        """
        # 配置 Edge 浏览器选项
        options = Options()
        options.use_chromium = True
        ua = UserAgent()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument('--headless')  # 启用无头模式
        options.add_argument('--disable-gpu')  # 禁用 GPU

        # 启动 Edge 浏览器
        driver = webdriver.Edge(options=options)

        # 打开网页
        driver.get(url)

        # 等待页面加载完成，例如等待某个元素加载出来（可以根据你网页的结构更改元素）
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "playleft"))  # 根据实际页面元素修改
        )
        # 获取页面 HTML
        html = driver.page_source

        # 关闭浏览器
        driver.quit()

        return html

    def match_video_url(html):
        """

        :param html(str)
        :return: url(str):视频下载地址
        """

        # 正则表达式
        pattern = r"(?<=;url=)[^ ]+\.mp4"

        # 使用 re.findall 找到所有匹配的结果
        matches = re.findall(pattern, html)

        # 输出匹配结果
        return matches[0]

    if url != None:
        html = get_html(url)
        video_url = match_video_url(html)
        return video_url
    else:
        return None


if __name__ == '__main__':
    url = 'https://dick.xfani.com/watch/401/1/24.html'
    print(get_video_url(url))
