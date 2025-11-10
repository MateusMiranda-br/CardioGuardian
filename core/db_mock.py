# core/db_mock.py

import json
import os
import random
import time
from threading import RLock # <<< CORRIGIDO para RLock

# Nome do nosso arquivo de "banco de dados"
DB_FILE = "mock_db.json"

# Usamos RLock para permitir que a mesma thread adquira o lock
file_lock = RLock()

def initialize_db(max_entries=200):
    """
    Cria o arquivo JSON inicial se ele não existir.
    """
    with file_lock:
        if not os.path.exists(DB_FILE):
            print("Inicializando banco de dados mock...")
            initial_data = []
            current_time = int(time.time())
            for i in range(10):
                initial_data.append({
                    "timestamp": current_time - (10 - i),
                    "bpm": random.randint(65, 80)
                })
            
            db_content = {
                "user_profile": {
                    "name": "Usuário Teste",
                    "age": 65,
                    "conditions": ["Hipertensão"] # <<< ESTADO ORIGINAL (LISTA)
                },
                "heart_rate_history": initial_data,
                "max_entries": max_entries
            }
            
            with open(DB_FILE, 'w') as f:
                json.dump(db_content, f, indent=4)

def read_data():
    """
    Lê todos os dados do banco de dados JSON.
    """
    with file_lock:
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            initialize_db()
            with open(DB_FILE, 'r') as f:
                return json.load(f)

def add_heart_rate_data(new_bpm):
    """
    Adiciona um novo registro de BPM usando "escrita atômica".
    """
    with file_lock:
        data = read_data()
        
        history = data.get("heart_rate_history", [])
        max_entries = data.get("max_entries", 200)
        
        new_entry = {
            "timestamp": int(time.time()),
            "bpm": new_bpm
        }
        history.append(new_entry)
        
        if len(history) > max_entries:
            history.pop(0) 
            
        data["heart_rate_history"] = history
        
        # --- ESCRITA ATÔMICA (CORRIGIDA) ---
        temp_file = DB_FILE + ".tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=4)
            os.replace(temp_file, DB_FILE)
        except Exception as e:
            print(f"ERRO: Falha na escrita atômica do DB: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)