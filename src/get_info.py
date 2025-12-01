import json
import os
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_info_and_playlist(url):
    """
    从指定视频页url中获取信息和播放列表集合。
    :param url(str):视频页信息地址
    :return:info_and_play_list(list):一个二元列表，前者是info(dict)，后者是播放列表(list)
    """

    def get_html(url):
        """
        从制定url中获取html页面。获取的不是完整的html，通过selenium库，获取到想要的元素之后便不在获取。
        这个函数获取的html信息包含目前需要的所有视频信息。
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
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cor5"))  # 根据实际页面元素修改
                                        )
        # 获取页面 HTML
        html = driver.page_source

        # 关闭浏览器
        driver.quit()

        return html

    def match_playlist(html):
        """
        从html页面获取播放列表
        :param html(str):
        :return: play_list(list):播放列表
        """

        # 解析 HTML 内容
        soup = BeautifulSoup(html, 'html.parser')

        # 查找第一个匹配的 ul，class 为 'anthology-list-play size'
        ul_element = soup.find('ul', class_='anthology-list-play size')

        soup = BeautifulSoup(str(ul_element), 'html.parser')
        # 提取所有 <span> 标签中的内容
        play_list = [li.text.strip() for li in soup.find_all('li')]

        return play_list

    html = get_html(url)
    info = dict()
    soup = BeautifulSoup(html, 'html.parser')
    title_element = soup.find('h3', class_='slide-info-title hide')
    title = title_element.text
    info['title'] = title
    fraction_element = soup.find('div', class_='fraction')
    score_element = soup.find('em', class_='score cor2')
    score = fraction_element.text if score_element.text == 0.0 else score_element.text
    info['score'] = score
    date_pattern = re.compile(r'\d{4}年\d{1,2}月')
    info['date'] = ''
    # 查找所有<a>标签，并匹配内容
    for a_tag in soup.find_all('a', string=date_pattern):
        info['date']=a_tag.string
        break
    play_list = match_playlist(html)
    return info, play_list


def get_info(id):
    """
    从本地资源获取信息。；
    如果本地不存在信息，调用get_info_and_playlist函数。
    :param id: 网站上的if
    :return: info(dict)，playlist(list)
    """

    if os.path.exists(f'../cache/{id}_info.json'):
        with open(f'../cache/{id}_info.json', 'r', encoding='utf-8') as json_file:
            info, playlist = json.load(json_file)
    else:
        print('正在获取标题和集数信息')
        url = f'https://dick.xfani.com/bangumi/{id}.html'
        info, playlist = get_info_and_playlist(url)
        with open(f'../cache/{id}_info.json', 'w', encoding='utf-8') as json_file:
            json.dump((info, playlist), json_file, ensure_ascii=False, indent=4)
    return info, playlist


if __name__ == '__main__':
    url = 'https://dick.xfani.com/bangumi/2162.html'
    print(get_info_and_playlist(url))
