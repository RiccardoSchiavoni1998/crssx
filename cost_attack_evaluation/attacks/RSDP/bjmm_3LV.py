from IPython.display import clear_output
from math import *
from attacks.RSDP.funs.utils_3LV import *
from attacks.RSDP.funs.nearest_neighbour import find_best_nn
import os

def clear_terminal():
    # Controllo del sistema operativo
    if os.name == 'nt':  # Windows
        _ = os.system('cls')
    else:  # Mac o Linux
        _ = os.system('clear')

# Utilizzo la funzione per cancellare l'output del terminale


def partial_cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d):
    
    succ_prob = comb(k+l,u0)*z**u0 * (7)**(-k-l)
    num_solutions = 1+((7**n)*(p**(k-n)))
    
    #vector weights level 1
    u_a, u_b, d_a, d_b = compute_lv_params(u0, d0, ε1, δ1)

    #vector weights level 2 
    u_a1, u_a2, d_a1, d_a2 = compute_lv_params(u_a, d_a, ε2, δ2)
    u_b1, u_b2, d_b1, d_b2 = compute_lv_params(u_b, d_b, ε2, δ2)
    
    #vector weights level 3 
    u_base1, u_base2, d_base1, d_base2 = compute_lv_params(u_a1, d_a1)
    u_base3, u_base4, d_base3, d_base4 = compute_lv_params(u_a2, d_a2)
    u_base5, u_base6, d_base5, d_base6 = compute_lv_params(u_b1, d_b1)
    u_base7, u_base8, d_base7, d_base8 = compute_lv_params(u_b2, d_b2)
    
    #compute representations
    try:
        rep_1 = compute_num_rep(u_b, u_b1, d_b1, alpha_e, alpha_d, δ2, ε2)
        l1 = round(log(rep_1, p))
        
        rep_0 = compute_num_rep(u0, u_b, 0, alpha_e, alpha_d, δ1, ε1)
        l0 = round(log(rep_0, p))-l1
        
    except Exception as e:
        rep_1, rep_0, l1, l0 = 0, 0, 0, 0
        ###print((e, l, δ2, ε2, rep_1, δ1, ε1, rep_0)
        
        
    if rep_1==0 or rep_0==0 or l0<=l1 or l-l0-l1<=0:
        return False, 0
    
    
    #______________________________________ LEVEL 3 ______________________________________
   
    len_v_base1 = floor(u0/2)
    len_v_base2 = ceil(u0/2)
    
    memory_cost_values = []
    len_list_base_values = {}
    time_cost_values = {}

    for i in range(1, 9):
        #load params lv3
        len_v_base = len_v_base1 if i % 2 == 1 else len_v_base2
        ubase = locals()["u_base" + str(i)]
        dbase = locals()["d_base" + str(i)]
        
        #compute list len
        len_list_base = compute_lists_len(len_v_base, p, z, zD, u=ubase, d=dbase)
        
        if len_list_base<=0:
            return False, 0
        
        len_list_base_values[str(i)] = len_list_base
        
        #compute partial time cost
        partial_time_cost_base = compute_time_cost(len_list_base, z, zD, p, ubase, dbase, l1)
        time_cost_values["cb_" + str(i)] = partial_time_cost_base
        
        #compute memory cost
        memory_cost_base = len_list_base*(ubase*log(z,2)+dbase*(log(zD,2)))
        memory_cost_values.append(memory_cost_base)
    
    
    #compute base time cost  2* (L3* ( l1*log(p,2)+u3*log(z,2)+d3*log(zD,2) ))
    time_cost_base = min(time_cost_values["cb_1"]+time_cost_values["cb_2"], time_cost_values["cb_3"]+time_cost_values["cb_4"], time_cost_values["cb_5"]+time_cost_values["cb_6"], time_cost_values["cb_7"]+time_cost_values["cb_8"])
    max_len_list_base = max(len_list_base_values.values())
    #______________________________________ LEVEL 2 ______________________________________
    
    len_list_lv2_values = {}
    len_v2= k+l
    
    for i in range(1, 3):
        #load params lv2
        u2_a = locals()["u_a" + str(i)]
        d2_a = locals()["d_a" + str(i)]
        u2_b = locals()["u_b" + str(i)]
        d2_b = locals()["d_b" + str(i)]
        
        #compute list len
        
        len_list_lv2_a = compute_lists_len(len_v2, p, z, zD, li=l1, u=u2_a, d=d2_a)
        len_list_lv2_values["a" + str(i)] = len_list_lv2_a
        
        len_list_lv2_b = compute_lists_len(len_v2, p, z, zD, li=l1, u=u2_b, d=d2_b)
        len_list_lv2_values["b" + str(i)] = len_list_lv2_b 
        
        if len_list_lv2_b<=0 or len_list_lv2_b<=0:
            return False, 0
        #compute partial time cost
        
        partial_time_cost_lv2_a = compute_time_cost(len_list_lv2_a, z, zD, p, u2_a, d2_a, l0)
        
        partial_time_cost_lv2_b = compute_time_cost(len_list_lv2_b, z, zD, p, u2_b, d2_b, l0)
        
        time_cost_values["partial_time_cost_lv2_a" + str(i)] = partial_time_cost_lv2_a
        time_cost_values["partial_time_cost_lv2_b" + str(i)] = partial_time_cost_lv2_b 
        
        #compute memory cost
        
        memory_cost_lv2_b = len_list_lv2_b*(u2_b*log(z,2)+d2_b*(log(zD,2)))
        memory_cost_values.append(memory_cost_lv2_b)
        
        memory_cost_lv2_a = len_list_lv2_a*(u2_a*log(z,2)+d2_a*(log(zD,2)))
        memory_cost_values.append(memory_cost_lv2_a)
    
    max_len_list_lv2 = max(len_list_lv2_values.values())
    #compute base time cost  2* (L2* ( l0*log(p,2)+u2*log(z,2)+d2*log(zD,2) ))
    time_cost_lv2 = min(time_cost_values["partial_time_cost_lv2_a1"]+time_cost_values["partial_time_cost_lv2_a2"], time_cost_values["partial_time_cost_lv2_b1"]+time_cost_values["partial_time_cost_lv2_b2"])
    
    #______________________________________ LEVEL 1 ______________________________________
  
    len_v1 = k+l
   
    len_list_lv1_values = {}
    
    #compute list len
    len_list_lv1_a = compute_lists_len(len_v1, p, z, zD, li=l0+l1, u=u_a, d=d_a)
    len_list_lv1_values["a"] = len_list_lv1_a
    
    len_list_lv1_b = compute_lists_len(len_v1, p, z, zD, li=l0+l1, u=u_b, d=d_b)
    len_list_lv1_values["b"] = len_list_lv1_b
    
    #compute memory cost
    
    memory_cost_lv1_a = len_list_lv1_a*(u_a*log(z,2)+d_a*(log(zD,2)))
    memory_cost_values.append(memory_cost_lv1_a)
    
    memory_cost_lv1_b = len_list_lv1_b*(u_b*log(z,2)+d_b*(log(zD,2)))
    memory_cost_values.append(memory_cost_lv1_b)

    #compute base time cost  2* ((L2)^2 * p**(-l0) * log(p,2))
    
    time_cost_lv1a = ((len_list_lv2_values["a1"]*len_list_lv2_values["a2"])/(p**(l0)))*log(p,2)    
    time_cost_lv1b = ((len_list_lv2_values["b1"]*len_list_lv2_values["b2"])/(p**(l0)))*log(p,2)    
    time_cost_lv1 = time_cost_lv1a + time_cost_lv1b
    
    params = u_a+d_a, u_b+d_b, l0, l1, num_solutions, succ_prob, len_list_lv1_a, len_list_lv1_b , max_len_list_base, max_len_list_lv2, time_cost_base, time_cost_lv2, time_cost_lv1, memory_cost_values

    return True, params
   
def cost_evaluator_bf(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, set_type, current_best):
    res={}           
    flag, results = partial_cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d)
    if flag:
        w1, w2, l0, l1, num_solutions, succ_prob, len_list_lv1_a, len_list_lv1_b , len_list_base, len_list_lv2, time_cost_base, time_cost_lv2, time_cost_lv1, memory_cost_values = results
        
        #______________________________________ LEVEL 0 ______________________________________
    
        #compute base time cost  L1^2 * p^-(l-l0-l1) * log(p,2)
        len_list_lv1=max(len_list_lv1_a, len_list_lv1_b)
        
        time_cost_0 = ((len_list_lv1_a*len_list_lv1_b)*log(p,2))/(p**(l-l0-l1))
        
        #TOTAL
        memory_cost = log(max(memory_cost_values),2)
        time_cost = time_cost_base+time_cost_lv2+time_cost_lv1+time_cost_0
        overall_cost = log(((time_cost/num_solutions)*memory_cost)/succ_prob,2)
        current_best = overall_cost
        
        #RESULT
        if set_type=="shifted":
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":w1+w2, "delta 1":δ1, "delta 2":δ2}
        else:
            res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "epsilon 1":ε1, "delta 1":δ1, "epsilon 2":δ1, "delta 2":δ2}
        
        res['Overall Cost'] = overall_cost
       
        details = {}

        details['Number of representation'] = {'l,l0,l1': [l,l0,l1] ,'q**l1':log(p**l1, 2), 'q**(l0-l1)': log(p**(l0-l1), 2), 'q**(l-l0-l1)':log(p**(l-l0-l1),2) }
        details["Memory cost"] = log(memory_cost,2)
        
        details['List Size'] = {'Base List': log(len_list_base,2), 'Lv2 Lists':log(len_list_lv2,2),  'Lv1 Lists': log(len_list_lv1,2)}
        
        details['Time Cost'] = {'Base Time Cost':log(time_cost_base, 2),  'Level 2 Time Cost':log(time_cost_lv2, 2), 'Level 1 Time Cost':log(time_cost_lv1, 2), 'Level 0 Cost':log(time_cost_0, 2)}
        
        details["Success Probability"] = log(succ_prob,2)
        res["Details"] = details

        
        
    return res, current_best

def cost_evaluator_nn(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, set_type, current_best, find_best_nn):
    res={}
    
    flag, results = partial_cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d)
    if flag:
        w1, w2, l0, l1, num_solutions, succ_prob, len_list_lv1_a, len_list_lv1_b , len_list_base, len_list_lv2, time_cost_base, time_cost_lv2, time_cost_lv1, memory_cost_values = results
           
        #compute base time cost  L1^2 * p^-(l-l0-l1) * log(p,2)
        n_round = p**(l-l0-l1)
        red_l1 = len_list_lv1_a/n_round
        red_l2 = len_list_lv1_b/n_round
        len_list_lv1=max(red_l1, red_l2)
        
        #compute memory cost
        memory_cost = log(max(memory_cost_values),2)
        
        #Nearest Neighbour
        partial_cost = log((((time_cost_base+time_cost_lv2+time_cost_lv1+n_round)/num_solutions)*memory_cost)/succ_prob,2)
        
        if partial_cost < current_best:
            
            #NEAREST NEIGHBOUR
            nn_costs, min_cost = find_best_nn(k, l, ε1 + δ1 + ε2 + δ2, w1, w2, red_l1, red_l2, current_best)
            
            if min_cost < current_best and len(nn_costs)>0:
                
                time_cost = time_cost_base+time_cost_lv2+time_cost_lv1+(min_cost*n_round)
                overall_cost = log(((time_cost/num_solutions)*memory_cost)/succ_prob,2)
                #
                #RESULT
                if set_type=="shifted":
                    res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":w1+w2, "delta 1":δ1, "delta 2":δ2}
                else:
                    res["Parameters"] = {"p":p, "n":n, "k":k, "z":z, "l":l, "epsilon 1":ε1, "delta 1":δ1, "epsilon 2":δ1, "delta 2":δ2}
                
                res['Overall Cost'] = overall_cost
            
                details = {}

                details['Number of representation'] = {'l,l0,l1': [l,l0,l1] ,'q**l1':log(p**l1, 2), 'q**(l0-l1)': log(p**(l0-l1), 2), 'q**(l-l0-l1)':log(p**(l-l0-l1),2) }
                details["Memory cost"] = log(memory_cost,2)
                
                details['List Size'] = {'Base List': log(len_list_base,2), 'Lv2 Lists':log(len_list_lv2,2),  'Lv1 Lists': log(len_list_lv1,2)}
                
                details['Time Cost'] = {'Base Time Cost':log(time_cost_base, 2),  'Level 2 Time Cost':log(time_cost_lv2, 2), 'Level 1 Time Cost':log(time_cost_lv1, 2), 'Num Iteration':  log(n_round, 2), 'Level 0 Cost (Nearest Neighbouor)':log(min_cost, 2)}
                
                details["Success Probability"] = log(succ_prob,2)
                res["Details"] = details
                nn_details = []
                for nn_cost in nn_costs:
                    nn_details.append(nn_cost)
                res['NN Details'] = nn_details
                #
                current_best = overall_cost

    return res, current_best
    
#SEBASTIAN RANGES
def bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator, mode, current_best, sec_level = 999, verb=False):
    
    #current_best = n+40
    if verb: print("Inizio", "Bjmm 3lv on Shifted set", mode, "\nParams:", p, n, k, z)
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
                        
                        if mode == "nn":
                            res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, "E", current_best, find_best_nn) #ERWIN
                        else:
                            res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, ε1, δ1, ε2, δ2, alpha_e, alpha_d, "E", current_best)
                    
                        if len(res_details) != {} and cost < current_best:
                            if cost < sec_level:
                                if verb: print("Finito", "Bjmm 3lv on set E", mode, "\nParams:", p, n, k, z, "\nNot Secure")
                                return cost, [], False
                            current_best = cost
                            list_cost.append(res_details)
    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    
    if verb: print("Finito", "Bjmm 3lv on Shifted set", mode, "\nParams:", p, n, k, z, "\nSecure")
    return current_best, list_cost, True                 

def bjmm_3lv_shifted(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator, mode, current_best, sec_level = 999, verb=False):

    #current_best = n+30
    if verb: print("Inizio", "Bjmm 3lv on Shifted set", mode, "\nParams:", p, n, k, z)
    list_cost = []
    ### BJMM SHIFTED

    for l in range(max(0, n-k-30), n-k+1):

        d0 = 0
        for u0 in range(8, k+l+1):
            
            max_δ1 = min(round(u0/2), 17)
            
            for δ1 in range(0, max_δ1+1):
                
                max_δ2 = min(round(u0/4), 9)
                
                for δ2 in range(0, max_δ2+1):
                    
                    if mode == "nn":
                        res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, 0, δ1, 0, δ2, alpha_e, alpha_d, "shifted", current_best, find_best_nn)
                    else:
                        res_details, cost = cost_evaluator(p, n, k, z, zD, l, u0, d0, 0, δ1, 0, δ2, alpha_e, alpha_d, "shifted", current_best)
                    
                    if len(res_details) != {} and cost < current_best:
                        if cost < sec_level:
                            if verb: print("Finito", "Bjmm 3lv on Shifted set", mode, "\nParams:", p, n, k, z, "\nNot Secure")
                            return cost, [], False
                        current_best = cost
                        list_cost.append(res_details)
                        res_details = {}
                        
    if len(list_cost)>0:
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    
    if verb: print("Finito", "Bjmm 3lv on Shifted set", mode, "\nParams:", p, n, k, z, "\nSecure")
    return current_best, list_cost, True                

def bjmm_3LV_opt_size_pk(p, n, k, z, current_best, sec_level, verb):
    data = {"BF on Set E":"", "NN on Set E":"", "BF on Shifted Set":"", "NN on Shifted Set":""}
    safe = False
    
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1 
    
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d, cost_evaluator_bf, "bf", current_best, sec_level, verb)
    data["BF on Shifted Set"] = current_best_S_BF

    if res_S_bf:
        
        current_best_S_NN, data_S_nn, res_S_nn = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d, cost_evaluator_nn, "nn", current_best_S_BF, sec_level, verb)
        data["NN on Shifted Set"] = current_best_S_NN
        
        if res_S_nn:
            
            current_best_E_NN, data_E_nn, res_E_nn = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator_nn, "nn", current_best_S_NN, sec_level, verb)
            data["NN on Set E"] = current_best_E_NN
            
            if res_E_nn:
                
                current_best_E_BF, data_E_bf, res_E_bf = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator_bf, "bf", current_best_E_NN, sec_level, verb)
                data["BF on Set E"] = current_best_E_BF
                
                if res_E_bf:
                    safe = True

    return safe, data

def bjmm_3LV(p, n, k, z):
    
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1 
    
    data = {}
    current_best = n+40
    current_best_E_BF, data_E_bf, res_E_bf = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator_bf, "bf", current_best)
    current_best_E_NN, data_E_nn, res_E_nn = bjmm_3lv_E(p, n, k, z, zD, alpha_e, alpha_d, cost_evaluator_nn, "nn", current_best)
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d, cost_evaluator_bf, "bf", current_best)
    current_best_S_NN, data_S_nn, res_S_nn = bjmm_3lv_shifted(p, n, k, z-1, zD, alpha_e, alpha_d, cost_evaluator_nn, "nn", current_best)

    data["BF on Set E"] = data_E_bf
    data["NN on Set E"] = data_E_nn
    data["BF on Shifted Set"] = data_S_bf 
    data["NN on Shifted Set"] = data_S_nn
    
    return data