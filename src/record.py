import json
import os


def record(id, title):
    """
    将已经全部下载完成的动漫保存在aleady.json中。保存信息：id、标题
    :param id(int): 网站上的id
    :param title(str): 标题
    :return:
    """

    if os.path.exists('../status/already.json'):
        with open('../status/already.json', "r", encoding='utf-8') as json_file:
            rec_list = json.load(json_file)
            already = set(rec_list)
    else:
        already = set()
    already.add(f'{id}:{title}')
    with open('../status/already.json', 'w', encoding='utf-8') as json_file:
        json.dump(list(already), json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    id = 67
    title = 'ttt'
    record(id, title)
