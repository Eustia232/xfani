import json
import os

from get_info_and_playlist import get_info_and_playlist
from get_video_url import get_video_url
from download import download_video


def get_info(id):
    if os.path.exists(f'../status/{id}_info.json'):
        with open(f'../status/{id}_info.json', 'r', encoding='utf-8') as json_file:
            info, playlist = json.load(json_file)
    else:
        print('正在获取标题和集数信息')
        url = f'https://dick.xfani.com/bangumi/{id}.html'
        info, playlist = get_info_and_playlist(url)
        with open(f'../status/{id}_info.json', 'w', encoding='utf-8') as json_file:
            json.dump((info, playlist), json_file, ensure_ascii=False, indent=4)
    return info,playlist


def record(id):
    if os.path.exists('../status/already.json'):
        with open('../status/already.json') as json_file:
            already=json.load(json_file)
    else:
        already=list()
    already.append(id)
    with open('../status/already.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    if os.path.exists('../status/todo.json'):
        with open('../status/todo.json') as json_file:
            todo=json.load(json_file)
    else:
        todo=list()
        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo, json_file, ensure_ascii=False, indent=4)

    # 获取title，playlist，更新在status

    while todo:
        try:
            id = todo[0]
            print(f'获取id为{id}')
            info, playlist = get_info(id)
            title=info['title']
            print(f'名称为{title}')
            os.makedirs(f'D:/Downloads/Video/{title}', exist_ok=True)
            score=info['score']
            with open(f'D:/Downloads/Video/{title}/评分：{score}.txt'):
                pass
            # 要确保哈希表的键是str类型。即使是int类型，在保存到json文件时也会被强制转化为str类型。
            if os.path.exists(f'../status/{id}_video.json'):
                with open(f'../status/{id}_video.json', 'r', encoding='utf-8') as json_file:
                    video_hashtable = json.load(json_file)
            else:
                video_hashtable = dict()
                video_hashtable['success_num'] = 0

            for i, item in enumerate(playlist, start=1):

                if str(i) in video_hashtable:
                    video_url = video_hashtable[str(i)]
                else:
                    print(f'正在解析{i}:{item}下载地址')
                    url = f'https://dick.xfani.com/watch/{id}/1/{i}.html'
                    video_url = get_video_url(url)
                    video_hashtable[str(i)] = video_url
                    with open(f'../status/{id}_video.json', 'w', encoding='utf-8') as json_file:
                        json.dump(video_hashtable, json_file, ensure_ascii=False, indent=4)

                filename = f'D:/Downloads/Video/{title}/{title + item}.mp4'
                if f'{i}_success' not in video_hashtable:
                    download_video(video_url, filename)
                    video_hashtable[f'{i}_success'] = 1
                    video_hashtable['success_num'] += 1
                    if video_hashtable['success_num'] == len(playlist):
                        todo.remove(id)
                        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
                            json.dump(todo, json_file, ensure_ascii=False, indent=4)
                        record(id)
                    with open(f'../status/{id}_video.json', 'w', encoding='utf-8') as json_file:
                        json.dump(video_hashtable, json_file, ensure_ascii=False, indent=4)
        except BaseException as e:
            print(f"异常类型: {type(e)}")

            print(f"异常信息: {str(e)}")
