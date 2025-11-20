# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import altair as alt 
from core.db_mock import read_data
from core.anomaly_detector import detect_anomalies
from core.notifier import send_telegram_alert
from streamlit_autorefresh import st_autorefresh

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard - CardioGuardian",
    page_icon="🩺",
    layout="wide"
)

# --- Auto-Refresh ---
st_autorefresh(interval=2000, limit=None, key="dashboard_refresh")

# --- Inicialização de Estado (Controle de Notificações) ---
if "last_alert_timestamp" not in st.session_state:
    st.session_state["last_alert_timestamp"] = None

# --- Título ---
st.title("🩺 Dashboard de Monitoramento Inteligente")
st.caption("Executando análise de IA (Isolation Forest Multivariado) em tempo real.")

# --- 1. Carregar Dados ---
db_data = read_data()
history = db_data.get("heart_rate_history", [])
profile = db_data.get("user_profile", {})

if len(history) < 20: 
    st.warning("Aguardando coleta de dados... (mínimo de 20 pontos para análise)")
    st.stop()

# --- 2. Processamento de IA e Fuso Horário ---
df = pd.DataFrame(history)

# --- CORREÇÃO DE FUSO HORÁRIO (AQUI ESTÁ O AJUSTE) ---
# 1. Converte de segundos para datetime, informando que a origem é UTC
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
# 2. Converte do UTC para o horário de São Paulo/Brasília
df['timestamp'] = df['timestamp'].dt.tz_convert('America/Sao_Paulo')
# 3. Remove a informação técnica de fuso (+03:00) para limpar o gráfico, mantendo a hora correta
df['timestamp'] = df['timestamp'].dt.tz_localize(None)

# Detecta anomalias
df_processed = detect_anomalies(df.copy())

last_row = df_processed.iloc[-1]
last_bpm = last_row['bpm']
last_timestamp = last_row['timestamp']
last_anomaly_status = last_row['anomaly']


# --- LÓGICA DE NOTIFICAÇÃO TELEGRAM ---
if last_anomaly_status == -1:
    # Verifica se é um novo alerta comparando timestamps
    if st.session_state["last_alert_timestamp"] != last_timestamp:
        
        msg = (
            f"🚨 **ALERTA CARDIOGUARDIAN** 🚨\n\n"
            f"**Paciente:** {profile.get('name', 'N/A')}\n"
            f"**BPM:** {last_bpm}\n"
            f"**Status:** Anomalia de Padrão Detectada!\n"
            # O horário aqui já estará corrigido (-3h)
            f"**Horário:** {last_timestamp.strftime('%H:%M:%S')}"
        )
        
        enviou = send_telegram_alert(msg)
        
        if enviou:
            st.toast("Alerta enviado para o Telegram!", icon="📲")
            st.session_state["last_alert_timestamp"] = last_timestamp
        else:
            st.toast("Falha ao enviar alerta.", icon="❌")


# --- 3. Layout do Dashboard ---
col1, col2 = st.columns([1, 2]) 

with col1:
    st.subheader(f"Paciente: {profile.get('name', 'N/A')}")
    st.write(f"**Idade:** {profile.get('age', 'N/A')}")
    st.write(f"**Condições:** {profile.get('conditions', 'N/A')}")

    # --- Métrica Principal ---
    delta = None
    if len(df_processed) > 1:
        delta_val = last_bpm - df_processed.iloc[-2]['bpm']
        delta = f"{delta_val:+} BPM"
        
    st.metric(label="Batimento Atual (BPM)", value=last_bpm, delta=delta)
    
    # --- ÁREA DE ALERTAS ---
    st.subheader("Status do Paciente")
    
    if last_anomaly_status == -1:
        st.warning("ALERTA (Nível 2): Padrão de ritmo incomum detectado pela IA!", icon="🤖")
    elif last_bpm > 100:
        st.error("ALERTA (Nível 1): Taquicardia detectada!", icon="🚨")
    elif last_bpm < 60:
        st.warning("ALERTA (Nível 1): Bradicardia detectada!", icon="⚠️")
    else:
        st.success("Padrão de ritmo normal.", icon="✅")


with col2:
    st.subheader("Histórico Recente com Detecção de Anomalias")

    # --- GRÁFICO AVANÇADO (ALTAIR) ---
    base = alt.Chart(df_processed).encode(
        x=alt.X('timestamp:T', title='Horário')
    ).properties(
        title='Frequência Cardíaca (Anomalias em Vermelho)'
    )

    line = base.mark_line(color='blue').encode(
        y=alt.Y('bpm:Q', title='BPM')
    )

    points = base.mark_circle(size=60, opacity=1).encode(
        y=alt.Y('bpm:Q'),
        color=alt.condition(
            alt.datum.anomaly == -1, 
            alt.value('red'),      
            alt.value('blue')      
        ),
        tooltip=[
            alt.Tooltip('timestamp:T', title='Horário', format='%d/%m %H:%M:%S'), 
            alt.Tooltip('bpm', title='BPM'),
            alt.Tooltip('anomaly', title='Status (IA)')
        ]
    )

    chart = (line + points).interactive()

    st.altair_chart(chart, use_container_width=True, theme="streamlit")


st.divider()
st.subheader("Logs de Dados Brutos (IA Incluída)")
df_display = df_processed.rename(columns={'anomaly': 'Status IA (-1 = Anomalia)'})
# Formata a coluna de data para exibir bonito na tabela também
st.dataframe(
    df_display.tail(10).sort_values(by="timestamp", ascending=False).style.format({"timestamp": lambda t: t.strftime("%H:%M:%S")})
)