from random import *
from lsh import find_best_lsh_solver
from funs import *

import os  
import json  
from math import*
#   bjmm_depth_m(p, n, k, z, depth, l, set_, u, list_epsilon, list_delta , prob)
def bjmm_depth_2(p, z, dim_set, zD, alpha_D, alpha_E , beta, n, k, depth, l, set_, w0, epsilon, delta, prob):
    not_failed = True      
    res_naive={} 
    res_lsh={}
    num_solutions = 1+(dim_set**n)*(p**(k-n))
    
    bqsf = ((n-k-l)**2)*(n+1)*((ceil(log(p,2))+ceil(log(p,2))**2)) 
    
    lsh_details = {}
    
    wa = ceil(w0/2)+epsilon
    wb = floor(w0/2)+epsilon
   
    wa1= ceil(wa/2)
    wa2 = floor(wa/2)
    
    wb1= ceil(wb/2)
    wb2 = floor(wb/2)
    
    d1 = ceil(delta/2)
    d2 = floor(delta/2)
    try:     
        rep = compute_representation_0(dim_set, z, k, l, w0, wa, epsilon, alpha_E, delta, alpha_D, 0, delta, beta)
        ell_1 = round(log(rep, p))
        ell_0 = l-ell_1
    except:
        not_failed = False      
        ell_1 =0
        ell_0 =0
        
    if ell_0>0 and ell_1>0 and ell_1+ell_0==l:
        list_a1 = (comb(ceil((k+l)/2), wa1+d1)*comb(wa1+d1, wa1)*(z**wa1)*(zD**d1))
        list_a2 = (comb(floor((k+l)/2), wa2+d2)*comb( wa2+d2, wa2)*(z**wa2)*(zD**d2))
        list_b1 = (comb(ceil((k+l)/2), wb1+d1)*comb(wb1+d1, wb1)*(z**wb1)*(zD**d1))
        list_b2 = (comb(floor((k+l)/2), wb2+d2)*comb(wb2+d2, wb2)*(z**wb2)*(zD**d2))

        memory_cost_1 = compute_memory_cost(list_a2, wa2, d2, z, zD)
        cost_a, output_list_a = merge_list_cost(p, l, list_a1, list_a2, k, ell_1, wa1, wa2, d1, d2)
        cost_b, output_list_b = merge_list_cost(p, l, list_b1, list_b2, k, ell_1, wb1, wb2, d1, d2)
        
        list_a = min((comb(k+l, (wa+delta))*comb((wa+delta), wa)*(z**wa)*(zD**delta))/(p**(ell_1)), output_list_a)
        list_b = min((comb(k+l, (wb+delta))*comb((wb+delta), wb)*(z**wb)*(zD**delta))/(p**(ell_1)), output_list_b)
        
        memory_cost_0 = compute_memory_cost(list_b, wb, delta, z, zD)
        cost_0, output_list_a = merge_list_cost(p, l, list_a, list_b, k, ell_0, wa, wb, delta, delta)
        
        lsh_details, cost_0_lsh, memory_cost_0_lsh = find_best_lsh_solver(p, k, l, w0, epsilon, delta, wa, wb, list_a, list_b, ell_0, memory_cost_0)

        overall_cost_naive = ((((bqsf+cost_a+cost_b+cost_0)/num_solutions)*log(max(memory_cost_1, memory_cost_0),2))/prob)
        overall_cost_lsh = ((((bqsf+cost_a+cost_b+cost_0_lsh)/num_solutions)*log(max(memory_cost_1, memory_cost_0_lsh),2))/prob)
        res_naive = results(p, n, k, z, depth, "naive", set_, l, w0, epsilon, delta, {"0":ell_0, "1": ell_1}, {"1":list_a1, "0":list_a}, {}, prob, max(memory_cost_1, memory_cost_0), {"BQSF":bqsf, "1": max(cost_a, cost_b), "0":cost_0}, overall_cost_naive)
        res_lsh = results(p, n, k, z, depth, "lsh", set_, l, w0, epsilon, delta, {"0":ell_0, "1": ell_1}, {"1":list_a1, "0":list_a},  lsh_details, prob, max(memory_cost_1, memory_cost_0_lsh), {"BQSF":bqsf, "1": max(cost_a, cost_b), "0":cost_0_lsh}, overall_cost_lsh)

    else:
        not_failed = False
    
    return not_failed, res_lsh, res_naive


def evaluator(p, n, u, k, z, min_l, max_l, depth, set_):
    w = int(n*u)
    z, dim_set, zD, alpha_D, alpha_E, beta = compute_dim_sets(p,z,set_)
    for l in range(min_l, max_l+1):
        if u==1 and not "shifted" in set_:
            min_w0 = k+l
            max_w0 = k+l+1
        else:
            min_w0 = 1
            max_w0 = min(w, k+l+1)

        
         
            
        list_plot_naive=[]
        list_plot_lsh=[]
        for wt in range(min_w0, max_w0):

            if  (z==2 and u==1) or "shifted" in set_: max_epsilon = 0
            else: max_epsilon = floor(wt/4)
            if u<1:
                prob = ((comb(n-k-l, w-wt)*comb(k+l,wt))) / (comb(n,w))
            elif "shifted" in set_:
                prob = (comb(k+l, wt)*((z)**wt))/(dim_set**(k+l))
            else:
                prob = 1    
            for epsilon in range(0, max_epsilon+1):
                
                if "D" in set_: max_delta = (round(wt/2))-2*epsilon
                else: max_delta = 0
                for delta in range(0, max_delta+1):                        
                    not_failed, res_lsh, res_naive = bjmm_depth_2(p, z, dim_set, zD, alpha_D, alpha_E, beta, n, k, depth, l, set_, wt, epsilon, delta, prob)
                    
                    if not_failed:
                        list_plot_lsh.append(res_lsh)
                        list_plot_naive.append(res_naive)
                        
                        #print("sy", l, "on", max_l, "w", wt, "on", max_w0, "eps", epsilon, "on", max_epsilon, "del", delta, "on", max_delta,  res_lsh["Overall cost"] - res_naive["Overall cost"]<10, round(res_lsh["Overall cost"]), round(res_naive["Overall cost"]))
                        print("sy", l, "on", max_l, "w", wt, "on", max_w0, "eps", epsilon, "on", max_epsilon, "del", delta, "on", max_delta, round(res_lsh["Overall cost"]))

        #update_res(dim_set, list_plot_naive, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_naive")
        update_res(dim_set, list_plot_lsh, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_lsh")        


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

#
#evaluator(p, n, u, k, z, 1, n-k, depth_2, set_E)

#evaluator(p, n, u, k, z, 39, n-k, depth_2, set_EuD)
#evaluator(p, n, 1, k, z, 34, n-k, depth_2, set_EuD_S)

#########################################Z=4#########################################
z = 4
p = 197
n = 384
r = 0.5
w = 0.34
k = int(r*n)
evaluator(p, n, w, k, z, 23, 23, depth_2, set_EuD)
"""l": 23,
            "w0": 48,
            "epsilon": 4,
            "delta": 1,"""
z = 4
r = 0.2
w = 0.6
p = 137
n = 384
k = int(r*n)
#evaluator(p, n, w, k, z, 1, n-k, depth_2, set_EuD)

z = 2
p = 16381
n = 500 
r = 0.75
w = 0.16
k = int(r*n)
#evaluator(p, n, w, k, z, 1, n-k, depth_2, set_EuD)

z = 2
p = 16381
n = 500 
r = 0.75
w = 0.16
k = int(r*n)
#evaluator(p, n, w, k, z, 1, n-k, depth_2, set_EuD)

z = 2
p = 32749
n = 500 
r = 0.75
w = 0.13
k = int(r*n)
#evaluator(p, n, w, k, z, 1, n-k, depth_2, set_EuD)