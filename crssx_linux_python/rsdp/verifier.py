from utils import *
from seed_tree import SeedTree
from merkle_tree import MerkleTree

class Verifier:

    def check_sign(self, seed_pk, s, msg, sign, p, z, n, w, k, r, t, lev_leaf, Fp, Fz, Fp_star):
        self.n = n
        self.r = r
        self.w = w
        self.t = t
        self.lev_leaf = lev_leaf
        self.g = get_generator(p, z, Fp)
        self.Fp = Fp
        self.Fz = Fz
        self.Fp_star = Fp_star
        self.msg = msg
        self.V = create_random_matrix(Fp, k, r, seed_pk)
        self.s = s
        self.__retrieve_sign(sign)
        self.__retrive_challenges()
        return self.__recompute_and_verify_responses()
    

    def __retrieve_sign(self, signature):
        #signature = get_object_from_binary_string(sign)
        self.salt = signature["salt"]
        self.c01 = signature["c01"]
        self.seed_ch2 = signature["ch2"] 
        self.seed_path = signature["seed_path"]
        self.merkle_proof = signature["merkle_proof"]
        self.rsp_ch0 = signature["rsp_ch0"]
        self.rsp_ch1 = signature["rsp_ch1"]
        
    def __retrive_challenges(self):
        hash_salt = convert_int_to_hash_string(self.salt)
        hash_msg = hexhash(self.msg)
        #challenge1
        input_ch1 = hash_msg+self.c01+hash_salt
        self.seed_ch1 = hash_and_get_seed(input_ch1)
        self.ch1 = create_vector_over_Fp_star(self.Fp_star, self.t, self.seed_ch1)
        #challenge2
        self.ch2 = generate_vector_fixed_hamming_w(self.w, self.t, self.seed_ch2)
        #recupero indici
        #self.index_0 = []
        #self.index_1 = []
        #[self.index_1.append(i) if x == 1 else self.index_0.append(i) for i, x in enumerate(self.ch2)]
        index_1 = []
        for i, x in enumerate(self.ch2):
            if x == 1: index_1.append(i)
        seed_tree = SeedTree(self.t, self.lev_leaf, self.salt)
        #i seeds servono solo quando ch_2 = 1 
        self.seeds = seed_tree.get_required_leaves_from_seed_path(self.seed_path, index_1)
    
    def __recompute_and_verify_responses(self):
        c0={}
        list_cmt1=""
        list_y=""
        j=0
        for i, x in enumerate(self.ch2):
            if x ==1:
                seed_ui, seed_ei = expand_seed(self.seeds[i]) 
                #RICALCOLO RISPOSTA CHALLENGE 1 
                ei = create_vEn(self.g, self.n, self.Fz, self.Fp, seed=seed_ei)
                ui = create_random_vector(self.Fp, self.n, seed_ui)   
                yi = ui+(self.ch1[i])*ei
                list_y=list_y+str(yi)
                #RICALCOLO COMMITMENT 1
                #cmt1_i = hexhash(ui, ei, salt, i)
                cmt1_i = hexhash(str(self.seeds[i]) + str(self.salt) + str(i))
                list_cmt1=list_cmt1+cmt1_i
                #hi = hexhash(str(yi))
            else:
                [yi, sigma_i]=self.rsp_ch0[j]
                list_y=list_y+str(yi)
                #verificare sigma_i appartenga a G

                #RICALCOLO SIGMA TILDE 
                v = create_vEn(self.g, self.n, self.Fz, self.Fp, eta=sigma_i)
                yi_ = component_wise_multiply(v, yi, self.Fp)

                st = yi_[0:self.r] + yi_[self.r:self.n]*self.V - self.ch1[i]*self.s

                #RICALCOLO COMMITMENT 0 
                cmt0_i = hexhash(str(st)+str(sigma_i)+str(self.salt)+str(i))
                c0[i]=cmt0_i

                #ESTRAGGO COMMITMENT 1
                cmt1_i = self.rsp_ch1[j]
                list_cmt1=list_cmt1+cmt1_i
                j = j+1

        merkle_tree = MerkleTree(self.t, self.lev_leaf)
        
        recomputed_root = merkle_tree.recompute_root(self.merkle_proof, c0)
        recomputed_c1 = hexhash(list_cmt1) 
        
        recomputed_c01 = hexhash(recomputed_root+recomputed_c1)
        recomputed_h = hexhash(list_y)
        input_recomputed_ch2 = "".join(recomputed_h)+str(self.seed_ch1)
        recomputed_ch2 = hash_and_get_seed(input_recomputed_ch2)
        
        return recomputed_c01 == self.c01 and recomputed_ch2 == self.seed_ch2
            
        #h = hexhash(h1,...,hn)
        #c0 = hexhash(c01,...,c0t)
        #VerifyMerkleProof   

    
