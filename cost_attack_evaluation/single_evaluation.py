import os  
import json  
from attacks.RSDP.bjmm_2LV import bjmm_2LV_interface
from attacks.RSDP.bjmm_3LV import bjmm_3LV
from attacks.RSDP.stern import stern
import configparser

with open('single_execution.json') as file:
    params = json.load(file)
p=params['params']['p']
n=params['params']['n']
k=params['params']['k']
z=params['params']['z']

data={}
data["Stern"]=stern(p, n, k, z)
data["Bjmm 2LV"]=bjmm_2LV_interface(p, n, k, z, params)
data["Bjmm 3LV"]=bjmm_3LV(p, n, k, z)

dir ='single_execution_results'
path = os.path.dirname(os.path.abspath(__file__))
complete_path = os.path.join(path, dir)

if not os.path.exists(complete_path):
    os.makedirs(complete_path)

complete_path = os.path.join(path, "single_execution.json")
with open(complete_path, 'w') as file:
    json.dump(data, file, indent=4)

