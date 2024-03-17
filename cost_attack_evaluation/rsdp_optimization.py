#from utils_optimization import init_params, get_params, update_data, find_opt_values
from utils_optimization import optimize
import concurrent.futures

num_workers = 8 #NUMERO DI PROCESSI IN ESECUZIONE PARALLELA

verb = False #TRUE SE VUOI VEDERE QUALI COMBINAZIONI STA VALUTANDO

#SCEGLIERE ATTACCHI DA VALUTARE
list_attacks = ["Stern", "Bjmm 2LV", "Bjmm 3LV"]

#SE STOPPI E VUOI RIPRENDERE DA DOVE HAI STOPPATO SETTA (GLI ATTACCHI DEVONO ESSERE LI STESSI):
#new_execution = False
#recovery_num = numero ultimo file (i file sono nominati results_ + intero progressivo)
new_execution = True
recovery_num = 0



def main(list_attacks, num_workers, verb, new_execution, recovery_num):
    optimize(list_attacks, num_workers, verb, new_execution, recovery_num)
    

if __name__ == '__main__':
    main(list_attacks, num_workers, verb, new_execution, recovery_num)