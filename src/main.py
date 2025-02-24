import json
import os

from download import download_video
from get_info import get_info
from get_video_url import get_video_url
from record import record

if __name__ == '__main__':
    if os.path.exists('../status/todo.json'):
        with open('../status/todo.json') as json_file:
            todo = json.load(json_file)
    else:
        todo = list()
        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo, json_file, ensure_ascii=False, indent=4)

    # 获取title，playlist，更新在status

    while todo:
        try:
            id = todo[0]
            print(f'获取id为{id}')
            info, playlist = get_info(id)
            title = info['title']
            print(f'名称为{title}')
            os.makedirs(f'D:/Downloads/Video/{title}', exist_ok=True)
            score = info['score']
            if not os.path.exists(f'D:/Downloads/Video/{title}/评分：{score}.txt'):
                with open(f'D:/Downloads/Video/{title}/评分：{score}.txt', "w", encoding='utf-8'):
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
                    print(f'正在下载{i}:{item}')
                    download_video(video_url, filename)
                    video_hashtable[f'{i}_success'] = 1
                    video_hashtable['success_num'] += 1
                    if video_hashtable['success_num'] == len(playlist):
                        todo.remove(id)
                        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
                            json.dump(todo, json_file, ensure_ascii=False, indent=4)
                    with open(f'../status/{id}_video.json', 'w', encoding='utf-8') as json_file:
                        json.dump(video_hashtable, json_file, ensure_ascii=False, indent=4)
                    record(id, title)
        except KeyboardInterrupt as e:
            print("用户主动停止")
            break
        except BaseException as e:
            print(f"异常类型: {type(e)}")

            print(f"异常信息: {str(e)}")
