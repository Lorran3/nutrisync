
# versão resumida placeholder (interface avançada simulada)
import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(layout="wide")

st.title("NutriSync PRO")

st.subheader("Dashboard Inteligente")

st.metric("Pacientes ativos", 12)
st.metric("Precisam atenção", 3)
st.metric("Adesão média", "78%")

st.line_chart(pd.DataFrame({
    "Peso": [80,79,78,77,76],
    "Adesão": [60,70,75,80,78]
}))

st.subheader("Alertas automáticos")

st.warning("Paciente João: baixa proteína 3 dias")
st.error("Paciente Maria: acima das calorias")
st.success("Paciente Ana: ótima evolução")

st.subheader("Chat inteligente")
msg = st.text_input("Mensagem")
if st.button("Enviar"):
    st.success("Mensagem enviada")

st.subheader("Fotos refeições")
img = st.file_uploader("Upload foto")
if img:
    st.image(img)

st.subheader("Check-in diário")
if st.button("Fazer check-in"):
    st.success("Check-in registrado")

st.subheader("Relatório automático")
st.text("Paciente com boa evolução geral. Ajustar proteína.")

