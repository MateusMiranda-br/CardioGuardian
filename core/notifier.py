# core/notifier.py

import requests
import streamlit as st

def send_telegram_alert(message: str):
    """
    Envia uma mensagem para o Telegram configurado no secrets.toml.
    Retorna True se sucesso, False se falha.
    """
    try:
        # Carrega as credenciais
        token = st.secrets["telegram"]["bot_token"]
        chat_id = st.secrets["telegram"]["chat_id"]
        
        # Monta a URL da API do Telegram
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        # Dados da mensagem
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown" # Permite usar negrito, itálico, etc.
        }
        
        # Envia a requisição
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return True
        else:
            print(f"Erro Telegram: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        return False