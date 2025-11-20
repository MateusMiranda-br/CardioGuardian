# core/anomaly_detector.py

import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_RANDOM_STATE = 42
DEFAULT_CONTAMINATION = 0.1


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas características (features) de engenharia
    para o modelo de IA.
    """
    # 1. Média Móvel (Suavização de tendência - últimos 3 pontos)
    df['bpm_rolling_avg_3'] = df['bpm'].rolling(window=3, min_periods=1).mean()
    
    # 2. Variação (Taxa de Mudança - Diferença do anterior)
    df['bpm_diff'] = df['bpm'].diff().fillna(0)
    
    return df


def detect_anomalies(df_history: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe histórico, cria features, treina Isolation Forest 
    e retorna DataFrame com coluna 'anomaly'.
    """
    
    # 1. Verificação de Sanidade
    if df_history.empty or len(df_history) < 20:
        df_history['anomaly'] = 1
        return df_history

    # 2. Engenharia de Features
    df_with_features = create_features(df_history)
    
    # Define as features para o modelo (Multivariado)
    feature_columns = ['bpm', 'bpm_rolling_avg_3', 'bpm_diff']
    
    # Removemos a primeira linha que pode ter dados incompletos no diff
    features_data = df_with_features[feature_columns].tail(-1)
    
    if features_data.empty or len(features_data) < 20:
        df_history['anomaly'] = 1
        return df_history

    # 3. Instanciação do Modelo
    model = IsolationForest(
        contamination=DEFAULT_CONTAMINATION,
        random_state=MODEL_RANDOM_STATE
    )

    # 4. Treinamento
    model.fit(features_data)

    # 5. Predição
    predictions = model.predict(features_data)

    # 6. Resultado
    # Adicionamos '1' (normal) para o primeiro ponto que pulamos
    final_predictions = [1] + list(predictions)
    
    df_history['anomaly'] = final_predictions

    return df_history