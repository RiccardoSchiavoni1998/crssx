from math import *
import random
import numpy as np

def gilbert_varshamov_bound(n, r):
    d = int(np.floor((1 - r) * n))  # Calcola la distanza minima
    
    gv_sum = 0
    for i in range(1, d):
        gv_sum += comb(n, i)
    
    k = n - gv_sum
    return k / n

def compute_dim_sets(p,z,mode):
    
    alpha_D = 0
    alpha_E = 0
    beta = 0
    zD = 0
    dim_set = z
    
    if z==2:
        zD = 2
        alpha_D = 2
        alpha_E = 0
        beta = 1
    
    if z==4:
        zD = 4
        alpha_D = 2
        alpha_E = 0
    
    if z== 7:
        g = 2
        alpha_D = 0
        alpha_E = 0
        zD = 0
        list_E = []
        for i in range(z):
            list_E.append(g**i)
        dim_set = z
        if 'shifted' in mode:
            z = z-1
            shift = 1
            list_E = sorted([(num - shift)%127 for num in list_E])
            list_E = [x for x in list_E if x != 0]

        list_alpha_E = []
        for e1 in list_E:
            counter = 0
            for e2 in list_E:
                if (e1+e2)%p in list_E:
                    counter = counter+1
            list_alpha_E.append(counter)
        
        if len(set(list_alpha_E)) == 1:
            alpha_E = list_alpha_E[0]   
        list_alpha_D = []
        list_D = []
        for d1 in list_E:
            counter = 0
            for d2 in list_E:
                if not((d1-d2)%p in list_E) and not((d1-d2)%p==0):
                    counter = counter+1
                    list_D.append(((d1-d2))%p)
            list_alpha_D.append(counter)
        zD = len(list_D) 
        if len(set(list_alpha_D)) == 1:
            alpha_D = list_alpha_D[0]

    return z, dim_set, zD, alpha_D, alpha_E, beta
    
def compute_representation_0(dim_set, z, k, l, u0, u1, epsilon, alpha_E, delta, alpha_D, d0, d1, beta):
    if dim_set==7:
        
        if comb(u0,u1)*comb(u1, 2*epsilon)*(comb(ceil(u0/2)-epsilon, delta)**2)*(alpha_D**(2*delta))==0:
            print(ceil(u0/2), 2*epsilon, delta)
            print((comb(u1-2*epsilon, delta)))
        
        return comb(u0,u1)*comb(u1, 2*epsilon)*(comb(u1-2*epsilon, delta)**2)*(alpha_D**(2*delta))
    else:
        if z==2 or z==4:
            return comb(u0, u1-epsilon)*(comb(u1-epsilon,d1)**2)*(alpha_D**(2*d1))*comb(k+l-(u0), epsilon)
        else:
            return comb(u0, u1)*comb(u1,2*epsilon)*(alpha_E**(2*epsilon))
            

def merge_list_cost(p, l, l1, l2, k, ell, ua=0, ub=0, da=0, db=0):
    c1 = (l1*(ua+da)+l2*(ub+db))*ell*(ceil(log(p,2))+ceil(log(p,2))**2)
    c2 = (l1*log(l1,2)+l2*log(l2,2))
    c3 = ((l1*l2)/(p**ell))*(k+l)*ceil(log(p,2))
    
    output_list=(l1*l2)/(p**ell)
    return c1 + c2 +c3 , output_list

def compute_memory_cost(l,u,d,z,zD):
    return l*(u*log(z,2)+d*log(zD,2))
            
def results(p, n, k, z, depth, mode, set_, l, w0, epsilon, delta, list_symbols, len_lists, lsh_details, prob, memory_cost, time_costs, overall_cost):
    
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
                "epsilon":epsilon,
                "delta":delta,
                "symbols":list_symbols
            },
        
        "Time Costs": {k: log(v,2) if v > 0 else 0 for k, v in time_costs.items()},
        "Lists Size": {k: log(v,2) if v > 0 else 0 for k, v in len_lists.items()},
        "Lsh Costs": lsh_details,
        "Num Iteration": log((prob)**(-1),2),
        "Time Cost":log(sum(time_costs.values()),2),
        "Memory Cost":log(memory_cost,2),
        "Overall cost": log(overall_cost,2)
    }
 