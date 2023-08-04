from utils import *
from seed_tree import SeedTree
from merkle_tree import MerkleTree

class Signer:

    def sign_msg(self, msg, seed_sk, p, z, n, w, k, r, t, lev_leaf, Fp, Fz, Fp_set, Fp_star):
        self.p = p
        self.n = n
        self.w = w
        self.z = z
        self.t = t
        self.r = r
        self.lev_leaf=lev_leaf
        self.Fp = Fp
        self.Fz = Fz
        self.g = get_generator(p, z, Fp)
        self.Fp_set = Fp_set
        self.Fp_star = Fp_star
        seed_e , seed_pk = expand_seed(seed_sk) 
        self.V = create_random_matrix(self.Fp, k, r, seed_pk)
        self.eta = create_random_vector(Fz, self.n, seed_e)
        self.__compute_commitment()
        self.__generate_first_challenge(msg)
        self.__generate_first_response()
        self.__generate_second_challenge()
        self.__generate_second_response()
        return self.__sign()

    def __compute_commitment(self):
        seed_m = generate_random_seed() 
        seed_salt = generate_random_seed()
        self.salt = hash_and_get_seed(seed_salt)
        self.seed_tree = SeedTree(self.t, self.lev_leaf, self.salt)
        self.seed_tree.make_tree(seed_m)
        self.seeds = self.seed_tree.get_leaves()
        list_cmt0 = [] 
        list_cmt1 = ""
        for i in range(0, self.t):
            seed_ui, seed_ei = expand_seed(self.seeds[i])
            eta_i = create_random_vector(self.Fz, self.n, seed_ei)
            sigma_i = self.eta-eta_i #sigma_i ∈ self.Fz^ns
            v = create_vEn(self.g, self.n, self.Fz, self.Fp, eta=sigma_i)
            ui = create_random_vector(self.Fp, self.n, seed_ui)
            u = component_wise_multiply(v, ui, self.Fp)
            st = u[0:self.r] + u[self.r:self.n]*self.V
            cmt0_i = hexhash(str(st) + str(sigma_i) + str(self.salt) + str(i))
            cmt1_i = hexhash(str(self.seeds[i]) + str(self.salt) + str(i))
            list_cmt0.append(cmt0_i) 
            list_cmt1=list_cmt1+cmt1_i
        #commitment 0
        self.merkle_tree = MerkleTree(self.t, self.lev_leaf)
        self.merkle_tree.make_tree(list_cmt0)
        c0 = self.merkle_tree.get_root()
        #commitment 1
        #input_c1 = "".join(map(str, list_cmt1))
        c1 = hexhash(list_cmt1) 
        #hash dei due commitment
        self.c01 = hexhash(c0+c1)

    def __generate_first_challenge(self, msg):
        hash_salt = convert_int_to_hash_string(self.salt)
        input_ch1 = hexhash(msg)+self.c01+hash_salt
        self.seed_ch1 = hash_and_get_seed(input_ch1)
        self.ch1 = create_vector_over_Fp_star(self.Fp_star, self.t, self.seed_ch1) 

    def __generate_first_response(self):
        #list_hash_yi=[]
        list_yi=""
        for seed_i, ch_i_1 in zip(self.seeds, self.ch1): #t round: rispota yi dipende da seed_i e ch_i_1
            seed_ui, seed_ei = expand_seed(seed_i) 
            ei = create_vEn(self.g, self.n, self.Fz, self.Fp, seed=seed_ei)
            ui = create_random_vector(self.Fp, self.n, seed_ui)
            yi = ui+(ch_i_1)*ei #calcolo risposta i-esima corrispondente all'elemento i-esmino del vettore ch1 
            list_yi=list_yi+str(yi)
            #hi = hexhash(str(yi))
            #list_hash_yi.append(hi)
        self.h = hexhash(list_yi)

    def __generate_second_challenge(self):#, seed_tree):
        input_ch2 = "".join(self.h)+str(self.seed_ch1)
        self.seed_ch2 = hash_and_get_seed(input_ch2)
        self.ch2 = generate_vector_fixed_hamming_w(self.w, self.t, self.seed_ch2)

    def __generate_second_response(self):#CONTROLLARE ORDINE
        index_1, index_0 = [], []
        #questi due vettori sono di lunghezza t-w ovvero i round corrisponenti agli indici in cui il vettore ch2=0
        self.rsp_ch0 = [] # self.Fp^n x self.Fz^m
        self.rsp_ch1 = [] # {0,1}^lambda
        #
        i = 0
        for seed_i, ch_i_2 in zip(self.seeds, self.ch2):
            if ch_i_2 == 1:#Challenge2 = 1
                index_1.append(i)  
                
            else: #Creo la risposta nel caso challenge2 = 0
                index_0.append(i)

                seed_ui, seed_ei = expand_seed(seed_i)
                #ricalcolo sigma i
                eta_i = create_random_vector(self.Fz, self.n, seed_ei)
                sigma_i = self.eta-eta_i #sigma_i ∈ self.Fz^ns
                #ricalcolo yi
                ei = create_vEn(self.g, self.n, self.Fz, self.Fp, seed_ei)
                ui = create_random_vector(self.Fp, self.n, seed_ui) 
                yi = ui+(self.ch1[i])*ei
                
                #risposta challenge 0
                self.rsp_ch0.append([yi, sigma_i]) 

                #risposta challenge 1
                cmt1_i = hexhash( str(seed_i) + str(self.salt) + str(i) )
                
                self.rsp_ch1.append(cmt1_i)

            i = i+1
            
        self.seed_tree.compute_seed_path(index_1)
        self.seed_path = self.seed_tree.get_seed_path()
        self.merkle_tree.compute_proof(index_0)
        self.merkle_proof = self.merkle_tree.get_merkle_proof()

    def __sign(self):
        signature = {}
        signature["salt"] = self.salt
        signature["c01"] = self.c01
        signature["ch2"] = self.seed_ch2
        signature["seed_path"] = self.seed_path
        signature["merkle_proof"] = self.merkle_proof
        signature["rsp_ch0"] = self.rsp_ch0
        signature["rsp_ch1"] = self.rsp_ch1
        #binary_signature = convert_object_to_binary_string(signature)
        #return binary_signature
        return signature