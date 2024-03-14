import os
import json
from attacks.RSDP.bjmm_2LV import bjmm_2LV_opt_size_pk
from attacks.RSDP.bjmm_3LV import bjmm_3LV_opt_size_pk
from attacks.RSDP.stern import stern_opt_size_pk
import concurrent.futures
from math import *
from filelock import FileLock
import multiprocessing
import threading

#CATEGORY 1
category = 1
security_level = 128
target_pk_size = 128*log(127*7,2)
name = 'results'

"""
#CATEGORY 3
category = 1
security_level = 192
target_pk_size = 187*log(127*7,2
name = 'results'

#CATEGORY 5
category = 5
security_level = 251
target_pk_size = 251*log(127*7,2)
name = 'results'
"""

def create_d_set(p,z):
    list_D = []
    g = 2
    list_E = []
    for i in range(z):
        list_E.append(g**i)
    for a in list_E:
        count = 0
        for b in list_E:
            res = (a-b)%p
            if res!=0 and not(res in list_E):
                list_D.append(res)
                count += 1
                
    return count, len(list_D)

def get_params(iter):
    
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = 'res_cat'+str(category)+'/'+name+"_"+str(iter-1)+'.json'
    complete_path = os.path.join(path, file_name)
    
    with open(complete_path, 'r') as file:
        data = json.load(file)
        
    for p in data.keys():
        values = list(filter(lambda item: item.get("State") != "Fail", data[p]))
        if len(values)>0:
            data[p] = values

    file_name = 'res_cat'+str(category)+'/'+name+"_"+str(iter)+'.json'

    complete_path = os.path.join(path, file_name)
    
    with open(complete_path, 'w') as file:
        json.dump(data, file, indent=4)
        
    return data, file_name
    
def init_params(target_pk_size):
    
    data = {}    
    
    max_n = 256
    min_n = 80
    
    dim_set = [3, 5, 7]
    list_p = [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    
    for p in list_p:
        list_elem=[]
        for n in range(min_n, max_n+1):
            #for r in rates:
            for z in dim_set:
                elem = {}
                k=int(n*(0.6))
                pk_size =  n*log(z*p ,2)
                if pk_size<=target_pk_size:
                    elem["Params"] = {"n":n, "k":k, "z":z, "p":p}
                    elem["Pk Size"] = pk_size
                    elem["State"] = "Ok"
                    elem["Res"] = {}
                    list_elem.append(elem)
        #devo ordinare list_elem?
        data[p]=list_elem
    
    #data = filter_per_category(data, category)
    #create file
    file_name = 'res_cat'+str(category)+'/'+name+"_"+'0.json'
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, file_name)
    with open(complete_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data, file_name

"""def filter_per_category(data, category):
    previous_category = []
    if category == 3:
        previous_category.append(1)
    if category == 5:
        previous_category.append(1,3)
    if len(previous_category)>0:
        for cat in previous_category:
            
            file_name = f"res/{name}_0.json"
            path = os.path.dirname(os.path.abspath(__file__))
            complete_path = os.path.join(path, file_name)
            
            if os.path.exists(complete_path):
                with open(complete_path, 'r') as file:
                    previous_data = json.load(file)
                    for k in previous_data.key()"""

def update_params(file_name, data):
    
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, file_name)
    
    with open(complete_path, 'w') as file:
        json.dump(data, file, indent=4)
                        
def find_opt_values_stern(elem):
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
    safe_s, current_best = stern_opt_size_pk(p, n, k, z, security_level) 
    if safe_s:
        elem["State"] = "Ok"
    else:
        elem["State"] = "Fail"
    
    elem["Res"]["Stern"] = current_best
    
    return elem
                    
def find_opt_values_bjmm_2LV(elem):
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
    
    """
    elem["Params"] = {"n":n, "k":k, "z":z}
    elem["Pk Size"] = pk_size
    elem["State"] = "None"
    elem["Res"] = {}
    """
    
    current_best = elem["Res"]["Stern"]
    
    safe_s, res = bjmm_2LV_opt_size_pk(p, n, k, z, current_best, security_level) 
    
    if safe_s:
        elem["State"] = "Ok"
    else:
        elem["State"] = "Fail"
    
    elem["Res"]["Bjmm 2LV"] = res
    
    return elem

def find_opt_values_bjmm_3LV(elem):
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
    
    """
    elem["Params"] = {"n":n, "k":k, "z":z}
    elem["Pk Size"] = pk_size
    elem["State"] = "None"
    elem["Res"] = {}
    """
    
    current_best = min(list(filter(lambda valore: isinstance(valore, (int, float)), elem["Res"]["Bjmm 2LV"].values())))

    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1
    safe_s, res = bjmm_3LV_opt_size_pk(p, n, k, z, zD, alpha_e, alpha_d, current_best, security_level)
    
    if safe_s:
        elem["State"] = "Ok"
    else:
        elem["State"] = "Fail"
    
    elem["Res"]["Bjmm 3LV"] = res
    
    return elem

def main():  
    
    num_workers = 8
    
    """list_params, file_name = init_params(target_pk_size)
    counter = 0
    for p in list_params.keys():
        print("________________________________________________")
        print(counter, len(list_params.keys()))
        list_elem = list_params[p]
        list_res = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            for elem, res in zip(list_elem, executor.map(find_opt_values_stern, list_elem)):
                try:
                    list_res.append(res)
                except Exception as e:
                    print(e, elem)
        counter+=1
        list_params[p] = list_res
        update_params(file_name, list_params)
        
    list_params, file_name = get_params(1)          
    print(len(list_params))
    counter = 0
    for p in list_params.keys():
        print("________________________________________________")
        print(counter, len(list_params.keys()))
        list_elem = list_params[p]
        list_res = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            for elem, res in zip(list_elem, executor.map(find_opt_values_bjmm_2LV, list_elem)):
                try:
                    list_res.append(res)
                except Exception as e:
                    print(e, elem)
        counter+=1
        list_params[p] = list_res
        update_params(file_name, list_params)"""
    
    list_params, file_name = get_params(2)          
    print(len(list_params))
    counter = 0
    for p in list_params.keys():
        print("________________________________________________")
        print(counter, len(list_params.keys()))
        list_elem = list_params[p]
        list_res = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            for elem, res in zip(list_elem, executor.map(find_opt_values_bjmm_3LV, list_elem)):
                try:
                    list_res.append(res)
                except Exception as e:
                    print(e, elem)
        counter+=1
        list_params[p] = list_res
        update_params(file_name, list_params)  
if __name__ == '__main__':
    main()  



print(create_d_set(127,7))