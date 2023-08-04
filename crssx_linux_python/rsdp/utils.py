from sage.all import *
import random
import hashlib

def generate_random_seed():
    set_random_seed()
    return initial_seed()

def set_seed(seed):
    set_random_seed(seed)
    return initial_seed()

def hash_and_get_seed(input):
    hash = hashlib.sha256(str(input).encode()).digest()
    seed = int.from_bytes(hash, 'big')
    return seed

def hexhash(input):
    return hashlib.sha256(input.encode()).hexdigest()

def convert_int_to_hash_string(input):
    return input.to_bytes((input.bit_length() + 7) // 8, 'big').hex()

def expand_seed(seed_init):
    seed_str = str(seed_init)
    seeds = hashlib.sha256(seed_str.encode()).digest()
    
    seed_1 = seeds[:16] #i primi 16 byte
    seed_2 = seeds[16:] #gli ultimi 16 byte
    
    seed_1 = int.from_bytes(seed_1, 'big')
    seed_2 = int.from_bytes(seed_2, 'big')
    
    return seed_1, seed_2

#Creo Generatore g del Campo E
def get_generator(p, z, Fp):
    assert is_prime(p),"p is not prime!"
    assert (p-1)%z == 0, "z does not divide p-1!"
    alpha = Fp.primitive_element()
    #non ricordo perchè exp e g sono scelti secondo questa logica
    exp = (p-1)/z
    g = alpha**exp
    return g

def create_random_vector(domain, n_elems, seed):
    set_seed(seed)
    return random_vector(domain, n_elems)

def create_random_matrix(domain, n_rows, n_columns, seed):
    set_seed(seed)
    M = random_matrix(domain, n_rows, n_columns)
    return M

#Creo vettore errore con elementi in E e lunghezza V 
def create_vEn(g, n, Fz, Fp, seed=0, eta=[]):
    e = vector(Fp, n)
    if len(eta)==0:
        eta = create_random_vector(Fz, n, seed)
    for i in range(0, n):#range check
        e[i] = (g**eta[i])
    return e

def create_vector_over_Fp_star(Fp_star, t, seed):
    set_random_seed(seed)
    return [Fp_star.random_element() for i in range(t)]

def generate_vector_fixed_hamming_w(w, t, seed):
    random.seed(seed)
    vector = [0] * t
    indices = random.sample(range(t), w)
    for index in indices:
        vector[index] = 1
    return vector

def component_wise_multiply(v1, v2, Fp):
    if len(v1) != len(v2):
        raise ValueError("I vettori devono avere la stessa dimensione")
    result = vector(Fp, len(v1))  # Crea un nuovo vettore per i risultati
    for i in range(len(v1)):
        result[i] = v1[i] * v2[i]  # Moltiplica gli elementi corrispondenti
    
    return result

#GENERAZIONE CHIAVI
def key_gen(p, z, n, k, r, Fp, Fz):
    seed_sk = generate_random_seed() 
    seed_e , seed_pk = expand_seed(seed_sk)
    V = create_random_matrix(Fp, k, r, seed_pk) 
    g = get_generator(p, z, Fp)
    e = create_vEn(g, n, Fz, Fp, seed=seed_e) #e=g^η
    s = e[0:r] + e[r:n]*V
    return seed_sk, seed_pk, s

	
