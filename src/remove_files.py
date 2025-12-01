import json
import os


def remove_files():
    # 获取already.json文件中的id列表，如果id存在，就删除对应的json文件
    with open('../status/already.json', 'r', encoding='utf-8') as file:
        already = json.load(file)
        for item in already:
            id = item.split(':')[0]
            try:
                os.remove(f'../cache/{id}_video.json')
                print(f'删除了{item}')
            except FileNotFoundError as e:
                pass
            try:
                os.remove(f'../cache/{id}_info.json')
                print(f'删除了{item}')
            except FileNotFoundError as e:
                pass


if __name__ == '__main__':
    remove_files()
