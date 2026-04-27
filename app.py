
import streamlit as st

st.set_page_config(page_title="NutriSync", layout="centered")

st.title("🥗 NutriSync")

st.write("Seu controle diário simples")

peso = st.number_input("Peso (kg)", 80.0)
altura = st.number_input("Altura (cm)", 180.0)

meta_calorias = peso * 30
meta_proteina = peso * 2

st.subheader("Metas")
st.write(f"🔥 Calorias: {int(meta_calorias)}")
st.write(f"🥩 Proteína: {int(meta_proteina)}g")

st.subheader("Hoje")

cal = st.number_input("Calorias hoje", 0)
prot = st.number_input("Proteína hoje", 0)

st.progress(min(cal/meta_calorias,1.0))
st.write(f"{cal}/{int(meta_calorias)} kcal")

st.progress(min(prot/meta_proteina,1.0))
st.write(f"{prot}/{int(meta_proteina)} g")

if prot < meta_proteina:
    st.warning("Come mais proteína 👊")
else:
    st.success("Boa, bateu proteína!")

if cal > meta_calorias:
    st.error("Passou das calorias")
else:
    st.success("Tá dentro!")
