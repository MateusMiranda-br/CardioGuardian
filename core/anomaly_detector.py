# core/anomaly_detector.py

import pandas as pd
from sklearn.ensemble import IsolationForest

# Decisão de Arquitetura:
# Usaremos um "random_state" fixo. Isso garante que o modelo
# dê os MESMOS resultados toda vez que for treinado com os MESMOS dados.
# Essencial para depuração e consistência.
MODEL_RANDOM_STATE = 42

# Decisão de Arquitetura:
# 'contamination' é o hiperparâmetro mais importante.
# Ele informa ao modelo qual a "proporção esperada" de anomalias
# nos dados (ex: 0.1 = 10%).
# Como nosso sensor_simulator.py foi programado para gerar
# anomalias (taquicardia/bradicardia) 10% das vezes,
# usar 0.1 é um ponto de partida ideal e logicamente sólido.
DEFAULT_CONTAMINATION = 0.1


def detect_anomalies(df_history: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um DataFrame com o histórico de BPM, treina um modelo
    Isolation Forest e retorna o DataFrame com uma nova coluna 'anomaly'.
    
    A coluna 'anomaly' terá os valores:
     -  1: Ponto de dado normal (inlier)
     - -1: Ponto de dado anômalo (outlier)
    """
    
    # --- 1. Verificação de Sanidade ---
    # O modelo não pode ser treinado com poucos dados.
    # Vamos definir um mínimo de, por exemplo, 20 pontos.
    if df_history.empty or len(df_history) < 20:
        # Se não temos dados suficientes, apenas retorne o df
        # marcando tudo como normal (1).
        df_history['anomaly'] = 1
        return df_history

    # --- 2. Preparação dos Dados (Feature Engineering) ---
    # O scikit-learn espera os dados em um formato 2D.
    # Por enquanto, nossa única "feature" é o próprio BPM.
    features = df_history[['bpm']]

    # --- 3. Instanciação do Modelo ---
    model = IsolationForest(
        contamination=DEFAULT_CONTAMINATION,
        random_state=MODEL_RANDOM_STATE
    )

    # --- 4. Treinamento ---
    # O modelo "aprende" o que é um padrão normal
    # com base nos dados fornecidos.
    model.fit(features)

    # --- 5. Predição ---
    # O modelo agora classifica todos os pontos de dados.
    # Ele retorna um array de 1 (normal) e -1 (anomalia).
    predictions = model.predict(features)

    # --- 6. Resultado ---
    # Adicionamos essas predições como uma nova coluna
    # ao nosso DataFrame original.
    df_history['anomaly'] = predictions

    return df_history