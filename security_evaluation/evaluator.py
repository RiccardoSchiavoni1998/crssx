from bjmmM import bjmm_depth_m
import os  
import json  
from math import*

def bjmm(p, n, u, k, z, min_l, max_l, depth, set_):
    w = int(n*u)
    print("Start", "Bjmm 2lv on set ", set_, "on Params:", p, n, k, z)
    #w=int(n*u)
    for l in range(min_l, max_l+1):
        list_plot_naive=[]
        list_plot_lsh=[]
        if u==1:
            if "shifted" in set_:
                min_w0 = 1
                max_w0 = min(w, k+l+1)
            else:
                min_w0 = k+l
                max_w0 = k+l+1
        else:
            min_w0 = 2
            max_w0 = min(11, w, k+l+1)
        for wt in range(min_w0, max_w0): 
            if z==2 and u==1:#or
                ranges_epsilon = [{"0":0, "1": 0, "2":0}]
            else:    
                ranges_epsilon = creates_dinamic_ranges_epsilon(round((k+l)/2), set_)
            
            for list_epsilon in ranges_epsilon:
                
                if "D" in set_:
                    ranges_delta = creates_dinamic_ranges_delta(round((k+l)/2)-list_epsilon['1'], set_)
                else: 
                    ranges_delta = [{"0":0, "1": 0, "2":0}]
                    
                for list_delta in ranges_delta:
                    if  u==1:
                        if "shifted" in set_:
                            prob = (comb(k+l, wt)*((z-1)**wt))/(z**(k+l))
                        else:
                            prob = 1
                    else:
                        prob = (comb(n-k-l, w-wt)*comb(k+l,wt)) / (comb(n,w))
                    not_failed, res_lsh, res_naive = bjmm_depth_m(p, n, k, z, depth, l, set_, wt, list_epsilon, list_delta , prob)
                    if not_failed:
                        list_plot_lsh.append(res_lsh)
                        list_plot_naive.append(res_naive)
                        
        update_res(list_plot_naive, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_naive")
        update_res(list_plot_lsh, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_lsh")        
        
def creates_dinamic_ranges_epsilon(range_max1, set_):
    list_ovlp = []
    if "shifted" in set_:
        list_ovlp.append({"0":0, "1":0, "2":0})
    else:
        for i in range(0, range_max1):
            list_ovlp.append({"0":0, "1":i, "2":0})
    return list_ovlp

def creates_dinamic_ranges_delta(range_max1, set_):
    list_ovlp = []
    if not("D" in set_):
        list_ovlp.append({"0":0, "1":0, "2":0})
    else:
        for i in range(0, range_max1):
            list_ovlp.append({"0":0, "1":i, "2":0})
    return list_ovlp

    

def update_res(data, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'results')
    if not os.path.exists(complete_path):
        os.makedirs(complete_path)
    complete_path = os.path.join(complete_path, file_name)
    if os.path.exists(complete_path):
        print(f"Il file {file_name} esiste già. Aggiunta dei dati.")
        with open(complete_path, 'r') as file:
            existing_data = json.load(file)
        
        if isinstance(existing_data, list):
            existing_data.extend(data)
        else:
            existing_data.update(data)
        
        with open(complete_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        print(f"Il file {file_name} non esiste e verrà creato.")
        with open(complete_path, 'w') as file:
            json.dump(data, file, indent=4)
        

#########################################Z=7#########################################
p = 127
n = 127
k = 76
z = 7
u = 1
current_best = 200

set_E="E"
set_E_S="shifted_E"
set_EuD="EuD"
set_EuD_S="shifted_EuD"
mode_naive="BF"
mode_NN_Bin="NN_Bin"
mode_NN_Restr="NN_Restr"
depth_2 = 2
#depth_3 = 3
base_name = "-depth bjmm"

#bjmm(p, n, u, k, z, 1, n-k, depth_2, set_EuD)
bjmm(p, n, 1, k, z, depth_2, set_E)
#bjmm(p, n, 1, k, z, 10, 20, depth_2, set_EuD_S)
#########################################Z=7#########################################
