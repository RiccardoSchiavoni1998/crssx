import os  
import json  
from attacks.RSDP.bjmm_2LV_detailed import bjmm_2LV_detailed
from attacks.RSDP.bjmm_3LV_detailed import bjmm_3LV_detailed
from attacks.RSDP.bjmm_2LV_fast import bjmm_2LV_fast
from attacks.RSDP.bjmm_3LV_fast import bjmm_3LV_fast
from attacks.RSDP.stern import stern

def exec_single_evaluation(mode):
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'single_execution_config.json')

    # Carica il file JSON
    with open(complete_path, "r") as file:
        params = json.load(file)
        
    p=params['params']['p']
    n=params['params']['n']
    k=params['params']['k']
    z=params['params']['z']

    data={}
    data["Stern"]=stern(p, n, k, z)
    if mode == "Fast":
        data["Bjmm 2LV"]=bjmm_2LV_fast(p, n, k, z, params)
        #data["Bjmm 3LV"]=bjmm_3LV_fast(p, n, k, z)
    else:
        data["Bjmm 2LV"]=bjmm_2LV_detailed(p, n, k, z, params)
        #data["Bjmm 3LV"]=bjmm_3LV_detailed(p, n, k, z)
  
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'single_execution_results')
    if not os.path.exists(complete_path):
        os.makedirs(complete_path)
    file_name = "single_execution_"+mode+".json"
    complete_path = os.path.join(complete_path, file_name)
    with open(complete_path, 'w') as file:
        json.dump(data, file, indent=4)

