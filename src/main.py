import json
import os

from download import download_video, DownloadSpeedTooLowException
from get_info import get_info
from get_video_url import get_video_url
from record import record

if __name__ == '__main__':

    with open('../status/download_config.json', 'r') as f:
        config = json.load(f)
        path = config['path']
    
    
    if os.path.exists('../status/todo.json'):
        with open('../status/todo.json', 'r', encoding='utf-8') as json_file:
            todo = json.load(json_file)
    else:
        todo = list()
        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo, json_file, ensure_ascii=False, indent=4)

    if os.path.exists('../status/todo2.json'):
        with open('../status/todo2.json') as json_file:
            todo2 = json.load(json_file)
            todo.extend(todo2)
            todo2.clear()
        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo, json_file, ensure_ascii=False, indent=4)
        with open('../status/todo2.json', 'w', encoding='utf-8') as json_file:
            json.dump(todo2, json_file, ensure_ascii=False, indent=4)


    # 获取title，playlist，更新在status

    try_time = 0

    while todo:
        try:
            todo_num= len(todo)
            index=try_time%todo_num
            id = todo[index]
            print(f'获取id为{id}')
            info, playlist = get_info(id)
            title = info['title']
            title_path=title.replace("/","-")
            print(f'名称为{title}')
            os.makedirs(f'{path}/{title_path}', exist_ok=True)
            score = info['score']
            date = info['date']
            if not os.path.exists(f'{path}/{title_path}/评分：{score}.txt'):
                with open(f'{path}/{title_path}/评分：{score}.txt', "w", encoding='utf-8') as file:
                    file.write(f'date:{date}\n')
            # 要确保哈希表的键是str类型。即使是int类型，在保存到json文件时也会被强制转化为str类型。
            if os.path.exists(f'../cache/{id}_video.json'):
                with open(f'../cache/{id}_video.json', 'r', encoding='utf-8') as json_file:
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
                    with open(f'../cache/{id}_video.json', 'w', encoding='utf-8') as json_file:
                        json.dump(video_hashtable, json_file, ensure_ascii=False, indent=4)

                filename = f'{path}/{title_path}/{title_path + item}.mp4'
                if f'{i}_success' not in video_hashtable:
                    print(f'正在下载{i}:{item}')
                    download_video(video_url, filename)
                    video_hashtable[f'{i}_success'] = 1
                    video_hashtable['success_num'] += 1
                    if video_hashtable['success_num'] == len(playlist):
                        todo.remove(id)
                        with open('../status/todo.json', 'w', encoding='utf-8') as json_file:
                            json.dump(todo, json_file, ensure_ascii=False, indent=4)
                        record(id, title)
                    with open(f'../cache/{id}_video.json', 'w', encoding='utf-8') as json_file:
                        json.dump(video_hashtable, json_file, ensure_ascii=False, indent=4)

        except KeyboardInterrupt as e:
            print("用户主动停止")
            break
        except BaseException as e:
            print(f"异常类型: {type(e)}")

            print(f"异常信息: {str(e)}")
        except DownloadSpeedTooLowException as e:
            print(e)
        finally:
            try_time += 1
