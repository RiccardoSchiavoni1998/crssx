# crssx
Dubbi principali:

PREMESSA: HO UTILIZZATO LAMBDA = 128 PERCHè ALESSIO PAVONI HA FATTO IN QUEL MODO


- Alessio utilizza sempre la funzione set_random_seed() per generare il seed e initial_seed() per recuperarlo.
set_random_seed() dovrebbe utilizzare una sorta di generatore di entropia all'interno del computer quindi il valore è sempre casuale.
controllando seed_sk.bit_length() mi restiuisce un valore da 125 a 128 

-----------------------------------------------
DOMANDA 1: 
partendo dal presupposto che .bit_length() restituisca la dimensione in bit seed_sk (mi sembrerebbe assurdo il contrario) dobbiamo controllare che la lunghezza del seed sia esattamente 128?
------------------------------------------------

Una volta generato un seed in questo modo:
set_random_seed()
seed = initial_seed()

quando richiamo set_random_seed(seed) ottengo di nuovo lo stesso seed.

Di seguito inoltre le seguenti funzioni:
1) random_matrix(Domain, n_rows, n_columns)
2) random_vector(Domain, nelems)
3) getrandbits(nbits)

quanto imposto il seed  set_random_seed(seed_sk) mi generano sempre le stesse sequenze di elementi random:

x1 = getrandbits(128)
x2 = getrandbits(128)
V1 = random_matrix(GF(2), 2, 2))
V2 = random_matrix(GF(2), 2, 2))

(Avrò sempre lo stesso x1, x2, V1, v2 
ma x1 e x2 sono diversi tra loro e analogamente V1 e V2)

QUINDI:
per fare l'analogo di quello che nel codice C è il CSPRNG facciamo come segue:
per esempio 
quando devo generare la matrice V trasposta (la parte non sistematica di H trasposta) a partire dal seed pubblicoche nello pseudo codice è generata come 
V <- CSPRNG(Seedpk,Fp^(r x k)) 

Facciamo:
set_random_seed(seed_pk)
V = random_matrix(Fp, k, r)

(Analogamente per espandere un seed0 in due nuovi seed1 e seed2)
Faccio cosi
seed1 = getrandbits(128)
seed2 = getrandbits(128)

------------------------------------------------
DOMANDA 2:
è giusto questo utilizzo delle funzioni pseudorandomiche? 

------------------------------------------------
DOMANDA 3:
la funzione treeseed() di alessio pavoni per come l ha implementata restituisce M hash 
io l ho fatta seguendo il documento e mi genera dei seed di lunghezza 128
