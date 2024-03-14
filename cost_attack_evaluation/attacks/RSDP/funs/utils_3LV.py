from math import *

def bits_to_bytes(bits):
    bytes = bits / 8
    return bytes

#FUNdim_set

def compute_lv_params(ui, di, v=0, δ=0):
    u_a = floor(ui/2)+v
    u_b = ceil(ui/2)+v
    d_a = floor(di/2)+δ
    d_b = ceil(di/2)+δ
    
    return u_a, u_b, d_a, d_b

def compute_num_rep(u0, u1, d, alpha_e, alpha_d, δ, v):
    rep = comb(u0, u1)*comb(u1, 2*v)*(alpha_e**(2*v))*((comb(u1-2*v, δ))**2)*(alpha_d**(2*δ))*comb(d, round(d/2))
    return rep
           
def compute_lists_len(len_v, p, z, zD, li=0, u=0, d=0):
    return (comb(len_v, (u+d))*comb((u+d),u)*(z**u)*(zD**d))/(p**li)

def compute_time_cost(len_list, z, zD, p, u, d, li=0):
    try: 
        return len_list*((li*log(p,2))+(u*log(z, 2))+(d*log(zD,2)))
    except:
        print("EEE", len_list, z, zD, p, u, d, li)