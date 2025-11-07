# core/db_mock.py

import json
import os
import random
import time
from threading import RLock

# Nome do nosso arquivo de "banco de dados"
DB_FILE = "mock_db.json"

# Um Lock é essencial para prevenir que o sensor e o dashboard
# tentem ler/escrever o arquivo AO MESMO TEMPO, o que corromperia o JSON.
file_lock = RLock()

def initialize_db(max_entries=200):
    """
    Cria o arquivo JSON inicial se ele não existir,
    com uma estrutura de dados de exemplo.
    """
    with file_lock:
        if not os.path.exists(DB_FILE):
            print("Inicializando banco de dados mock...")
            # Começamos com alguns dados normais
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
                    "conditions": ["Hipertensão"]
                },
                "heart_rate_history": initial_data,
                "max_entries": max_entries # Define o limite de dados a guardar
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
            # Se o arquivo estiver corrompido ou não existir, reinicia.
            initialize_db()
            with open(DB_FILE, 'r') as f:
                return json.load(f)

def add_heart_rate_data(new_bpm):
    """
    Adiciona um novo registro de BPM ao banco de dados usando
    um método de "escrita atômica" para evitar race conditions.
    """
    with file_lock:
        # 1. Lê os dados atuais (a função read_data não muda)
        data = read_data()
        
        history = data.get("heart_rate_history", [])
        max_entries = data.get("max_entries", 200)
        
        # 2. Prepara os novos dados em memória
        new_entry = {
            "timestamp": int(time.time()),
            "bpm": new_bpm
        }
        history.append(new_entry)
        
        if len(history) > max_entries:
            history.pop(0) # Remove o registro mais antigo
            
        data["heart_rate_history"] = history
        
        # --- INÍCIO DA CORREÇÃO (ESCRITA ATÔMICA) ---
        
        # 3. Define um nome de arquivo temporário
        temp_file = DB_FILE + ".tmp"
        
        try:
            # 4. Escreve os dados completos no arquivo temporário
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            # 5. Renomeia (move) o arquivo temporário para o real.
            # Esta operação é "atômica" e instantânea.
            os.replace(temp_file, DB_FILE)
            
        except Exception as e:
            print(f"ERRO: Falha na escrita atômica do DB: {e}")
            # Se algo der errado, limpa o arquivo temporário
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        # --- FIM DA CORREÇÃO ---