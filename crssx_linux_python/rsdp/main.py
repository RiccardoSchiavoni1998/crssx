import os
from sage.all import *
from signer import Signer
from verifier import Verifier
from utils import *
from dotenv import load_dotenv
load_dotenv() 


p = int(os.environ.get('p'))
n = int(os.environ.get('n'))
k = int(os.environ.get('k'))
w = int(os.environ.get('w'))
t = int(os.environ.get('t'))
z = int(os.environ.get('z'))
lambda_ = int(os.environ.get('lambda_'))

r=n-k
lev_leaf=log(t,2)
Fp=GF(p)
Fz=GF(z)
Fp_set=Set(Fp)
Fp_star=Fp_set.difference([0])


seed_sk, seed_pk, s = key_gen(p, z, n, k, r, Fp, Fz)
signer = Signer()
signature = signer.sign_msg("buonasera", seed_sk, p, z, n, w, k, r, t, lev_leaf, Fp, Fz, Fp_set, Fp_star)
verifier = Verifier()
esito = verifier.check_sign(seed_pk, s, "buonasera", signature, p, z, n, w, k, r, t, lev_leaf, Fp, Fz, Fp_star)
print(esito)