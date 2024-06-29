from random import *
from lsh import find_best_lsh_solver
from funs import *

import os  
import json  
from math import*
#   bjmm_depth_m(p, n, k, z, depth, l, set_, u, list_epsilon, list_delta , prob)
def bjmm_depth_3(p, z, dim_set, zD, alpha_D, alpha_E , beta, n, k, depth, l, set_, w0, epsilon1, epsilon2,  delta1, delta2, prob):
    not_failed = True      
    res_naive={} 
    res_lsh={}
    num_solutions = 1+(dim_set**n)*(p**(k-n))
    
    bqsf = ((n-k-l)**2)*(n+1)*((ceil(log(p,2))+ceil(log(p,2))**2)) 
    
    lsh_details = {}
    #pesi 1
    wa = ceil(w0/2)+epsilon1
    wb = floor(w0/2)+epsilon1
    
    #delta1
    
    #pesi 2
    
    wa1= ceil(wa/2)+epsilon2#+d1
    wa2 = floor(wa/2)+epsilon2#+d2
    
    wb1= ceil(wb/2)+epsilon2#+d1
    wb2 = floor(wb/2)+epsilon2#+d2
    
    d1 = ceil(delta1/2)+delta2
    d2 = floor(delta1/2)+delta2
    
    #pesi 3
    
    db1 = ceil(d1/2)
    db2 = floor(d2/2)
    
    w_base1= ceil(wa1/2)#+db1
    w_base2= floor(wa1/2)#+db2
    
    w_base3= ceil(wa2/2)#+db1
    w_base4= floor(wa2/2)#+db2
    
    w_base5= ceil(wb1/2)#+db1
    w_base6= floor(wb1/2)#+db2
    
    w_base7= ceil(wb2/2)#+db1
    w_base8= floor(wb2/2)#+db2
    
    try:
              #compute_representation(dim_set, z, k, l, u0, u1,  epsilon,  alpha_E, delta,  alpha_D, d0, d1,   beta)
        rep1 = compute_representation(dim_set, z, k, l, wa, wa1, epsilon1, alpha_E, delta1, alpha_D, 0, delta1, beta)
        rep2 = compute_representation(dim_set, z, k, l, wa, wa1, epsilon1, alpha_E, delta1, alpha_D, delta1, d1, beta)
        
        ell_0 = l - round(log(rep1, p))
        ell_1 = round(log(rep1, p))-round(log(rep2, p))
        ell_2 = round(log(rep2, p))
    except:
        not_failed = False  
        ell_2 = 0    
        ell_1 = 0
        ell_0 = 0
        
    if ell_0>0 and ell_1>0 and ell_1+ell_0==l:
        #LEVEL 2
        list_b1 = (comb(ceil((k+l)/2), w_base1+db1)*comb(w_base1+db1, w_base1)*(z**w_base1)*(zD**db1))
        list_b2 = (comb(floor((k+l)/2), w_base2+db2)*comb(w_base2+db2, w_base2)*(z**w_base2)*(zD**db2))
        list_b3 = (comb(ceil((k+l)/2), w_base3+db1)*comb(w_base3+db1, w_base3)*(z**w_base3)*(zD**db1))
        list_b4 = (comb(floor((k+l)/2), w_base4+db2)*comb(w_base4+db2, w_base4)*(z**w_base4)*(zD**db2))
        list_b5 = (comb(ceil((k+l)/2), w_base5+db1)*comb(w_base1+db1, w_base5)*(z**w_base5)*(zD**db1))
        list_b6 = (comb(floor((k+l)/2), w_base6+db1)*comb(w_base1+db1, w_base6)*(z**w_base6)*(zD**db2))
        list_b7 = (comb(ceil((k+l)/2), w_base7+db1)*comb(w_base1+db1, w_base7)*(z**w_base7)*(zD**db1))
        list_b8 = (comb(floor((k+l)/2), w_base8+db1)*comb(w_base1+db1, w_base8)*(z**w_base8)*(zD**db2))
        
        memory_cost_2 = compute_memory_cost(list_b2, w_base1, db2, z, zD)
        
        cost_a1, list_a1 = merge_list_cost(p, l, list_b1, list_b2, k, ell_2, w_base1, w_base2, db1, db2)
        cost_a2, list_a2 = merge_list_cost(p, l, list_b3, list_b4, k, ell_2, w_base3, w_base4, db1, db2)
        cost_b1, list_b1 = merge_list_cost(p, l, list_b5, list_b6, k, ell_2, w_base5, w_base6, db1, db2)
        cost_b2, list_b2 = merge_list_cost(p, l, list_b7, list_b8, k, ell_2, w_base7, w_base8, db1, db2)
        
        cost_2 = cost_a1+cost_a2+cost_b1+cost_b2
        
        #LEVEL 1
        list_a1 = min((comb(k+l, wa1+d1)*comb(wa1+d1, wa1)*(z**wa1)*(zD**d1))/(p**ell_2),list_a1)
        list_a2 = min((comb(k+l, wa2+d2)*comb( wa2+d2, wa2)*(z**wa2)*(zD**d2))/(p**ell_2),list_a2)
        list_b1 = min((comb(k+l, wb1+d1)*comb(wb1+d1, wb1)*(z**wb1)*(zD**d1))/(p**ell_2),list_b1)
        list_b2 = min((comb(k+l, wb2+d2)*comb(wb2+d2, wb2)*(z**wb2)*(zD**d2))/(p**ell_2),list_b2)

        memory_cost_1 = compute_memory_cost(list_a2, wa2, d2, z, zD)
        
        cost_a, list_a = merge_list_cost(p, l, list_a1, list_a2, k, ell_1, wa1, wa2, d1, d2)
        cost_b, list_b = merge_list_cost(p, l, list_b1, list_b2, k, ell_1, wb1, wb2, d1, d2)
        
        cost_1 = cost_a+cost_b
        #LEVEL 0
        list_a = min((comb(k+l, (wa+delta1))*comb((wa+delta1), wa)*(z**wa)*(zD**delta1))/(p**(ell_1+ell_2)), list_a)
        list_b = min((comb(k+l, (wb+delta1))*comb((wb+delta1), wb)*(z**wb)*(zD**delta1))/(p**(ell_1+ell_2)), list_b)
        
        memory_cost_0 = compute_memory_cost(list_b, wb, delta1, z, zD)
        cost_0, output_list = merge_list_cost(p, l, list_a, list_b, k, ell_0, wa, wb, delta1, delta1)
        
        lsh_details, cost_0_lsh, memory_cost_0_lsh = find_best_lsh_solver(p, k, l, w0, epsilon1, delta1, wa, wb, list_a, list_b, ell_0, memory_cost_0)

        overall_cost_naive = ((((bqsf+cost_2+cost_1+cost_0)/num_solutions)*log(max(memory_cost_2, memory_cost_1, memory_cost_0),2))/prob)
        overall_cost_lsh = ((((bqsf+cost_2+cost_1+cost_0_lsh)/num_solutions)*log(max(memory_cost_2, memory_cost_1, memory_cost_0_lsh),2))/prob)
        
        res_naive = results(p, n, k, z, depth, "naive", set_, l, w0, epsilon1, delta1, {"0":ell_0, "1": ell_1, "2": ell_2}, {"2":list_b1, "1":list_a1, "0":list_a}, {}, prob, max(memory_cost_1, memory_cost_0), {"BQSF":bqsf, "2": max(cost_a1,cost_a2,cost_b1,cost_b2), "1": max(cost_a, cost_b), "0":cost_0}, overall_cost_naive)
        res_lsh = results(p, n, k, z, depth, "lsh", set_, l, w0, epsilon1, delta1, {"0":ell_0, "1": ell_1, "2": ell_2}, {"2":list_b1, "1":list_a1, "0":list_a},  lsh_details, prob, max(memory_cost_1, memory_cost_0_lsh), {"BQSF":bqsf, "2": max(cost_a1,cost_a2,cost_b1,cost_b2), "1": max(cost_a, cost_b), "0":cost_0_lsh}, overall_cost_lsh)

    else:
        not_failed = False
    
    return not_failed, res_lsh, res_naive

def evaluator(p, n, u, k, z, min_l, max_l, depth, set_):
    w = int(n*u)
    z, dim_set, zD, alpha_D, alpha_E, beta = compute_dim_sets(p,z,set_)
    print(z, dim_set, zD, alpha_D, alpha_E, beta)
    for l in range(min_l, max_l+1):
        if u==1 and not "shifted" in set_:
            min_w0 = k+l
            max_w0 = k+l+1
        else:
            min_w0 = 6
            max_w0 = min(w, k+l+1)

        list_plot_naive=[]
        list_plot_lsh=[]
        for wt in range(min_w0, max_w0):
            
            if u<1:
                prob = ((comb(n-k-l, w-wt)*comb(k+l,wt))) / (comb(n,w))
            elif "shifted" in set_:
                prob = (comb(k+l, wt)*((z)**wt))/(dim_set**(k+l))
            else:
                prob = 1
            
            if  (z==2 and u==1) or "shifted" in set_: max_epsilon1 = 0
            else: max_epsilon1 = floor(wt/2)
            
            for epsilon1 in (0, max_epsilon1+1):
                
                if  (z==2 and u==1) or "shifted" in set_: max_epsilon2 = 0
                else: max_epsilon2 =  (wt/8) + (epsilon1/4) 
                
                for epsilon2 in (0, max_epsilon2+1):
                    
                    if "D" in set_: max_delta1 = (floor(wt/2))-epsilon1
                    else: max_delta1 = 0
                
                    for delta1 in range(0, max_delta1+1):
                        
                        if "D" in set_: max_delta2 = (floor(wt/4)+floor(epsilon1/2))-epsilon2
                        else: max_delta2 = 0
                        
                        for delta2 in range(0, max_delta2+1):

                            not_failed, res_lsh, res_naive = bjmm_depth_3(p, z, dim_set, zD, alpha_D, alpha_E , beta, n, k, depth, l, set_, wt, epsilon1, epsilon2,  delta1, delta2, prob)
                            if not_failed:
                                list_plot_lsh.append(res_lsh)
                                list_plot_naive.append(res_naive)
                            print(l, "on", max_l, wt, "on", max_w0, not_failed)
                    
        update_res(dim_set, list_plot_naive, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_naive")
        update_res(dim_set, list_plot_lsh, str(depth)+"-depth bjmm"+"_"+set_+"_"+str(z)+"_n_"+str(n)+"_lsh")        


def update_res(z, data, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    complete_path = os.path.join(path, 'results_'+z)
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
depth_3 = 3
base_name = "-depth bjmm"

#
#evaluator(p, n, u, k, z, 5, 30, depth_3, set_E)

evaluator(p, n, 1, k, z, 5, 30, depth_3, set_EuD_S)
#evaluator(p, n, u, k, z, 1, n-k, depth_3, set_EuD)

#########################################Z=7#########################################
z = 4
p = 197
n = 384
r = int(0.5*n)
w = 0.34
evaluator(p, n, w, k, z, 1, 10, depth_2, set_EuD)

z = 4
p = 197
n = 384
r = int(0.5*n)
w = 0.34
evaluator(p, n, w, k, z, 1, 20, depth_2, set_EuD)

z = 2
p = 32749
n = 500 
k = int(167*0.75)
w = 0.13
evaluator(p, n, w, 1, 20, depth_2, set_EuD)
