from utils import *

class SeedTree:
    def __init__(self, n_leaves, depth, salt):
        if(depth>0):
            self.seed_m = None
            self.salt = str(salt)
            self.n_leaves = n_leaves
            self.depth = depth
            self.tree = None
            self.seed_path = None
            self.full = False
        else:
            raise Exception('Il numero delle foglie deve essere una porenza di 2')

    def make_tree(self, seed_m):
        if self.full:
            raise Exception('Albero gia creato')
        else:
            self.seed_m = seed_m
            #BISOGNA AGGIUNGERE CONTROLLI?
            self.tree = []
            self.__make_tree([self.seed_m], 0)
            self.full = True
        
    def get_leaves(self):
        if self.full:
            return self.tree[self.depth]
        else:
            raise Exception('Albero non creato')

    def compute_level(self, parents, level):
        return self.__create_new_level(parents, level) 

    def get_seed_path(self):
        if self.full and self.seed_path is not None:
            return self.seed_path

    def compute_seed_path(self, list_nodes):
        if all(self.full or 1 <= node <= 2**self.depth for node in list_nodes):
            self.seed_path={}
            self.__compute_seed_path(self.depth, list_nodes)
        else:
            raise Exception('Albero non creato o foglia non valida')
        
    def get_required_leaves_from_seed_path(self, seed_path, leaves_indexes):
        leaves = self.__get_required_leaves_from_seed_path(seed_path)
        if list(leaves.keys())==leaves_indexes:
            return leaves
        else:
            raise Exception('Seed Path non corretto')
    

    def __make_tree(self, list_nodes, lev):
        if(lev<=self.depth):
            self.tree.append(list_nodes)
            list_children = self.__create_new_level(list_nodes, lev)
            self.__make_tree(list_children, lev+1)

    def __create_new_level(self, parents, level):
        children = []
        if level == 0:
            sx, dx = self.__compute_children_value(parents[0], '')
            children.append(sx)
            children.append(dx)
        else:
            base = self.n_leaves
            for i in range(0, len(parents)):
                sx, dx = self.__compute_children_value(parents[i], base+i)
                children.append(sx)
                children.append(dx)
        return children
    
    def __recompute_new_level(self, parents, level):
        children = {}
        base = self.n_leaves
        for i in parents.keys():
            sx, dx = self.__compute_children_value(parents[i], base+i)
            children[i*2]=sx
            children[(i*2)+1]=dx
        return children
        
    def __compute_children_value(self, seed_parent, index_parent):
        nodes = str(seed_parent) + self.salt + str(index_parent)
        sx, dx = expand_seed(int(nodes))  
        return sx, dx
    
    def __compute_seed_path(self, depth, list_index):
        if(depth > 1):
            list_index_next_level= list(filter(lambda x: (x % 2 == 0 and x + 1 in list_index) or (x % 2 != 0 and x - 1 in list_index), list_index)) 
            list_index = list(filter(lambda x: x not in list_index_next_level, list_index)) 
            list_parent = sorted(list(set(map(lambda elem: (elem // 2), list_index_next_level)))) 
            if len(list_index)>0:
                self.seed_path[depth] = dict(map(lambda x: (x, self.tree[depth][x]), list_index)) 
            if len(list_parent)>0:
                self.__compute_seed_path(depth-1, list_parent) 
    
    def __get_required_leaves_from_seed_path(self, seed_path):
        if len(seed_path.keys())>1:
            index = min(seed_path.keys())
            current_nodes=seed_path.pop(index)
            recomputed_children = self.__recompute_new_level(current_nodes, index)
            new_index=min(seed_path.keys())
            children = seed_path[new_index]
            merged_children = {**children, **recomputed_children} 
            seed_path[new_index] = dict(sorted(merged_children.items()))
            return self.__get_required_leaves_from_seed_path(seed_path)
        else:
            index, current_nodes = seed_path.popitem()
            return current_nodes


            