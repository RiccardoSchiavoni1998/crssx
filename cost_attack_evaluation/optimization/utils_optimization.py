################################################################# SET DEPENDENCES AND GLOBAL PARAMS #################################################################

import os
import json
import concurrent.futures
from math import *
from sympy import isprime
from attacks.RSDP.stern import stern_opt_size_pk

def get_global_vars():
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'opt_config.json')

    # Carica il file JSON
    with open(complete_path, "r") as file:
        global_params = json.load(file)

    #DEFINE GLOBAL VARS
    min_p = global_params['ranges']['p_min']
    max_p = global_params['ranges']['p_max']
    min_n = global_params['ranges']['n_min']
    max_n = global_params['ranges']['n_max']
    rates = global_params['ranges']['rates']
    ranges = {**global_params["rangeSetE2"], **global_params["rangeSetShiftedE2"]}
    category = global_params['currentCategory']
    security_level = global_params['paramsCategory'+str(category)]['security_level']
    [n_,p_,z_] = global_params['paramsCategory'+str(category)]['target_size']
    target_size = n_*log(p_*z_,2)
    directory_name= global_params["files"]["dir"]
    name = global_params["files"]["name"]
    verb = global_params["verb"]
    fast = global_params["fast"]
    num_workers = global_params["num_workers"]
    list_attacks = global_params["list_attacks"]
    new_execution = global_params["new_execution"]
    recovery_num = global_params["recovery_num"]
    complete_path = os.path.join(path, directory_name)
    if not os.path.exists(complete_path):
        os.makedirs(complete_path)

    current_attack="" 
    return min_p, max_p, min_n, max_n, rates, ranges, security_level, target_size, name, verb, fast, num_workers, list_attacks, new_execution, recovery_num, current_attack, path, directory_name

min_p, max_p, min_n, max_n, rates, ranges, security_level, target_size, name, verb, fast, num_workers, list_attacks, new_execution, recovery_num, current_attack, path, directory_name = get_global_vars()

if fast:
    from attacks.RSDP.bjmm_2LV_fast import bjmm_2LV_opt_size_pk
    from attacks.RSDP.bjmm_3LV_fast import bjmm_3LV_opt_size_pk
else:
    from attacks.RSDP.bjmm_2LV_detailed import bjmm_2LV_opt_size_pk
    from attacks.RSDP.bjmm_3LV_detailed import bjmm_3LV_opt_size_pk


################################################################################## UTILIS ################################################################################

def get_p_values(min_p, max_p):
    list_p = []
    for p in range(min_p, max_p+1):
        if isprime(p):
            list_p.append(p)
    return list_p

def get_z_values(p):
    return [7]
    """
    list_z = []
    for z in range(3, p):
        if (p-1)%z == 0:
            list_z.append(z)
    return list_z"""
    
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

def get_data(file_name):
    file_name = directory_name+"/"+file_name
    complete_path = os.path.join(path, file_name)
    with open(complete_path, "r") as file:
        data = json.load(file)
    return data
        
def update_data(file_name, data):
    file_name = directory_name+"/"+str(file_name)
    
    complete_path = os.path.join(path, file_name)
    
    with open(complete_path, "w") as file:
        json.dump(data, file, indent=4)

def get_min_cost(item):
    list_min = []
    for key in item["Res"].keys():
        min_ = item["Res"][key]
        if type(min_)==list:
            min_ = min(list(filter(lambda v: isinstance(v, (int, float)), min_.values())))
        list_min.append(min_)
    if len(list_min)==0:
        return item["Params"]["n"]+35
    else:
        return min(list_min)

def init_params():
    
    data = {}    
    list_p = get_p_values(min_p, max_p)
    for p in list_p:
        list_elem=[]
        dim_set = get_z_values(p)
        for z in dim_set:
            for n in range(min_n, max_n+1):
                for rate in rates:
                    elem = {}
                    k=int(n*(rate))
                    size =  n*log(z*p, 2)
                    if size<=target_size:#keep only the combo with a size lower than 128*log(7*128, 2)
                        elem["Params"] = {"n":n, "k":k, "z":z, "p":p}
                        elem["Size"] = size
                        elem["Failed"] = False
                        elem["Res"] = {}
                        
                        list_elem.append(elem)
                        
        data[p]={"State":"To Do", "Evaluations":list_elem}
        
    file_name = name+"_0.json"
    
    update_data(file_name, data)
    
    return data, file_name

def get_params(iter, flag):
    #Take both the files of the last and the new execution
    old_iter = iter-int(flag) #if it is the first step of a previous execution the 2 files are the same
    data={}
    old_file = name +"_"+str(old_iter)+".json"
    new_file = name +"_"+str(iter)+".json"
    try:
        data = get_data(old_file) 
        for p in data.keys():
            values = data[p]["Evaluations"]
            values = list(filter(lambda item: not(item["Failed"]), values)) #Discaring the failed executions
            values = list(filter(lambda item: get_min_cost(item) < security_level, values)) #Discaring the executions that gives a cost lower than the security level
            if len(values)>0:
                if iter == 3:
                    values = sorted(values, key=lambda x: x["Size"]) #if it is the last execution the results are sorted according the size
                data[p]["Evaluations"] = values
        update_data(new_file, data) 
    except Exception as e:
        print("Problem in data recovering", e)
    return data, new_file

def find_opt_stern(elem):
    
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
   
    safe_s, res = stern_opt_size_pk(p, n, k, z, security_level)
        
    elem["Failed"] = not(safe_s)
    
    elem["Res"]["Stern"] = res
    
    return elem

def find_opt_bjmm2LV(elem):
    
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
   
    safe_s, res = bjmm_2LV_opt_size_pk(p, n, k, z, ranges, get_min_cost(elem), security_level, verb) 
 
    if safe_s:
        elem["Failed"] = True
    
    elem["Res"]["Bjmm 2LV"] = res
    
    return elem

def find_opt_bjmm3LV(elem):
    
    n = elem["Params"]["n"]
    z = elem["Params"]["z"]
    k = elem["Params"]["k"]
    p = elem["Params"]["p"]
   
    safe_s, res = bjmm_3LV_opt_size_pk(p, n, k, z, get_min_cost(elem), security_level, verb)
           
    if safe_s:
        elem["Failed"] = True
    
    elem["Res"]["Bjmm 3LV"] = res
    
    return elem

################################################################################## OPTIMIZATION FUNCTIONS ################################################################################

def optimize():
    #try:
    new_execution_ = new_execution
    for iter in range(recovery_num, len(list_attacks)):
        list_params = [] 
        file_name = ""
        
        #if start from the first attack or if is a new execution 
        if iter == 0 and new_execution_:
            list_params, file_name = init_params() #take all the combination of p,n,k,z
        
        #if it is not the first attack or a previous execution is being taken up 
        else:
            list_params, file_name = get_params(iter, new_execution_)  

        counter = 0
        num_of_p = len(list_params.keys()) #values of p
        
        #SET CURRENT ATTACK
        if list_attacks[iter]=="Stern": find_opt_values = find_opt_stern
        if list_attacks[iter]=="Bjmm 2LV": find_opt_values = find_opt_bjmm2LV
        if list_attacks[iter]=="Bjmm 3LV": find_opt_values = find_opt_bjmm3LV
            
        for p in list_params.keys():
            
            if new_execution_ or list_params[p]["State"] == "To Do":
                
                print(list_attacks[iter], "p:", p, "round:", counter, "on", num_of_p) 
                list_elem = list_params[p]["Evaluations"]
                list_res = []
                
                with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
                    
                    for elem, res in zip(list_elem, executor.map(find_opt_values, list_elem)):
                        try:
                            list_res.append(res)
                        except Exception as e:
                            print(e, elem)
                            
                counter += 1
                list_params[p]["State"] = "Finished"
                list_params[p]["Evaluations"] = list_res
                update_data(file_name, list_params)  
        if not(new_execution_):
            new_execution_ = True
    """        
    except Exception as e:
        print("EH LU SACC", e)"""
    
    
