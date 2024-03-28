from math import *

def create_d_set(p,z):
    list_D = []
    g = 2
    list_E = []
    for i in range(z):
        list_E.append(g**i)
    for a in list_E:
        count = 0
        for b in list_E:
            res = (a-b)%p
            if res!=0 and not(res in list_E):
                list_D.append(res)
                count += 1
                
    return count, len(list_D)

def create_d_set(p,z):
    list_D = []
    g = 2
    list_E = []
    for i in range(z):
        list_E.append(g**i)
    for a in list_E:
        count = 0
        for b in list_E:
            res = (a-b)%p
            if res!=0 and not(res in list_E):
                list_D.append(res)
                count += 1
                
    return count, len(list_D)

def compute_params(length, u0, epsilon=0, delta=0):
    
    u1 = floor(u0/2)+epsilon
    u2 = ceil(u0/2)+epsilon
    u1 = floor(u0/2)+epsilon
    u2 = ceil(u0/2)+epsilon
    
    len_vb_1 = floor(length/2)
    len_vb_2 = ceil(length/2)
    
    u1_1 = floor(u1/2)
    u1_2 = ceil(u1/2)
    u2_1 = floor(u2/2)
    u2_2 =ceil(u2/2)
    
    d1_1 = floor(delta/2)
    d1_2 = ceil(delta/2)
    d2_1 = floor(delta/2)
    d2_2 = ceil(delta/2)

    return len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2, d1_1, d1_2, d2_1, d2_2
   
def compute_n_reps(u0, u1, e=0, d=0, alpha_d=0):
    if e!=0 and d!=0:
        return comb(u0, u1)*comb(u1, 2*e)*((comb((u1-(2*e)), d))**2)*(alpha_d**(2*d))
    if e!=0 and d==0:
        return comb(u0, u1)*comb(u1, 2*e)
def compute_n_reps(u0, u1, e=0, d=0, alpha_d=0):
    if e!=0 and d!=0:
        return comb(u0, u1)*comb(u1, 2*e)*((comb((u1-(2*e)), d))**2)*(alpha_d**(2*d))
    if e!=0 and d==0:
        return comb(u0, u1)*comb(u1, 2*e)
    return comb(u0, u1)

#return max_list_size, list_a, list_b, c_base, memory_base, c_lv1 
def compute_partial_costs(p, l, t, len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2, d1_1, d1_2, d2_1, d2_2, dim_set, dim_set_D):

    #
    lb_1 = comb(len_vb_1, u1_1 + d1_1)*comb(u1_1+d1_1, u1_1)*(dim_set**u1_1)*(dim_set_D**d1_1)
    lb_2 = comb(len_vb_2, u1_2 + d1_2)*comb(u1_2+d1_2, u1_2)*(dim_set**u1_2)*(dim_set_D**d1_2)
    lb_3 = comb(len_vb_1, u2_1 + d2_1)*comb(u2_1+d2_1, u2_1)*(dim_set**u2_1)*(dim_set_D**d2_1)
    lb_4 = comb(len_vb_2, u2_2 + d2_2)*comb(u2_2+d2_2, u2_2)*(dim_set**u2_2)*(dim_set_D**d2_2)

    #Livello 1
    #c_base = (lb_1*(l*log(p,2)+u1_1*log(dim_set,2)+d1_1*log(dim_set_D,2)))+(lb_2*(l*log(p,2)+u1_2*log(dim_set,2)+d1_2*log(dim_set_D,2)))+(lb_3*(l*log(p,2)+u2_1*log(dim_set,2)+d2_1*log(dim_set_D,2)))+(lb_4*(l*log(p,2)+u2_2*log(dim_set,2)+d2_2*log(dim_set_D,2)))     
    enum_list_1 = lb_1*(t*log(p,2)+u1_1*log(dim_set,2)+d1_1*log(dim_set_D,2))
    enum_list_2 = lb_2*(t*log(p,2)+u1_2*log(dim_set,2)+d1_2*log(dim_set_D,2))
    enum_list_3 = lb_3*(t*log(p,2)+u2_1*log(dim_set,2)+d2_1*log(dim_set_D,2))
    enum_list_4 = lb_4*(t*log(p,2)+u2_2*log(dim_set,2)+d2_2*log(dim_set_D,2)) 
    c_base =enum_list_1+enum_list_2+enum_list_3+enum_list_4  
    
    max_list_size = max(lb_1, lb_2, lb_3, lb_4)
    
    list_a = (lb_1*lb_2)/(p**t)      
    list_b = (lb_3*lb_4)/(p**t)     
    
    c_lv1 = (list_a + list_b)*log(p,2)
    
    memory_base_a = min(lb_1*(u1_1*log(dim_set,2)+d1_1*log(dim_set_D,2)), lb_2*(u1_2*log(dim_set,2)+d1_2*log(dim_set_D,2)))
    memory_base_b = min(lb_3*(u2_1*log(dim_set,2)+d2_1*log(dim_set_D,2)), lb_4*(u2_2*log(dim_set,2)+d2_2*log(dim_set_D,2)))
    memory_base = max(memory_base_a, memory_base_b)
    

    return max_list_size, list_a, list_b, c_base, memory_base, c_lv1 

#return detail
def save_details(rep, num_r0, prob, max_list_size, list_a, list_b, c_base, c_lv1, c_0):
    
    details = {}
    
    details['Number of Representation'] = {'q**t':log(rep,2), 'q**(l-t)': log(num_r0, 2)}
    
    details['Probability'] = prob
    
    details['List Size'] = {'Base List': log(max_list_size,2), 'Lv1 Lists': log(max(list_a, list_b),2)}
    
    details['Time Cost'] = {'Base Time Cost':log(c_base, 2), 'Level 1 Time Cost':log(c_lv1, 2), 'Level 0 Time Cost': log(c_0, 2)}
    
    return details

def save_params(set_, p, n, k, z, l, w0, epsilon, delta):
        
    if set_=="E": return {"p":p, "n":n, "k":k, "z":z, "l":l, "epsilon":epsilon}
    
    if set_=="shifted_E": return {"p":p, "n":n, "k":k, "z":z, "l":l, "w0":w0}
    
    if set_=="EuD": return {"p":p, "n":n, "k":k, "z":z, "l":l, "epsilon":epsilon, "delta":delta}
    
    if set_=="shifted_EuD": return {"p":p, "n":n, "k":k, "z":z, "l":l, "delta":delta}
    