import os
import shutil

#Percorsi delle directory e dei file
base_dir = '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/tiff_try'
train_txt_path = '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/splits/train.txt'
val_txt_path = '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/splits/val.txt'


# Nuove cartelle di destinazione
train_set_dir ='/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/train_set'
val_set_dir = "/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/val_set"
test_set_dir = "/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/test_set"

# Crea le nuove cartelle se non esistono
os.makedirs(train_set_dir, exist_ok=True)
os.makedirs(val_set_dir, exist_ok=True)
os.makedirs(test_set_dir, exist_ok=True)

# Leggi i nomi dei file da train.txt e converti i nomi
with open(train_txt_path, 'r') as f:
    train_files = [line.strip().replace("PS-RGBNIR", "Buildings").replace(".tif", "_mask.tiff") for line in f]

# Leggi i nomi dei file da val.txt e converti i nomi
with open(val_txt_path, 'r') as f:
    val_files = [line.strip().replace("PS-RGBNIR", "Buildings").replace(".tif", "_mask.tiff") for line in f]

# Funzione per spostare i file nella cartella di destinazione
def move_files(file_list, dest_dir):
    for file_name in file_list:
        src_path = os.path.join(base_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)
        # Verifica se il file è già stato spostato
        if not os.path.exists(dest_path):
            if os.path.exists(src_path):
                shutil.move(src_path, dest_path)
            else:
                print(f"File not found: {src_path}")
        else:
            print(f"File already exists in destination: {dest_path}")

# Sposta i file di addestramento nella cartella train_set
move_files(train_files, train_set_dir)

# Sposta i file di validazione nella cartella val_set
move_files(val_files, val_set_dir)

# Identifica i file rimanenti come file di test
remaining_files = [f for f in os.listdir(base_dir) if (f.endswith('.tiff')) and f not in train_files and f not in val_files]

# Sposta i file di test nella cartella test_set
move_files(remaining_files, test_set_dir)

print("File riorganizzati con successo.")

#Definisci le coppie di directory
directory_pairs = [
    ('/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/PS-RGBNIR/train_set', '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/train_set'),
    ('/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/PS-RGBNIR/val_set', '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/val_set'),
    ('/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/PS-RGBNIR/test_set', '/Users/francescotorella/Library/CloudStorage/GoogleDrive-torella.1984820@studenti.uniroma1.it/Il mio Drive/progettoLabAi3/train/mask/test_set')
]

def get_base_filename(file_name, mask=False):
    """
    Rimuove il suffisso specifico e l'estensione del file per ottenere il nome base.
    Sostituisce 'Buildings' con 'PS-RGBNIR' se mask è True.
    """
    if mask:
        return file_name.replace('_mask.tiff', '').replace('Buildings', 'PS-RGBNIR')
    else:
        return file_name.replace('.tif', '')

def check_correspondence(dirA, dirB):
    """
    Controlla i file nelle directory A e B e stampa i file per cui non è stata trovata una corrispondenza.
    """
    filesA = [f for f in os.listdir(dirA) if f.endswith('.tif')]
    filesB = [f for f in os.listdir(dirB) if f.endswith('.tiff')]
    
    base_filesA = {get_base_filename(f) for f in filesA}
    base_filesB = {get_base_filename(f, mask=True) for f in filesB}
    
    for fileA in filesA:
        base_fileA = get_base_filename(fileA)
        corresponding_fileB = base_fileA + '.tiff'

        if base_fileA not in base_filesB:
            print(f"No correspondence for {fileA, base_fileA} in {dirB}")
    
    for fileB in filesB:
        base_fileB = get_base_filename(fileB, mask=True)
        corresponding_fileA = base_fileB + '.geojson'
        if base_fileB not in base_filesA:
            print(f"No correspondence for {fileB, base_fileB} in {dirA}")

# Esegui il controllo per ciascuna coppia di directory
for dirA, dirB in directory_pairs:
    print(f"Checking correspondence between {dirA} and {dirB}")
    check_correspondence(dirA, dirB)
    print()