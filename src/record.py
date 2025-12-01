import json
import os


def record(id, title):
    """
    将已经全部下载完成的动漫保存在aleady.json中。保存信息：id、标题
    :param id(int): 网站上的id
    :param title(str): 标题
    :return:
    """

    # 判断文件是否存在
    if os.path.exists('../status/already.json'):
        # 如果存在，则打开文件，读取内容
        with open('../status/already.json', "r", encoding='utf-8') as json_file:
            rec_list = json.load(json_file)
            already = set(rec_list)
    else:
        # 如果不存在，则创建一个空集合
        already = set()
    # 将id和title拼接成一个字符串，添加到集合中
    already.add(f'{id}:{title}')
    # 将集合转换为列表
    already = list(already)
    #对already进行排序
    already.sort(key=lambda x: int(x.split(':')[0]))
    # 将列表写入文件
    with open('../status/already.json', 'w', encoding='utf-8') as json_file:
        json.dump(already, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    id = 67
    title = 'ttt'
    record(id, title)
