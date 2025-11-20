# app.py

import streamlit as st
from core.db_mock import initialize_db

# --- Configuração da Página ---
st.set_page_config(
    page_title="CardioGuardian - Home",
    page_icon="❤️",
    layout="wide"
)

# Garante que o DB existe ao abrir o app
initialize_db()

# --- Conteúdo da Página ---
st.title("❤️ Bem-vindo ao CardioGuardian")
st.caption("Monitoramento Cardíaco Inteligente (Versão de Simulação Local)")
st.divider()

st.header("Sobre o Projeto")
st.write("""
O CardioGuardian é uma plataforma de TCC para monitoramento de dados
cardíacos, utilizando um biossensor simulado, um banco de dados local (JSON) 
e modelos de Inteligência Artificial para detecção de anomalias.
""")

st.subheader("Como usar esta demonstração:")
st.markdown("""
1.  **Abra dois terminais** na pasta `cardioguardian`.
2.  No **Terminal 1**, inicie o sensor:
    `python sensor_simulator.py`
3.  No **Terminal 2**, inicie o dashboard:
    `python3 -m streamlit run app.py`
4.  Navegue pelo menu lateral para ver o Dashboard ou Editar o Perfil.
""")

st.sidebar.success("Navegue no menu acima.")