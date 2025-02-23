from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_info_and_playlist(url):
    """

    :param url(str):视频页信息
    :return:info_and_play_list(list):一个二元列表，前者是info(dict)，后者是集数列表(list)
    """

    def get_html(url):
        """

        :param url(str)
        :return: html(str)
        """
        # 配置 Edge 浏览器选项
        options = Options()
        options.use_chromium = True
        options.add_argument('--headless')  # 启用无头模式
        options.add_argument('--disable-gpu')  # 禁用 GPU

        # 启动 Edge 浏览器
        driver = webdriver.Edge(options=options)

        # 打开网页
        driver.get(url)

        # 等待页面加载完成，例如等待某个元素加载出来（可以根据你网页的结构更改元素）
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cor5"))  # 根据实际页面元素修改
        )
        # 获取页面 HTML
        html = driver.page_source

        # 关闭浏览器
        driver.quit()

        return html

    def match_playlist(html):
        """

        :param html(str)
        :return: play_list(list):
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
    score_element = soup.find('div', class_='fraction')
    score=score_element.text
    info['score']=score
    play_list = match_playlist(html)
    return info, play_list


if __name__ == '__main__':
    url = 'https://dick.xfani.com/bangumi/1917.html'
    print(get_info_and_playlist(url))
