# app.py

import streamlit as st
from core.db_mock import initialize_db

# --- Configuração da Página ---
st.set_page_config(
    page_title="CardioGuardian - Home",
    page_icon="❤️",
    layout="wide"
)

# Inicializa o banco de dados mocado se ele não existir
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
2.  (Opcional) Instale as bibliotecas:
    ```bash
    pip install -r requirements.txt
    ```
3.  No **Terminal 1**, inicie o sensor:
    ```bash
    python sensor_simulator.py
    ```
4.  No **Terminal 2**, inicie o dashboard:
    ```bash
    python3 -m streamlit run app.py
    ```
5.  No menu lateral do seu navegador, clique em **"1_Dashboard"** para ver os dados em tempo real.
""")

st.sidebar.success("Navegue no menu acima.")