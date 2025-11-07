# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import time
from core.db_mock import read_data
from streamlit_autorefresh import st_autorefresh # <<< NOSSA NOVA IMPORTAÇÃO

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard - CardioGuardian",
    page_icon="🩺",
    layout="wide"
)

# --- Função de Auto-Refresh ---
# ESTA É A NOVA FORMA: Usamos um componente dedicado.
# Ele rodará a cada 2000ms (2 segundos) e nunca vai parar (limit=None).
st_autorefresh(interval=2000, limit=None, key="dashboard_refresh")


# --- Título ---
st.title("🩺 Dashboard de Monitoramento")
st.caption("Os dados estão sendo lidos do `mock_db.json` em tempo real.")

# --- Carregar Dados ---
db_data = read_data()
history = db_data.get("heart_rate_history", [])
profile = db_data.get("user_profile", {})

if not history:
    st.warning("Nenhum dado de frequência cardíaca encontrado. O sensor está rodando?")
    st.stop()

# Converte o histórico para um DataFrame Pandas para fácil manipulação
df = pd.DataFrame(history)
# Converte timestamp (segundos) para datetime legível
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')


# --- Layout do Dashboard ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Paciente: {profile.get('name', 'N/A')}")
    st.write(f"**Idade:** {profile.get('age', 'N/A')}")
    st.write(f"**Condições:** {', '.join(profile.get('conditions', []))}")

    # Pega o último batimento registrado
    last_bpm = df.iloc[-1]['bpm']
    
    # --- Métrica Principal ---
    # Usamos o delta para mostrar a mudança do penúltimo para o último
    delta = None
    if len(df) > 1:
        delta_val = last_bpm - df.iloc[-2]['bpm']
        delta = f"{delta_val:+} BPM"
        
    st.metric(label="Batimento Atual (BPM)", value=last_bpm, delta=delta)
    
    # --- Lógica de Alerta Heurístico (Passo 1 da IA) ---
    if last_bpm > 100:
        st.error("ALERTA: Taquicardia detectada!", icon="🚨")
    elif last_bpm < 60:
        st.warning("ALERTA: Bradicardia detectada!", icon="⚠️")
    else:
        st.success("Ritmo cardíaco normal.", icon="✅")


with col2:
    st.subheader("Histórico Recente (Últimos 200 registros)")
    
    # --- Gráfico de Linha ---
    # Queremos o timestamp no eixo X e o BPM no eixo Y
    chart_data = df.set_index('timestamp')['bpm']
    
    st.line_chart(chart_data, height=350)

st.divider()
st.subheader("Logs de Dados Brutos (Últimos 10)")
st.dataframe(df.tail(10).sort_values(by="timestamp", ascending=False))