from random import *
from lsh import find_best_lsh_solver
from funs import *

import os  
import json  
from math import*
#   bjmm_depth_m(p, n, k, z, depth, l, set_, u, list_epsilon, list_delta , prob)
def stern(p, z, dim_set, zD, n, k, l, w0):

    num_solutions = 1+(dim_set**n)*(p**(k-n))
    
    bqsf = ((n-k-l)**2)*(n+1)*((ceil(log(p,2))+ceil(log(p,2))**2)) 
    
    wa = ceil(w0/2)
    wb = floor(w0/2)
    list_a = comb(ceil((k+l)/2), wa)*(z**wa)
    list_b = comb(floor((k+l)/2), wb)*(z**wb)
    memory_cost= compute_memory_cost(list_b, wb, 0, z, zD)
    cost, ouput = merge_list_cost(p, l, list_a, list_b, k, l, wa, wb, 0, 0)
    overall_cost = ((bqsf+cost)/num_solutions)*log(memory_cost,2)
    
    return {"Params":{"l":l}, "Overall cost": log(overall_cost,2)}


def evaluator(p, n, u, k, z, set_):
    list_plot=[]
    z, dim_set, zD, alpha_D, alpha_E, beta = compute_dim_sets(p,z,set_)
    for l in range(4, n-k+1):
        w = int((k+l)*u)
        res = stern(p, z, dim_set, zD, n, k, l, w)
        list_plot.append(res)

    update_res(dim_set, list_plot, "stern")


def update_res(z, data, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'results_'+str(z))
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
evaluator(p, n, u, k, z, set_E)
