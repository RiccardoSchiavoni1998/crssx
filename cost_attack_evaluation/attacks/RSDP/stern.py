from math import *
def evaluator(p, z, n, k, l):
    n_sol = 1+(z**n)*(p**(k-n))
    w1 = floor((k+l)/2)
    w2 = ceil((k+l)/2)
    list_1 = z**w1
    list_2 = z**w2
    cost1 = list_1*((w1*log(z,2))+(l*log(p,2)))
    cost2 = list_2*((w2*log(z,2))+(l*log(p,2)))
    cost3 = ((list_1*list_2)*((k+l)*log(p,2)))/(p**l)
    memory_stern = log(list_1*w1*log(z,2),2)
    total_cost = ((cost1+cost2+cost3)*memory_stern)/n_sol
    total_cost = log(total_cost,2)
    return total_cost, memory_stern

def stern(p, n, k, z):
    C_opt = 10**6
    M_opt = 10**6
    P_opt =  {'ell': -1}
    for l in range(n-k+1):
            C, M = evaluator(p, z, n, k, l)
            if C < C_opt:
                C_opt = C
                M_opt = M
                P_opt =  l
                if C < 128:
                    return False, {}, C
    return True, {"Time Cost":C_opt, "Memory Cost":M_opt, "l":P_opt}, C_opt

def stern_opt_size_pk(p, n, k, z, security_level):
    C_opt = 10**6
    M_opt = 10**6
    P_opt =  {'ell': -1}
    for l in range(n-k+1):
            C, M = evaluator(p, z, n, k, l)
            if C < C_opt:
                C_opt = C
                M_opt = M
                P_opt =  l
                if C < security_level:
                    return False, 0
    return True, C_opt



