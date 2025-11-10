# core/anomaly_detector.py

import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_RANDOM_STATE = 42
DEFAULT_CONTAMINATION = 0.1


def detect_anomalies(df_history: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um DataFrame com o histórico de BPM, treina um modelo
    Isolation Forest e retorna o DataFrame com uma nova coluna 'anomaly'.
    
    A coluna 'anomaly' terá os valores:
     -  1: Ponto de dado normal (inlier)
     - -1: Ponto de dado anômalo (outlier)
    """
    
    # 1. Verificação de Sanidade
    if df_history.empty or len(df_history) < 20:
        df_history['anomaly'] = 1
        return df_history

    # 2. Preparação dos Dados
    features = df_history[['bpm']]

    # 3. Instanciação do Modelo
    model = IsolationForest(
        contamination=DEFAULT_CONTAMINATION,
        random_state=MODEL_RANDOM_STATE
    )

    # 4. Treinamento
    model.fit(features)

    # 5. Predição
    predictions = model.predict(features)

    # 6. Resultado
    df_history['anomaly'] = predictions

    return df_history