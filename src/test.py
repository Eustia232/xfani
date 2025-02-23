import json

d=dict()
d[1]=5
print(d)
with open('test.json','w') as file:
    json.dump(d,file)