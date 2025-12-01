#读取add中的数据，list格式
import json

from get_info import get_info
from src.record import record

with open('../status/add.json', 'r') as f:
    add = json.load(f)
#对于add中的每一个元素，调用get_info函数
#当add不为空时
while add:
    id = add[0]
    try:
        print(id)
        info,_=get_info(id)
        print(info['title'])
        record(id, info['title'])
        add.remove(id)
        #把add写入add.json
        with open('../status/add.json', 'w') as f:
            json.dump(add, f)
    except:
        pass