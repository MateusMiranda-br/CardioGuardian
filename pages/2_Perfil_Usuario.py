# pages/2_Perfil_Usuario.py

import streamlit as st
from core.db_mock import read_data, update_user_profile

st.set_page_config(
    page_title="Perfil do Paciente - CardioGuardian",
    page_icon="👤",
    layout="centered"
)

st.title("👤 Perfil do Paciente")
st.caption("Edite as informações do paciente monitorado.")

# --- 1. Carregar Dados ---
try:
    db_data = read_data()
    current_profile = db_data.get("user_profile", {})
except Exception as e:
    st.error(f"Erro ao carregar o perfil do banco de dados: {e}")
    current_profile = {}

# --- 2. Formulário ---
with st.form(key="profile_form"):
    st.subheader("Informações Demográficas")
    
    name = st.text_input(
        "Nome do Paciente", 
        value=current_profile.get("name", "")
    )
    
    age = st.number_input(
        "Idade", 
        min_value=0, 
        max_value=120, 
        value=current_profile.get("age", 0),
        step=1
    )
    
    st.subheader("Informações Médicas")
    
    conditions = st.text_area(
        "Condições Médicas (separadas por vírgula)",
        value=current_profile.get("conditions", ""),
        height=100
    )
    
    submitted = st.form_submit_button("Salvar Alterações")

# --- 3. Salvar ---
if submitted:
    try:
        new_profile_data = {
            "name": name,
            "age": age,
            "conditions": conditions
        }
        
        update_user_profile(new_profile_data)
        
        st.success("Perfil atualizado com sucesso!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Erro ao salvar o perfil: {e}")