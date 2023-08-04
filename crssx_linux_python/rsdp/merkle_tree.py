from utils import *

class MerkleTree:
    def __init__(self, n_leaves, depth):
        if(n_leaves%2==0):
            self.n_leaves = n_leaves
            self.depth = depth
            self.tree =  None
            self.merkle_proof =  None
            self.full = False
        else:
            raise Exception('Il numero delle foglie deve essere una porenza di 2')

    #METODI PUBBLICI 
    def make_tree(self, leaves):
        if isinstance(leaves, list) and len(leaves) == self.n_leaves and not(self.full): 
            self.tree = []
            self.tree.append(leaves)  
            self.__make_tree(leaves, self.depth-1) 
            self.full = True
        else:
            raise Exception('Il numero delle foglie deve essere pari a {}'.format(self.n_leaves))
       
    def get_root(self):
        if self.full:
            return self.tree[0][0]
        else:
            raise Exception('Albero non creato')

    def get_merkle_proof(self):
        if self.full and self.merkle_proof is not None:
            return self.merkle_proof

    def compute_proof(self, list_nodes):
        if all(self.full or 1 <= node <= 2**self.depth for node in list_nodes):
            self.merkle_proof={}
            list_leaves = sorted(list(map(lambda x: x+1 if x % 2 == 0 else x-1, list_nodes))) 
            self.__compute_merkle_proof(self.depth, list_leaves)
            list_leaves = list(filter(lambda x: x not in list_nodes, list_leaves)) 
            self.merkle_proof[self.depth] = dict(map(lambda x: (x, self.tree[self.depth][x]), list_leaves)) 
            #self.merkle_proof = sorted(self.merkle_proof.items())
            self.merkle_proof = {k: self.merkle_proof[k] for k in sorted(self.merkle_proof, key=lambda x: int(x))}
        else:
            raise Exception('Albero non creato o foglia non valida')

    def recompute_root(self, merkle_proof, leaves):
        if len(leaves)<self.n_leaves:
            return self.__recompute_root(merkle_proof, leaves)
    
    #METODI PRIVATI

    def __make_tree(self, list_nodes, depth): 
        if(depth>=0): 
            list_parent = self.__create_new_level(list_nodes) 
            self.tree.insert(0, list_parent)
            self.__make_tree(list_parent, depth-1) 

    def __create_new_level(self, child_nodes):
        parents = [] 
        for i in range(0, len(child_nodes), 2): 
            new_node = self.__compute_father_value(child_nodes[i], child_nodes[i+1]) 
            parents.append(new_node)
        return parents
        
    def __compute_father_value(self, sx, dx):
        return hexhash(sx+dx)
    
    def __compute_merkle_proof(self, depth, list_index):
        if(depth > 1): 
            list_parent = sorted(list(set(map(lambda elem: ((elem // 2) + 1) if (elem // 2) % 2 == 0 else (elem // 2) - 1, list_index))))  
            parent_proof = list(filter(lambda x: x*2 not in list_index and (x*2)+1 not in list_index, list_parent))
            if len(parent_proof)>0:
                self.merkle_proof[depth-1] = dict(map(lambda x: (x, self.tree[depth-1][x]), parent_proof)) 
            self.__compute_merkle_proof(depth-1, list_parent) 

    def __recompute_root(self, merkle_proof, nodes):
        if len(nodes)==2:
            return self.__compute_father_value(nodes[0],nodes[1])
        else:
            if len(merkle_proof.keys())>0:
                index = max(merkle_proof.keys())
                current_level = merkle_proof.pop(index)
                merged_nodes = {**current_level, **nodes}
                merged_nodes = dict(sorted(merged_nodes.items()))
            else:
                merged_nodes=nodes
            new_nodes = {}
            for key in merged_nodes:
                new_key = key//2
                if new_key in new_nodes.keys():
                    new_nodes[new_key] = self.__compute_father_value(new_nodes[new_key],merged_nodes[key])
                else:
                    new_nodes[new_key] = merged_nodes[key]
            return self.__recompute_root(merkle_proof, new_nodes)