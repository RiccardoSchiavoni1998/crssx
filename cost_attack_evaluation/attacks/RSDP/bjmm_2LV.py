from IPython.display import clear_output
from math import *
from attacks.RSDP.funs.utils_2LV import *
from attacks.RSDP.funs.nearest_neighbour import *
"""
from funs.utils_2LV import *
from funs.nearest_neighbour import *"""
import os

def clear_terminal():
    # Controllo del sistema operativo
    if os.name == 'nt':  # Windows
        _ = os.system('cls')
    else:  # Mac o Linux
        _ = os.system('clear')

def cost_evaluator_bf(p, n, k, z, l, current_best, w0, e=0):
    
    res = {}
    
    len_vb_1, len_vb_2, w1, w2, w1_1, w1_2, w2_1, w2_2 = compute_params(k+l, w0, e)
    
    rep = compute_n_reps(w0, w2, e)
   
    t = round(log(rep, p))
    
    if t>0 and l>t:
        num_solution = 1+(7**n)*(p**(k-n))
        
        prob = (comb(k+l, w0)*((z)**w0))/(7**(k+l))
        
        max_list_size, c_base, c_lv1, list_a, list_b, num_r0 = compute_partial_costs(p, l, t, len_vb_1, len_vb_2, w1_1, w1_2, w2_1, w2_2, z)
        memory_cost = compute_memory_cost(len_vb_1, len_vb_2, w1_1, w1_2, w2_1, w2_2, list_a, list_b, w1, w2, z)
        c_0 = ((list_a*list_b)/num_r0)*log(p,2)
        
        total_cost = log((((c_base+c_lv1+c_0)/num_solution)*log(memory_cost,2))/prob,2)
        
        if e==0 and w0==k+l:
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":w0}
        else:
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "e":e}
        res['Overall Cost'] = total_cost
            
        details = {}
            
        details['Number of representation'] = {'q**t':log(rep,2), 'q**(l-t)': log(num_r0, 2)}

        details['Memory Cost'] = log(memory_cost,2)
        
        res['Time Cost'] = {'Base Time Cost':log(c_base, 2), 'Level 1 Time Cost':log(c_lv1, 2), 'Level 0 Cost':log(c_0, 2)}
        
        details['List Size'] = {'Base List': log(max_list_size,2), 'Lv1 Lists': log(max(list_a, list_b),2)}
        
        res["Details"] = details
        
        current_best = total_cost

    return res, current_best

def cost_evaluator_nn(p, n, k, z, l, current_best, w0, find_best_nn, e=0):
    
    res = {}
    
    len_vb_1, len_vb_2, w1, w2, w1_1, w1_2, w2_1, w2_2 = compute_params(k+l, w0, e)
    
    rep = compute_n_reps(w0, w2, e)
    
    t = log(rep, p)
    
    if t>0 and l>t and w1_1>0 and w1_2>0 and w2_1>0 and w2_2>0:
        num_solution = 1+(7**n)*(p**(k-n))
       
        prob = (comb(k+l, w0)*((z)**w0))/(7**(k+l))
        
        max_list_size, c_base, c_lv1, list_a, list_b, num_r0 = compute_partial_costs(p, l, t, len_vb_1, len_vb_2, w1_1, w1_2, w2_1, w2_2, z)
        
        red_l1 = list_a/num_r0
        red_l2 = list_b/num_r0
        
        memory_cost = compute_memory_cost(len_vb_1, len_vb_2, w1_1, w1_2, w2_1, w2_2, red_l1, red_l2, w1, w2, z)
        
        partial_cost = log((((c_base+c_lv1+num_r0)/num_solution)*log(memory_cost,2))/prob,2)
        
        if partial_cost <= current_best:
            
            nn_costs, min_cost = find_best_nn(k, l, e, w1, w2, red_l1, red_l2, current_best)
            
            total_cost = log((((c_base+c_lv1+num_r0*min_cost)/num_solution)*log(memory_cost,2))/prob,2)
            
            if total_cost <= current_best and len(nn_costs)>0:
                if e==0 and w0==k+l:
                    res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":w0}
                else:
                    res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "e":e}
                
                res['Overall Cost'] = total_cost
               
                details = {}
                    
                details['Number of representation'] = {'q**t':log(rep,2), 'q**(l-t)': log(num_r0, 2)}
        
                details['Memory Cost'] = log(memory_cost,2)
                
                details['List Size'] = {'Base List': log(max_list_size,2), 'Lv1 Lists': log(max(list_a, list_b),2), 'Reduced Lists (Input NN) Size ':  log(max(red_l1, red_l2),2)}
               
                details['Time Cost'] = {'Base Time Cost':log(c_base, 2), 'Level 1 Time Cost':log(c_lv1, 2), 'Num Iteration':  log(num_r0, 2), 'Level 0 Cost (Nearest Neighbouor)':log(min_cost, 2)}
                
                res["Details"] = details
                
                nn_details = []
                for nn_cost in nn_costs:
                    nn_details.append(nn_cost)
                res['NN Details'] = nn_details
                
                current_best = total_cost
    return res, current_best

def bjmm_2lv_E(p, n, k, z, evaluator, mode, current_best, sec_level = 999):
    #BRUTE FORCE
    #current_best = n+40
    list_cost=[]
    
    for l in range(1, (n-k)+1):
        clear_output(wait=True)
        #print("l", l, " on", n-k)
        w0=k+l
        for e in range(1, 6):
            #clear_terminal()
            #print("2LVE", mode, p, n, k, z,"::", l, e, "on", n-k, 5)
            if mode == "nn":
                res_details, total_cost = evaluator(p, n, k, z, l, current_best, w0, find_best_nn, e=e)
            else:
                res_details, total_cost = evaluator(p, n, k, z, l, current_best, w0, e=e)
            
            if res_details != {} and total_cost<=current_best:
                if total_cost < sec_level:
                    return total_cost, [], False
                current_best = total_cost
                list_cost.append(res_details)
    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    return current_best, list_cost, True   
   
def bjmm_2lv_shifted(p, n, k, z, evaluator, mode, current_best, sec_level = 999):

    list_cost=[]
    
    for l in range(1, (n-k)+1):
        clear_output(wait=True)
        for w0 in range(1, (k+l)+1):
            if mode == "nn":
                res_details, total_cost = evaluator(p, n, k, z, l, current_best, w0, find_best_nn)
            else:
                res_details, total_cost = evaluator(p, n, k, z, l, current_best, w0)
            
            if res_details!={} and total_cost<=current_best:
                    
                if total_cost < sec_level:
                    return total_cost, [], False
                current_best = total_cost
                list_cost.append(res_details)

    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    return current_best, list_cost, True 

def bjmm_2LV_opt_size_pk(p, n, k, z, current_best, sec_level):
    data = {"BF on Set E":"", "NN on Set E":"", "BF on Shifted Set":"", "NN on Shifted Set":""}
    safe = False
    
    print("inizio 2 S bf", p, n, k, z-1)
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_2lv_shifted(p, n, k, z-1, cost_evaluator_bf, "bf", current_best, sec_level)
    print("finito 2 S bf", p, n, k, z-1, res_S_bf, current_best_S_BF)
    data["BF on Shifted Set"] = current_best_S_BF 
    if res_S_bf:
        
        print("inizio 2 S nn", p, n, k, z-1)
        current_best_S_NN, data_S_nn, res_S_nn = bjmm_2lv_shifted(p, n, k, z-1, cost_evaluator_nn, "nn", current_best_S_BF, sec_level)
        data["NN on Shifted Set"] = current_best_S_NN
        print("finito 2 S nn" , p, n, k, z-1, res_S_nn, current_best_S_NN)
        if res_S_nn:
            
            print("inizio 2 E nn", p, n, k, z)
            current_best_E_NN, data_E_nn, res_E_nn = bjmm_2lv_E(p, n, k, z, cost_evaluator_nn, "nn", current_best_S_NN, sec_level)
            data["NN on Set E"] = current_best_E_NN
            print("finito 2 E NNV" , p, n, k, z, res_S_bf, current_best_E_NN)
            if res_E_nn:    
                
                print("inizio 2 E bf", p, n, k, z)
                current_best_E_BF, data_E_bf, res_E_bf = bjmm_2lv_E(p, n, k, z, cost_evaluator_bf, "bf", current_best_E_NN, sec_level)
                data["BF on Set E"] = current_best_E_BF
                print("finito 2 E BF" , p, n, k, z, res_S_bf, current_best_E_BF)
                
                if res_S_nn:
                    safe = True
    #print(safe)
    return safe, data

"""
def bjmm_2LV(p, n, k, z):
    data = {}
    safe = False
    data_E_nn, res_E_nn = bjmm_2lv_E(p, n, k, z, cost_evaluator_nn, "nn")
    print("finito 2 E nn" , p, n, k, z, res_E_nn)
    if res_E_nn:
        data_S_nn, res_S_nn = bjmm_2lv_shifted(p, n, k, z-1, cost_evaluator_nn, "nn")
        print("#finito 2 S nn" , p, n, k, z, res_S_nn)
        if res_S_nn:
            safe = True
            #data["BF on Set E"] = data_E_bf
            data["NN on Set E"] = data_E_nn
            #data["BF on Shifted Set"] = data_S_bf 
            data["NN on Shifted Set"] = data_S_nn
    print(safe)
    return safe, data
"""
    
