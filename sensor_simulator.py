# sensor_simulator.py

import time
import random
from core.db_mock import add_heart_rate_data, initialize_db

def generate_bpm():
    """
    Gera um valor de BPM simulado.
    """
    prob = random.random()
    
    if prob < 0.05: # 5% de chance de Bradicardia
        return random.randint(40, 55)
    elif prob < 0.10: # 5% de chance de Taquicardia
        return random.randint(100, 130)
    else: # 90% de chance de ser normal
        return random.randint(65, 85)

def run_sensor():
    """
    Loop principal do sensor. (Versão SIMPLES)
    """
    print("--- Sensor CardioGuardian Ativado ---")
    print("Gerando dados de BPM a cada 2 segundos. Pressione CTRL+C para parar.")
    
    while True:
        try:
            bpm = generate_bpm()
            add_heart_rate_data(bpm)
            print(f"[{time.strftime('%H:%M:%S')}] Novo dado enviado: {bpm} BPM")
            
            time.sleep(2) 
            
        except KeyboardInterrupt:
            print("\n--- Sensor CardioGuardian Desativado ---")
            break
        except Exception as e:
            print(f"Erro no sensor: {e}")
            time.sleep(5) 

if __name__ == "__main__":
    initialize_db()
    run_sensor()