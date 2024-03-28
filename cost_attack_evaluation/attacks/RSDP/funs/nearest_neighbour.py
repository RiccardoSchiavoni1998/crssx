from math import *

def nn_cost(k, l, w1, w2, f, x, y, ovlap, l1, l2):
    res = {}   
    try: 
        #d describes how many filters contains a binary solution (vx, vy) such that wth(vx+vy)=k+l-ovlap
        u = max(0, x+y-f)  #u is the number of common overlaps with the filters 
        r1 = max(0, (k+l)-(w1+w2)) #number of entries where both vectors have no entries
        r2 = max(0, f-(x+y)) ##number of entries where filters have no overlaps with vectors
        d = comb(ovlap, u)*comb(w1-ovlap, x-u)*comb(w2-ovlap, y-u)*comb(r1,r2)
    except:
        d = 0
    if d == 0:
        p1 = 2
        p2 = 2
        nf = 2
        d = 2
        bucketing_cost = 2
        collision_search_cost = l1*l2
    else: 
        p1= comb(w1, x)*comb((k+l)-w1, f-x) #
        p2 = comb(w2, y)*comb((k+l)-w2, f-y)
        nf = comb(k+l,f)
        bucketing_cost = ((l1*p1)+(l2*p2))/d
        collision_search_cost = ((l1*p1)*(l2*p2))/(nf*d)
    res["Bucketing Cost"] = log(bucketing_cost,2)
    res["Collision Search Cost"] = log(collision_search_cost,2)
    res['Parameters'] = {'x': str(x), 'y': str(y), 'f': str(f)}
    res['NN Details'] = {"p1": log(p1,2), "p2": log(p2,2), "d":log(d,2), "f": log(nf,2)}
    return bucketing_cost+collision_search_cost, res
    
def find_best_nn(k, l, e, w1, w2, l1, l2, best_cost):
        
    ovlap = 2*e
    list_cost=[]
    #f is the weight of the vector filters
    for f in range(1, (k+l+1)):
        
        #x are the number exclusive overlaps with vector 1 of weight w1
        
        #the minimum number of overlaps is more than 0 if w1+f exceedes the length k+l, there must be at least as many overlaps as the number of exceeding values
        min_x = max(0, (f+w1)-(k+l)) 
        max_x = min(f, w1) 
        
        for x in range(min_x, max_x):
            
            #y are the number exclusive overlaps with vector 2 of weight w2

            #the minimum number y of overlaps is more than 0 if w2+f exceedes the length k+l, there must be at least as many overlaps as the number of exceeding values
            #I think the logic is the same for both the lists
            #min_y = max(0, ((f-max(0,x-ovlap))+w2)-(k+l-(w1-ovlap)))
            min_y = max(0, (f+w2)-(k+l))
            max_y = min(f, w2)
            
            for y in range(min_y, max_y):
                cost, res = nn_cost(k, l, w1, w2, f, x, y, ovlap, l1, l2)
                aux = log(cost,2)
                if aux <= best_cost and res != {}:
                    best_cost = aux
                    res['NN Cost'] = cost
                    list_cost.append(res)
    if len(list_cost)>0:
        best_cost = min(list_cost, key=lambda x: x['NN Cost'])['NN Cost']
        list_cost = [item for item in list_cost if item['NN Cost'] == best_cost]
        [item.pop('NN Cost') for item in list_cost]
        return list_cost, best_cost
    return [], best_cost

