import os
import json   

    
def check_bjmm(item, min_):
    res2 = item["Res"]["Bjmm 2LV"]
    min2 = min(list(filter(lambda v: isinstance(v, (int, float)), res2.values())))
    res3 = item["Res"]["Bjmm 3LV"]
    min3 = min(list(filter(lambda v: isinstance(v, (int, float)), res2.values())))
    return min3 > min_ and min2 > min_
    
    
path = os.path.dirname(os.path.abspath(__file__))
source = 'results_2.json'
dest = 'final.json'
complete_path = os.path.join(path, source)

with open(complete_path, 'r') as file:
    data = json.load(file)
new_data={}
for p in data.keys():
    values = list(filter(lambda item: item.get("State") != "Fail", data[p]))
    values = list(filter(lambda item: check_bjmm(item, 130), data[p]))
    if len(values)>0:
        new_data[p]=values
complete_path = os.path.join(path, dest)


with open(complete_path, 'w') as file:
    json.dump(new_data, file, indent=4)

