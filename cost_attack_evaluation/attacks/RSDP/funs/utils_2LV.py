from math import *

def bits_to_bytes(bits):
    bytes = bits / 8
    return bytes

#FUNdim_set

def compute_params(length, u0, v=0, d=0):
    
    u1 = floor(u0/2)+v
    u2 = ceil(u0/2)+v
    
    len_vb_1 = floor(length/2)
    len_vb_2 = ceil(length/2)
    
    u1_1 = floor(u1/2)
    u1_2 = ceil(u1/2)
    u2_1 = floor(u2/2)
    u2_2 =ceil(u2/2)
    
    if d!=0:
        d1_1 = floor(d/2)
        d1_2 = ceil(d/2)
        d2_1 = floor(d/2)
        d2_2 = ceil(d/2)
        return len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2, d1_1, d1_2, d2_1, d2_2
   
    else:
        return len_vb_1, len_vb_2, u1, u2, u1_1, u1_2, u2_1, u2_2

def compute_n_reps(u0, u1, v=0, d=0, alpha_d=0):
    if v!=0 and d!=0:
        return comb(u0, u1)*comb(u1, 2*v)*((comb((u1-(2*v)), d))**2)*(alpha_d**(2*d))
    if v!=0 and d==0:
        return comb(u0, u1)*comb(u1, 2*v)
    return comb(u0, u1)
    
def compute_partial_costs(p, l, t, len_vb_1, len_vb_2, u1_1, u1_2, u2_1, u2_2, dim_set, d1_1=0, d1_2=0, d2_1=0, d2_2=0, dim_set_d=0, alpha_d=0):
    
    if dim_set_d == 0:
    
        #Livello base
        lb_1 = comb(len_vb_1, u1_1)*(dim_set**u1_1)
        lb_2 = comb(len_vb_2, u1_2)*(dim_set**u1_2)
        lb_3 = comb(len_vb_1, u2_1)*(dim_set**u2_1)
        lb_4 = comb(len_vb_2, u2_2)*(dim_set**u2_2) 
        
        #Livello 1
        c_base = (lb_1*(l*log(p,2)+u1_1*log(dim_set,2)))+(lb_2*(l*log(p,2)+u1_2*log(dim_set,2)))+(lb_3*(l*log(p,2)+u2_1*log(dim_set,2)))+(lb_4*(l*log(p,2)+u2_2*log(dim_set,2)))     
    else:

        #Livello base
        lb_1 = comb(len_vb_1, u1_1 + d1_1)*comb(u1_1+d1_1, u1_1)*(dim_set**u1_1)*(alpha_d**d1_1)
        lb_2 = comb(len_vb_2, u1_2 + d1_2)*comb(u1_2+d1_2, u1_2)*(dim_set**u1_2)*(alpha_d**d1_2)
        lb_3 = comb(len_vb_1, u2_1 + d2_1)*comb(u2_1+d2_1, u2_1)*(dim_set**u2_1)*(alpha_d**d2_1)
        lb_4 = comb(len_vb_2, u2_2 + d2_2)*comb(u2_2+d2_2, u2_2)*(dim_set**u2_2)*(alpha_d**d2_2)

        #Livello 1
        c_base = (lb_1*(l*log(p,2)+u1_1*log(dim_set,2)+d1_1*log(dim_set_d,2)))+(lb_2*(l*log(p,2)+u1_2*log(dim_set,2)+d1_2*log(dim_set_d,2)))+(lb_3*(l*log(p,2)+u2_1*log(dim_set,2)+d2_1*log(dim_set_d,2)))+(lb_4*(l*log(p,2)+u2_2*log(dim_set,2)+d2_2*log(dim_set_d,2)))     
    
    max_list_size = max(lb_1, lb_2, lb_3, lb_4)
    list_a = (lb_1*lb_2)/(p**t)      
    list_b = (lb_3*lb_4)/(p**t)     
    
    c_lv1 = (list_a + list_b)*log(p,2)
    
    num_r0 = p**(l-t)
    
    return max_list_size, c_base, c_lv1, list_a, list_b, num_r0

def compute_memory_cost(len_vb_1, len_vb_2, w1_1, w1_2, w2_1, w2_2, list_a, list_b, w1, w2, z):
    lb_1 = comb(len_vb_1, w1_1)*(z**w1_1)
    lb_2 = comb(len_vb_2, w1_2)*(z**w1_2)
    lb_3 = comb(len_vb_1, w2_1)*(z**w2_1)
    lb_4 = comb(len_vb_2, w2_2)*(z**w2_2) 
    memory_base_a = min(lb_1*(w1_1*log(z,2)), lb_2*(w1_2*log(z,2)))
    memory_base_b = min(lb_3*(w2_1*log(z,2)), lb_4*(w2_2*log(z,2)))
    memory_base = max(memory_base_a, memory_base_b)
    memory_1a = list_a*(w1*log(2,z))
    memory_1b = list_b*(w2*log(2,z))
    memory_1 = min(memory_1a, memory_1b)
    
    memory_cost = max(memory_base, memory_1)

    return memory_cost
  

