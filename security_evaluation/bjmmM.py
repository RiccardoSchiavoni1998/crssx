from math import *
from random import *
from lsh import find_best_lsh_solver
from funs import *
#   bjmm_depth_m(p, n, k, z, depth, l, set_, u, list_epsilon, list_delta , prob)
   
def bjmm_depth_m(p, n, k, z, depth, l, set_, w0, list_epsilon, list_delta, prob):
    
    """ """        
    list_to_plot = []
    valid, z, dim_set, zD, alpha_D, alpha_E, beta = compute_dim_sets(p,z,set_)
    num_solutions = 1+(dim_set**n)*(p**(k-n))
    #
    w_tree = compute_tree_weights(w0, depth, list_epsilon, list_delta)
    list_symbols, not_failed = compute_symbols(p, k, l, w_tree, depth, list_epsilon, list_delta, alpha_E, alpha_D, beta, dim_set, z)
    #print("peso", k+l)
    #for noo in w_tree:
    #    print("lv", w_tree[noo], "ovlp", list_epsilon[noo], "simb", list_symbols[noo])
    memory_costs = {}
    final_lists_len = {}
    len_lists = {}
    pre_cost = ((n-k-l)**2)*(n+1)*((ceil(log(p,2))+ceil(log(p,2))**2)) 
    time_costs = {"BQSF":pre_cost}
    
    res_lsh={}
    res_naive={}
    lsh_details = {}
    
    if not_failed:
        
        for lv in range(depth, -1, -1):
            len_lists[str(lv)] = {}
            
        for lv in range(depth-1, -1, -1): # per tutti i livelli da M-1 a 1
            if not_failed:
                lv_lists = []
                lv_memory_cost = []
                lv_time_cost = 0
                #0 1 2 3 4 5 6 7 
                # 0   1   2   3
                
                for node in range(0, 2**lv):
                    
                    if not_failed:
                        u = w_tree[str(lv)][str(node)]["u"]
                        d = w_tree[str(lv)][str(node)]["d"]
                        ua = w_tree[str(lv+1)][str(2*node)]["u"]
                        da = w_tree[str(lv+1)][str(2*node)]["d"]
                        ub = w_tree[str(lv+1)][str(2*node+1)]["u"]
                        db = w_tree[str(lv+1)][str(2*node+1)]["d"]
                        
                        list_1 = 0
                        list_2 = 0
                        cost = 0
                        
                        if lv == depth-1:
                            #COMPUTE BASE LISTS
                            #(k+l/2 , (ub,db))*(z**u)*(zD**db)
                            list_1 = compute_lists_len(ceil((k+l)/2), p, z, zD, list_symbols, lv+1, ua, da)
                            list_2 = compute_lists_len(floor((k+l)/2), p, z, zD, list_symbols, lv+1, ub, db)
                        else:
                            #GET OUTPUT LISTS FROM PREVIOUS MERGE
                            list_1 = len_lists[str(lv+1)][str(2*node)]
                            list_2 = len_lists[str(lv+1)][str(2*node+1)]

                        
                        list_lv = min(list_1,list_2)
                        memory_cost_lv = compute_memory_cost(list_lv, ub, db, z, zD)
                    
                        if lv == 0:
                            cost, output_list = merge_list_cost(p, l, list_1, list_2, k, list_symbols[str(lv)], ua, ub, da, db)
                            
                            epsilon = list_epsilon[str(lv+1)]
                            delta = list_delta[str(lv+1)]      
                            lsh_details, cost_0_lsh, memory_cost_0_lsh = find_best_lsh_solver(p, k, l, u, epsilon, delta, ua, ub, list_1, list_2, list_symbols[str(lv)], memory_cost_lv)
                            
                        else:
                            #merge cost
                            cost, output_list = merge_list_cost(p, l, list_1, list_2, k, list_symbols[str(lv)], ua, ub, da, db)
                            
                            #LEN OUTPUT LIST, min:
                            #|L1||L2|/p**li
                            #(k+l , (u,d))*(z**u)*(zD**d) / p**(l_i+l_i+1....)
                            
                            comb_list = compute_lists_len(k+l, p, z, zD, list_symbols, lv, u, d)
                            len_lists[str(lv)][str(node)]  = min(output_list, comb_list)
                                    
                            not_failed = not_failed and  min(output_list, comb_list)>= 1
                            
                            #compute memory
                            list_lv = min(list_1,list_2)
                            memory_cost = compute_memory_cost(list_lv, ub, db, z, zD)
                        
                        lv_lists.append(list_lv)    
                        lv_memory_cost.append(memory_cost)   
                        lv_time_cost = lv_time_cost + cost          
                
                        print(lv, node, round(log(list_lv,2)))

                if lv == 0:
                    
                    memory_costs[lv]={"lsh":memory_cost_0_lsh, "naive":memory_cost_lv} 
                    time_costs[lv]={"lsh":cost_0_lsh, "naive":cost} 
                        
                else:
                    final_lists_len[lv] = max(lv_lists)
                    memory_costs[lv] = max(lv_memory_cost)
                    time_costs[lv] = lv_time_cost
                #print( {k: log(v,2) for k, v in time_costs.items()})
                #print(  time_costs.items())
                
        if not_failed:          
            time_costs_naive = dict(map(lambda item: (item[0], item[1]['naive']) if isinstance(item[1], dict) else item, time_costs.items()))
            
            memory_costs_naive =  dict(map(lambda item: (item[0], item[1]['naive']) if isinstance(item[1], dict) else item, memory_costs.items()))
           
            len_lists =  dict(map(lambda item: (item[0], item[1]['naive']) if isinstance(item[1], dict) else item, final_lists_len.items()))
            
            time_costs_lsh= dict(map(lambda item: (item[0], item[1]['lsh']) if isinstance(item[1], dict) else item, time_costs.items()))
            
            memory_costs_lsh =  dict(map(lambda item: (item[0], item[1]['lsh']) if isinstance(item[1], dict) else item, memory_costs.items()))
            
            overall_time_cost_naive = sum(time_costs_naive.values())
            
            overall_memory_cost_naive = max(memory_costs_naive.values())
            
            overall_cost_naive = ((overall_time_cost_naive/num_solutions)*log(overall_memory_cost_naive,2))/prob
            
            
            overall_time_cost_lsh = sum(time_costs_lsh.values())
            
            overall_memory_cost_lsh = max(memory_costs_lsh.values())
            
            overall_cost_lsh = ((overall_time_cost_lsh/num_solutions)*log(overall_memory_cost_lsh,2))/prob
            res_lsh = results(p, n, k, z, depth, 'lsh', set_, l, w0, list_epsilon, list_delta, list_symbols, len_lists, memory_costs_lsh, time_costs_lsh, lsh_details, prob, overall_memory_cost_lsh, overall_time_cost_lsh, overall_cost_lsh)
            res_naive =results(p, n, k, z, depth, 'naive', set_, l, w0, list_epsilon, list_delta, list_symbols, len_lists, memory_costs_naive, time_costs_naive, {}, prob, overall_memory_cost_naive, overall_time_cost_naive, overall_cost_naive)
            print("l", l, "w0", w0, list_epsilon['1'], list_delta['1'], overall_cost_naive>overall_cost_lsh,  round(log(overall_cost_naive, 2)) , round(log(overall_cost_lsh, 2)))
        
    return not_failed, res_lsh, res_naive

def results(p, n, k, z, depth, mode, set_, l, w0, list_epsilon, list_delta, list_symbols, len_lists, memory_costs, time_costs, lsh_details, prob, memory_cost, time_cost, overall_cost):
    return {
        "Params":
            {
                "p":p,
                "n":n,
                "k":k,
                "z":z,
                "mode":mode,
                "depth":depth,
                "set":set_,
                "l":l,
                "w0":w0,
                "epsilon":list_epsilon,
                "delta":list_delta,
                "symbols":list_symbols
            },
        
        "Time Costs": {k: log(v,2) if v > 0 else 0 for k, v in time_costs.items()},
        "Memory Costs": {k: log(v,2) if v > 0 else 0 for k, v in memory_costs.items()},
        "Memory Costs": {k: log(v,2) if v > 0 else 0 for k, v in len_lists.items()},
        "nn costs": lsh_details,
        "Num Iteration": log((prob)**(-1),2),
        "Memory Cost":log(memory_cost,2),
        "Time Cost":log(time_cost,2),
        "Overall cost": log(overall_cost,2)
    }
