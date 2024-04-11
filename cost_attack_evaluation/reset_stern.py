import shutil
import json
import os

def copy_json_file(source_file, destination_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))+r"\optimization\results_opt"
        print(path)
        source_file = os.path.join(path, source_file)
        destination_file = os.path.join(path, destination_file)
        # Leggi il contenuto del file JSON
        with open(source_file, 'r') as file:
            json_data = json.load(file)

        # Crea una copia del contenuto
        copied_data = json_data

        # Salva la copia come nuovo file JSON
        with open(destination_file, 'w') as file:
            json.dump(copied_data, file, indent=4)

        print(f"File JSON '{source_file}' copiato come '{destination_file}' con successo.")
    
    except FileNotFoundError:
        print("File non trovato.")
    
    except json.decoder.JSONDecodeError:
        print("Errore nella decodifica del file JSON.")

# Esempio di utilizzo
source_file = 'stern_results.json'
destination_file = 'results_0.json'

copy_json_file(source_file, destination_file)