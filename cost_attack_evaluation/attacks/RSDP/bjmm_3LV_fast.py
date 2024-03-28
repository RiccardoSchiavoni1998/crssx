from IPython.display import clear_output
from math import *
from attacks.RSDP.funs.utils_3LV import *
from attacks.RSDP.funs.nearest_neighbour import find_best_nn
import os

# Utilizzo la funzione per cancellare l'output del terminale

def cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, set_type, current_best, mode):
    res={}       
    flag = False    
    
    succ_prob = comb(k+l,u0)*z**u0 * (7)**(-k-l)
    num_solutions = 1+((7**n)*(p**(k-n)))

    #vector weights level 1
    u1 = round(u0/2)+ε1
    d1 = round(d0/2)+δ1
    
    #vector weights level 2 
    u2 = round(u1/2)+ε2
    d2 = round(d1/2)+δ2
    
    #vector weights level 3 
    u_base = round(u2/2)
    d_base  = round(d2/2)
    
    #compute representations
    try:
        rep_1 = compute_num_rep(u1, u2, d1, alpha_e, alpha_d, δ2, ε2)
        l1 = round(log(rep_1, p))
        
        rep_0 = compute_num_rep(u0, u1, d0, alpha_e, alpha_d, δ1, ε1)
        l0 = round(log(rep_0, p))-l1
        
    except Exception as e:
        rep_1, rep_0, l1, l0 = 0, 0, 0, 0
        ###print((e, l, δ2, ε2, rep_1, δ1, ε1, rep_0)
        
        
    if rep_1==0 or rep_0==0 or l0<=l1 or l-l0-l1<=0:
        return False, 0
    
    
    #______________________________________ LEVEL 3 ______________________________________
    
    len_v_base = round((k+l)/2)
    
    len_list_base = compute_lists_len(len_v_base, p, z, zD, u=u_base, d=d_base)

    if len_list_base<=0:
        return False, 0
    
    memory_cost_base = len_list_base*(u_base*log(z,2)+d_base*(log(zD,2)))
    time_cost_base = compute_time_cost(len_list_base, z, zD, p, u_base, d_base, l1)
    
    #______________________________________ LEVEL 2 ______________________________________
    
    len_v2 = k+l
    len_list_lv2 = compute_lists_len(len_v2, p, z, zD, li=l1, u=u2, d=d2)
    
    if len_list_lv2<=0:
        return False, 0
    
    memory_cost_lv2 = len_list_lv2*(u2*log(z,2)+d2*(log(zD,2)))
    
    time_cost_lv2 = compute_time_cost(len_list_lv2, z, zD, p, u2, d2, l0)
    
    #______________________________________ LEVEL 1 ______________________________________
  
    len_v1 = k+l
    time_cost_lv1 = ((len_list_lv2*len_list_lv2)/(p**(l0)))*log(p,2)  
    len_list_lv1 = compute_lists_len(len_v1, p, z, zD, li=l0+l1, u=u1, d=d1)
   
    #______________________________________ LEVEL 0 ______________________________________
    
    if mode=="NN":
       len_list_lv1 = len_list_lv1/p**(l-l0-l1)
       
    memory_cost_lv1 = len_list_lv1*(u1*log(z,2)+d1*(log(zD,2)))
    memory_cost = log(max(memory_cost_base, memory_cost_lv2, memory_cost_lv1),2)
    
    if mode == "BF":
        #compute base time cost  L1^2 * p^-(l-l0-l1) * log(p,2)
        time_cost_0 = ((len_list_lv1*len_list_lv1)*log(p,2))/(p**(l-l0-l1))
        time_cost = time_cost_base+time_cost_lv2+time_cost_lv1+time_cost_0
        overall_cost = log(((time_cost/num_solutions)*memory_cost)/succ_prob,2)
        if overall_cost<=current_best:
            flag = True
            current_best = overall_cost
    else:
        w1 = u1+d1
        
        #Nearest Neighbour
        partial_cost = log((((time_cost_base+time_cost_lv2+time_cost_lv1+p**(l-l0-l1))/num_solutions)*memory_cost)/succ_prob,2)
        
        if partial_cost < current_best:
            
            #NEAREST NEIGHBOUR
            nn_costs, time_cost_0 = find_best_nn(k, l, ε1 + δ1 + ε2 + δ2, w1, w1, len_list_lv1, len_list_lv1, current_best)
            
            if len(nn_costs)>0:
   
                time_cost = time_cost_base+time_cost_lv2+time_cost_lv1+(time_cost_0*p**(l-l0-l1))
                overall_cost = log(((time_cost/num_solutions)*memory_cost)/succ_prob,2)
                
                if overall_cost<=current_best:
                    flag = True
                    current_best = overall_cost
    
    if flag:
        
        if set_type=="shifted":
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":u0, "delta 1":δ1, "delta 2":δ2}
        else:
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "epsilon 1":ε1, "delta 1":δ1, "epsilon 2":δ1, "delta 2":δ2}
        
        res['Overall Cost'] = overall_cost
    
        details = {}

        details['Number of representation'] = {'l,l0,l1': [l,l0,l1] ,'q**l1':log(p**l1, 2), 'q**(l0-l1)': log(p**(l0-l1), 2), 'q**(l-l0-l1)':log(p**(l-l0-l1),2) }
        
        details["Memory cost"] = log(memory_cost,2)
        
        details['List Size'] = {'Base List': log(len_list_base,2), 'Lv2 Lists':log(len_list_lv2,2), 'Lv1 Lists': log(len_list_lv1,2)}
        
        details['Time Cost'] = {'Base Time Cost':log(time_cost_base, 2), 'Level 2 Time Cost':log(time_cost_lv2, 2), 'Level 1 Time Cost':log(time_cost_lv1, 2), 'Level 0 Cost' : log(time_cost_0, 2)}
            
        details["Success Probability"] = log(succ_prob,2)
        
        res["Details"] = details 
        
        if mode == "NN":
            nn_details = []
            for nn_cost in nn_costs:
                nn_details.append(nn_cost)
            res['NN Details'] = nn_details
    
    
    return res, current_best
      
#SEBASTIAN RANGES
def bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, mode, current_best, sec_level = 999, verb=False):
    
    #current_best = n+40
    if verb: print("Inizio", "Bjmm 3lv on Shifted set", mode, "on Params:", p, n, k, z)
    list_cost = []
    
    for l in range(max(0, n-k-30), n-k+1):

        u0, d0 = (k+l), 0    
        
        max_ε1 = ceil(u0/4)
        
        for ε1 in range(0, max_ε1+1):
            max_ε2 = round( (u0/8) + (ε1/4) ) 
            
            for ε2 in range(0, max_ε2+1):
                max_δ1 = round((u0/2)-ε1)
                
                for δ1 in range(0, min(max_δ1, 17)+1):
                    max_δ2 = round((u0/4)+(ε1/2)-ε2)
                    
                    for δ2 in range(0, min(max_δ2, 9)+1):
                        res_details={} 
                        res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, "E", current_best, mode) #ERWIN
                        
                        if len(res_details) != {} and cost < current_best:
                            if cost < sec_level:
                                if verb: print("End", "Bjmm 3lv on set E", mode, "on Params:", p, n, k, z, "Not Secure")
                                return cost, [], False
                            current_best = cost
                            list_cost.append(res_details)
    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    
    if verb: print("End", "Bjmm 3lv on Shifted set", mode, "on Params:", p, n, k, z, "Secure")
    return current_best, list_cost, True                 

def bjmm_3lv_shifted(p, n, k, z, zD, alpha_e, alpha_d, mode, current_best, sec_level = 999, verb=False):

    #current_best = n+30
    if verb: print("Inizio", "Bjmm 3lv on Shifted set", mode, "on Params:", p, n, k, z)
    list_cost = []
    ### BJMM SHIFTED

    for l in range(max(0, n-k-30), n-k+1):

        d0 = 0
        
        for u0 in range(8, k+l+1):
            
            max_δ1 = min(round(u0/2), 17)
            
            for δ1 in range(0, max_δ1+1):
                
                max_δ2 = min(round(u0/4), 9)
                
                for δ2 in range(0, max_δ2+1):
                    
                    res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, 0, δ1, 0, δ2, alpha_e, alpha_d, "shifted", current_best, mode)
                    
                    if len(res_details) != {} and cost < current_best:
                        if cost < sec_level:
                            if verb: print("End", "Bjmm 3lv on Shifted set", mode, "on Params:", p, n, k, z, "Not Secure")
                            return cost, [], False
                        current_best = cost
                        list_cost.append(res_details)
                        res_details = {}
                        
    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    
    if verb: print("End", "Bjmm 3lv on Shifted set", mode, "on Params:", p, n, k, z, "Secure")
    return current_best, list_cost, True                

def bjmm_3LV_opt_size_pk(p, n, k, z, current_best, sec_level, verb):
    data = {"BF on Set E":"", "NN on Set E":"", "BF on Shifted Set":"", "NN on Shifted Set":""}
    safe = False
    
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1 
    
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d_bf, "bf", current_best, sec_level, verb)
    data["BF on Shifted Set"] = current_best_S_BF

    if res_S_bf:
        
        current_best_S_NN, data_S_nn, res_S_nn = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d_nn, "nn", current_best_S_BF, sec_level, verb)
        data["NN on Shifted Set"] = current_best_S_NN
        
        if res_S_nn:
            
            current_best_E_NN, data_E_nn, res_E_nn = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d_nn, "nn", current_best_S_NN, sec_level, verb)
            data["NN on Set E"] = current_best_E_NN
            
            if res_E_nn:
                
                current_best_E_BF, data_E_bf, res_E_bf = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d_bf, "bf", current_best_E_NN, sec_level, verb)
                data["BF on Set E"] = current_best_E_BF
                
                if res_E_bf:
                    safe = True

    return safe, data

def bjmm_3LV_fast(p, n, k, z):
    
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1 
    
    data = {}
    current_best = n+40
    current_best_E_BF, data_E_bf, res_E_bf = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d_bf, "bf", current_best)
    current_best_E_NN, data_E_nn, res_E_nn = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d_nn, "nn", current_best)
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d_bf, "bf", current_best)
    current_best_S_NN, data_S_nn, res_S_nn = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d_nn, "nn", current_best)

    data["BF on Set E"] = data_E_bf
    data["NN on Set E"] = data_E_nn
    data["BF on Shifted Set"] = data_S_bf 
    data["NN on Shifted Set"] = data_S_nn
    
    return data