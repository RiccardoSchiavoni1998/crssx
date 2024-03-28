from math import *
from attacks.RSDP.funs.utils_2LV import *
from attacks.RSDP.funs.nearest_neighbour import *

def evaluator(p, n, k, z, l, set_, mode, current_best, w0, alpha_d, epsilon, delta, zD):

    res = {}
    flag = False
    
    len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2, d1_1, d1_2, d2_1, d2_2 = compute_params(k+l, w0, epsilon, delta)
    
    try: 
        rep = compute_n_reps(w0, u2, epsilon, delta, alpha_d)
        t = floor(log(rep, p))
    except Exception as e:
        rep, t = 0, 0
        
    if t>0 and l>t:

        num_solution = 1+(7**n)*(p**(k-n))
        
        prob = (comb(k+l, w0)*((z)**w0))/(7**(k+l)) 
        
        max_list_size, list_a, list_b, c_base, memory_base, c_lv1  = compute_partial_costs(p, l, t, len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2, d1_1, d1_2, d2_1, d2_2, z, zD)

        num_r0 = p**(l-t)

        if mode =="nn":
            
            list_a = list_a/num_r0
            list_b = list_b/num_r0
       
        memory_1a = list_a*(u1*log(z, 2)+delta*log(zD, 2))
        memory_1b = list_b*(u2*log(z, 2)+delta*log(zD, 2))
        memory_1 = min(memory_1a, memory_1b)
        memory_cost = max(memory_base, memory_1)
        
        if mode == "bf":
            c_0 = ((list_a*list_b)/num_r0)*log(p,2)
            total_cost = log((((c_base+c_lv1+c_0)/num_solution)*log(memory_cost,2))/prob,2)
            
            if total_cost <= current_best:
                flag = True
                current_best = total_cost
        
        else:
            partial_cost = log((((c_base+c_lv1+num_r0)/num_solution)*log(memory_cost,2))/prob,2)
        
            if partial_cost <= current_best:
            
                nn_costs, c_0 = find_best_nn(k, l, epsilon+delta, u1+delta, u2+delta, list_a, list_a, current_best)
                
                total_cost = log((((c_base+c_lv1+num_r0*c_0)/num_solution)*log(memory_cost,2))/prob,2)
                
                if total_cost < current_best and len(nn_costs)>0:
                    
                    nn_details = []
                    
                    for nn_cost in nn_costs:
                        nn_details.append(nn_cost)
                    
                    flag = True
                    current_best = total_cost
                    
        if flag:
                        
            res["Parameters"] = save_params(set_, p, n, k, z, l, w0, epsilon, delta)
            res['Details'] = save_details(rep, num_r0, prob, max_list_size, list_a, list_b, c_base, c_lv1, c_0)
            res['Memory Cost'] = log(memory_cost,2)
            res['Overall Cost'] = total_cost
            if mode =="nn":
                res['NN Details'] = nn_details
                    
            
    return res, current_best

#######################################################################################################################################################
def bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon, max_epsilon, min_delta, max_delta, set_, mode, current_best, sec_level = 0, verb = False):
    
    if verb: print("Start", "Bjmm 2lv on set ", set_, mode, "on Params:", p, n, k, z)
    list_cost=[]
    for l in range(1, (n-k)+1):
        
        if 'shifted' in set_: 
            min_w0 = 1 
            max_w0 = k+l+1
        else: 
            min_w0 = k+l
            max_w0 = k+l+1
       
        for w0 in range(min_w0, max_w0): 
            
            for epsilon in range(min_epsilon, max_epsilon+1):
           
                for delta in range(min_delta, max_delta+1):
                   
                    res_details, total_cost = evaluator(p, n, k, z, l, set_, mode, current_best, w0, alpha_d, epsilon, delta, zD)
                    
                    if res_details != {} and total_cost<=current_best:
                            
                            if total_cost < sec_level:
                                if verb: print("End",  "Bjmm 2lv on set", set_, mode, "on Params:", p, n, k, z, "Not Secure")
                                return total_cost, [], False
                            
                            current_best = total_cost
                            
                            list_cost.append(res_details)
                        
    if len(list_cost)>0:
        
        current_best = min(list_cost, key=lambda x: x['Overall Cost'])['Overall Cost']
        list_cost = [item for item in list_cost if item['Overall Cost'] == current_best]
    
    if verb: print("End",  "Bjmm 2lv on set", set_, mode, "on Params:", p, n, k, z, "Secure")
   
    return current_best, list_cost, True   

##################################################### INTERFACCE #########################################################################
def bjmm_2LV_opt_size_pk(p, n, k, z, ranges, current_best, sec_level, verb):
    data = {"BF on Set E":"", "NN on Set E":"", "BF on Shifted_E Set":"", "NN on Shifted_E Set":""}
    safe = False
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1
    
    min_epsilon_E = ranges['min_epsilon_E']
    max_epsilon_E = ranges['max_epsilon_E']
    min_delta_E = ranges['min_delta_E']
    max_delta_E = ranges['max_delta_E']
    
    min_epsilon_ES = ranges['min_epsilon_ES']
    max_epsilon_ES = ranges['max_epsilon_ES']
    min_delta_ES = ranges['min_delta_ES']
    max_delta_ES = ranges['max_delta_ES']
    
    current_best_S_BF, data_S_bf, res_S_bf = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_ES, max_epsilon_ES, min_delta_ES, max_delta_ES, "shifted_E", "bf", current_best, sec_level, verb)  
    data["BF on Shifted_E Set"] = current_best_S_BF 
    
    if res_S_bf:
        current_best_S_NN, data_S_nn, res_S_nn = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_ES, max_epsilon_ES, min_delta_ES, max_delta_ES, "shifted_E", "nn", current_best_S_BF, sec_level, verb)
        data["NN on Shifted_E Set"] = current_best_S_NN

        if res_S_nn:
            
            min_epsilon_E = 1
            max_epsilon_E = 5
            current_best_E_NN, data_E_nn, res_E_nn = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_E, max_epsilon_E, min_delta_E, max_delta_E, "E", "nn", current_best_S_NN, sec_level, verb)
            data["NN on Set E"] = current_best_E_NN
           
            if res_E_nn:    
                current_best_E_BF, data_E_bf, res_E_bf = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_E, max_epsilon_E, min_delta_E, max_delta_E, "E", "bf", current_best_E_NN, sec_level, verb)
                data["BF on Set E"] = current_best_E_BF
                
                if res_E_bf:
                    safe = True

    return safe, data

def bjmm_2LV_detailed(p, n, k, z, params):
    data = {}
    current_best = n+40
    
    alpha_d, zD = create_d_set(p,z)
    alpha_e = 1 

    # Set E
    min_epsilon_E = params['setE']['min_epsilon_E']
    max_epsilon_E = params['setE']['max_epsilon_E']
    
    min_delta_E = params['setE']['min_delta_E']
    max_delta_E = params['setE']['max_delta_E']

    current_best_E_BF, data_E_bf, res_E_bf = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_E, max_epsilon_E, min_delta_E, max_delta_E, "E", "bf", current_best, verb = True)
    current_best_E_NN, data_E_nn, res_E_nn = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_E, max_epsilon_E, min_delta_E, max_delta_E,  "E", "nn", current_best, verb = True)
    data["BF on Set E"] = data_E_bf
    data["NN on Set E"] = data_E_nn
    
    # Set shifted E
    min_epsilon_ES = params['setShiftedE']['min_epsilon_ES']
    max_epsilon_ES = params['setShiftedE']['max_epsilon_ES']
    
    min_delta_ES = params['setShiftedE']['min_delta_ES']
    max_delta_ES = params['setShiftedE']['max_delta_ES']
    
    current_best_S_E_BF, data_S_E_bf, res_S_E_bf = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_ES, max_epsilon_ES, min_delta_ES, max_delta_ES, "shifted_E", "bf", current_best, verb = True)
    current_best_S_E_NN, data_S_E_nn, res_S_E_nn = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_ES, max_epsilon_ES, min_delta_ES, max_delta_ES, "shifted_E", "nn", current_best, verb = True)
    data["BF on Shifted E Set"] = data_S_E_bf 
    data["NN on Shifted E Set"] = data_S_E_nn
    
    """# Set EuD
    min_epsilon_EuD = params['setEuD']['min_epsilon_EuD']
    max_epsilon_EuD = params['setEuD']['max_epsilon_EuD']
    min_delta_EuD = params['setEuD']['min_delta_EuD']
    max_delta_EuD = params['setEuD']['max_delta_EuD']
    
    current_best_EuD_BF, data_EuD_bf, res_EuD_bf = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_EuD, max_epsilon_EuD, min_delta_EuD, max_delta_EuD, "EuD", "bf", current_best, verb = True)
    current_best_EuD_NN, data_EuD_nn, res_EuD_nn = bjmm_2LV(p, n, k, z, alpha_d, zD, alpha_e, min_epsilon_EuD, max_epsilon_EuD, min_delta_EuD, max_delta_EuD, "EuD", "nn", current_best, verb = True)
    data["BF on Set EuD"] = data_EuD_bf
    data["NN on Set EuD"] = data_EuD_nn
    
    # Set shifted EuD
    min_epsilon_EuDS = params['setShiftedEuD']['min_epsilon_EuDS']
    max_epsilon_EuDS = params['setShiftedEuD']['max_epsilon_EuDS']
    min_delta_EuDS = params['setShiftedEuD']['min_delta_EuDS']
    max_delta_EuDS = params['setShiftedEuD']['max_delta_EuDS'] 
    
    current_best_S_EuD_BF, data_S_EuD_bf, res_S_EuD_bf = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_EuD, max_epsilon_EuD, min_delta_EuD, max_delta_EuD, "shifted_EuD", "bf", current_best, verb = True)
    current_best_S_EuD_NN, data_S_EuD_nn, res_S_EuD_nn = bjmm_2LV(p, n, k, z-1, alpha_d, zD, alpha_e, min_epsilon_EuD, max_epsilon_EuD, min_delta_EuD, max_delta_EuD, "shifted_EuD", "nn", current_best, verb = True)
    data["BF on Shifted EuD Set"] = data_S_EuD_bf 
    data["NN on Shifted EuD Set"] = data_S_EuD_nn"""
    
    return data
    