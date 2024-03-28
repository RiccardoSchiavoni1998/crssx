#############################################################################################################################################################################################################################################
#################################################################################################### PARAMETERS OPTIMIZATION ################################################################################################################
#############################################################################################################################################################################################################################################

- SUB DIRECTORY NAME: cost_attack_evaluation
- Set params in cost_attack_evaluation\optimization\opt_config.json
     The json file contains the following fields:
     - ranges: ranges for parameters n, p, k
     - currentCategory: set 1, 2, or 3 to get both the correct security level and target size
     - rangeSetE2: ranges number of overlapping values (epsilon and delts) for BJMM 2LV on Set E
     - rangeSetShiftedE2: ranges number of overlapping values (epsilon and delts) for BJMM 2LV on Set Shifted E
     - verb: The evaulation prints both the current running attack and set of parameters if verb is set to True.
     - fast: Evaluation works more specifically with the rounding of weights and vector lengths on intermediate levels
     - num_workers: number of cups for parallel execution
     - list_attacks: list of attacks involved in the evaluation
     - new_execution : True if it is a new execution False if a previous execution is being taken up 
     - recovery_num : the number of files with the results of aborted execution

- The alogrithm works as follows:
     - Gets all the combinations of p,n,k,z according to the specified ranges
     - Filters out all the combinations such that n*log(p*z, 2) < 128*log(127*z, 2), latter assumed as the initial best solution
     - Filters out all the combinations such that Stern_Cost(p, n, k, z) < security_level
     - Filters out all the combinations such that BJMM_2LV(p, n, k, z) < security_level
     - Filters out all the combinations such that BJMM_3LV(p, n, k, z) < security_level
- Each result of sub evaluations is saved in json files in the directory ost_attack_evaluation\optimization\results_opt\ , with the following structure:

min_p = {...}

...
p_i : {

     "State": "To Do" \ "Finished",
     
     "Evaluations": [
     
         ...
         
         {
         
             "Params": {
                 "n": n_value,
                 "k": k_value,
                 "z": z_value,
                 "p": p_value
             }, 
             
             "Size": n*log(p*z, 2),
             
             "Failed": false / true,
             
             "Res": {
                        "Stern": ...
                        "Bjmm 2LV": ...
                        "Bjmm 3LV": ...
                   
                    }
         },
         
         ...
     ]
   
  }
  
...
max_p = {...}


  
        
  
  




















##############################################################################################################################################################################################################################################
#################################################################################################### REFERENCE CROSS PYTHON ##################################################################################################################
##############################################################################################################################################################################################################################################


PER ESEGUIRE SU LINUX:

crssx_linux_python/rspd
crssx_linux_python/rspd_g

(Sintesi di https://doc.sagemath.org/html/en/installation/conda.html)

1) Installare python e visual studio code
2) Comandi per installare sage
   -  curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh
   - sh Mambaforge-$(uname)-$(uname -m).sh
   
3) Creare ambiente d'esecuzione: mamba create -n sage sage python=X  (X versione python)
4) Mandare in esecuzione (posizionarsi sulla directory del progetto): mamba activate sage
5) Installare pacchetto per variabili d'ambiente: mamba install python-dotenv


PER ESEGUIRE SU WINDOWS:

Tutorial: https://www.youtube.com/watch?v=sXb58bIstIw



Variabili da valorizzare nel .env:
p=
n=
k=
w=
t=
z=
lambda_=

