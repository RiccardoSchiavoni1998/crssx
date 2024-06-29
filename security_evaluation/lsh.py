from math import *
def lsh_solver(p, k, l, f, x, y, epsilon, delta, w1, w2, list_1, list_2, ell, naive_collision_search_cost, naive_bucketing_cost1, naive_bucketing_cost2):
    #AMMETTE SOLUZIONE SOLO SE 
    # [    0    ][      f   ][   0      ][ ]
    # [   w1-x  ][  x       ][     0    ][ ] 
    # [    0    ][       y  ][   w2-y   ]] ]
    # [    0    ][    u     ][     0    ][ ]# 
    # Affinche sia un combinazione di x, y, f valida per trovare una soluzione
    # Range x: max(w1+f-k+l, 0) < x < min(f,w1) minimo è il numero in cui devono sovrapporsi per forza 
    # Range y: max(w2+f-k+l, 0) < x < min(f,w1) analogo
    # Inoltre deve essere tale che 
    # 
    res = {"Failed":False}   
    try:
        d= 0
        ovlap = 2*(epsilon+delta)
        if(w1+w2-2*epsilon) == k+l:
            u = x+y-f
            if u>=0 and u<=ovlap :
                d = comb(ovlap, u)*comb(w1+delta-ovlap, x-u)*comb(w2+delta-ovlap, y-u)
        else:

            no_entries = k+l-((w1+delta)+(w2+delta)-ovlap) 
            
            min_ug = max(0, max((x+ovlap)-(w1+delta), (y+ovlap)-(w2+delta)))
            max_ug = min(ovlap, x, y)
            if w1-ovlap >= x-max_ug and w2-ovlap >= y-max_ug and ovlap >= max_ug and  no_entries>=f-(x+y-max_ug) and max_ug-min_ug>=0: 
                for u in range(min_ug, max_ug+1):
                    no_ovlp = max(0,  f-(x+y-u))
                    d+=comb(ovlap , u)*comb(w1+delta-ovlap, x-u)*comb(w2+delta-ovlap, y-u)*comb(no_entries, no_ovlp)
            
        p1 = comb(w1+delta, x)*comb(k+l-(w1+delta), f-x)
        p2 = comb(w2+delta, y)*comb(k+l-(w2+delta), f-y)
        nf = comb(k+l,f)
        
        #d = min([p1, p2, d])
        prob =  round(1 - ((1-(d/nf))**(nf/d)),20)
        
        
        if d<=0 or p1<=0 or p2<=0 or d>nf or d>min(p1,p2) or p1 > nf or p2>nf or prob==0 or x+y-f< 0 or x+y-f>ovlap:
            res = {"Failed":True} 
        else:
            
            bucketing_cost1 = (list_1)*(p1/d)
            bucketing_cost2 = (list_2)*(p2/d)
            
            collision_search_cost = (nf/d)*(((list_1*(p1/nf)) * (list_2*(p2/nf)))/(p**ell))
            
   
            res["lists size"] ={"list1": log(list_1,2), "list2": log(list_2,2)} 
            res["Bucketing Cost 1"] = log(bucketing_cost1,2)
            res["Bucketing Cost 2"] = log(bucketing_cost1,2)
            res["Collision Search"] = log(collision_search_cost,2)
            res['Parameters'] = {'x': str(x), 'y': str(y), 'u': str(x+y-f), 'f': str(f)}
            res['Lsh Solver Details'] = {"p1": log(p1,2), "p2": log(p2,2), "d":log(d,2), "nf": log(nf,2)}
            res['Memory Cost'] = bucketing_cost1
            res["Num Iteration Solver"] = prob
    except Exception as e:
        #print(e, "p1", p1<=0, "p2", p2<=0, "d", d<=0, "nf", nf<=0, "list1", list_1<=0, "list2", list_2<=0)
        res = {"Failed":True} 
    if res["Failed"]:
        prob = 1
        bucketing_cost1 = naive_bucketing_cost1
        bucketing_cost2 = naive_bucketing_cost2
        collision_search_cost =naive_collision_search_cost
    return bucketing_cost1, bucketing_cost2, collision_search_cost, prob, res

### find_best_lsh_solver(p, k, l, w0, epsilon, delta, wa, wb, list_a, list_b, ell_0, memory_cost_1)
def find_best_lsh_solver(p, k, l, u0, epsilon, delta, w1, w2, list_1, list_2, ell, memory):
    
    naive_coll_bit = (k+l)*ceil(log(p,2))
    naive_collision_search = (list_1*list_2)/(p**ell)
    naive_bucketing_1 = 0
    naive_bucketing_2 = 0
    sort_lists = (list_1*log(list_1,2) + list_2*log(list_2,2))
    compute_ell_ops1 = (w1+delta)*ell*(ceil(log(p,2))+ceil(log(p,2))**2)
    compute_ell_ops2 = (w2+delta)*ell*(ceil(log(p,2))+ceil(log(p,2))**2)
    total_cost = list_1*(compute_ell_ops1) +list_2*(compute_ell_ops2) + sort_lists + naive_collision_search*naive_coll_bit
    best_cost = naive_collision_search
    ovlap = 2*(epsilon+delta)
    
    list_cost=[]
    #list_1 = list_1/(p**ell)
    #list_2 = list_2/(p**ell)
    #f is the weight of the vector filters
    for f in range(1, (k+l+1)):
        min_x = max(1, (f+w1+delta)-(k+l)) 
        max_x = min(f, w1+delta) +1
        
        for x in range(min_x, max_x):
            
            min_y = max(1, (f+w2+delta)-(k+l)) 
            max_y = min(f, w2+delta)+ 1
            
            for y in range(min_y, max_y):
                if x+y>=(f+u0)-(k+l) and ((x+y-f)<=ovlap):
                    bucketing_cost1, bucketing_cost2, collision_search_cost, prob, res = lsh_solver(p, k, l, f, x, y, epsilon, delta, w1, w2, list_1, list_2, ell, naive_collision_search, naive_bucketing_1, naive_bucketing_2)
                    new_cost = (bucketing_cost1+bucketing_cost2+collision_search_cost)/prob
                    if new_cost < best_cost and not(res["Failed"]):
                        best_cost = new_cost
                        res['Lsh Solver Cost'] = best_cost
                        list_cost.append(res)
                        
                        
                   
    if len(list_cost)>0:
        try:
            list_cost = [item for item in list_cost if not(item['Failed'])]
            best_cost = min(list_cost, key=lambda x: x['Lsh Solver Cost'])['Lsh Solver Cost']
            list_cost = [item for item in list_cost if item['Lsh Solver Cost'] == best_cost]
            best_memory = min(list_cost, key=lambda x: x['Memory Cost'])['Memory Cost']
            list_cost = [item for item in list_cost if item['Memory Cost'] == best_memory]
            memory =  best_memory
            [item.pop('Memory Cost') for item in list_cost]
            [item.pop('Lsh Solver Cost') for item in list_cost]
            res = list_cost[0]
            f = int(res['Parameters']['f'])
            op_buck1 = min(f, w1+delta)
            op_buck2 = min(f, w2+delta)
            prob = res["Num Iteration Solver"]
            res["Num Iteration Solver"] = log((prob)**(-1),2)
            
            bucketing_cost1 = (2**res["Bucketing Cost 1"])*op_buck1
            bucketing_cost2 = (2**res["Bucketing Cost 2"])*op_buck2
            collision_search = (2**res["Collision Search"])*max(1, ovlap*log(p,2))
            total_cost = list_1*(compute_ell_ops1) +list_2*(compute_ell_ops2) + sort_lists + (bucketing_cost1 + bucketing_cost2 + collision_search)/prob
        
        except Exception as e:
            print("Fine ott" , e)
    
    
    return res, total_cost , memory

