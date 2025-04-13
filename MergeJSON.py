import json

# Nomi dei file JSON da unire
file1 = "datasetChats.json"
file2 = "datasetConversation.json"
output_file = "dataset.json"

def load_json(file_path):
    """Carica un file JSON e restituisce i dati."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Errore: Il file '{file_path}' non esiste.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Errore: Il file '{file_path}' non è un JSON valido.")
        return None

def save_json(data, file_path):
    """Salva i dati in un file JSON."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ File '{file_path}' salvato con successo!")

def merge_json(file1, file2, output_file):
    """Unisce due file JSON in uno."""
    # Carica i dati dai due file
    data1 = load_json(file1)
    data2 = load_json(file2)

    if data1 is None or data2 is None:
        return  # Interrompi l'esecuzione se uno dei file non è valido

    # Unisci i dati
    if isinstance(data1, list) and isinstance(data2, list):
        merged_data = data1 + data2  # Unisci le liste
    elif isinstance(data1, dict) and isinstance(data2, dict):
        merged_data = {**data1, **data2}  # Unisci i dizionari
    else:
        print("❌ Errore: I file JSON non hanno lo stesso formato (entrambi devono essere liste o dizionari).")
        return

    # Salva i dati uniti in un nuovo file JSON
    save_json(merged_data, output_file)

# Esegui la funzione per unire i file JSON
merge_json(file1, file2, output_file)