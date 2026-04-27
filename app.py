
import streamlit as st
import pandas as pd
from datetime import datetime
import json
from pathlib import Path

st.set_page_config(
    page_title="NutriSync",
    page_icon="NS",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path("nutrisync_data.json")

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #f5f8f4;
    --dark: #12372a;
    --dark2: #0b271e;
    --green: #1f8f5f;
    --green2: #176f49;
    --soft: #eaf7ef;
    --text: #13231c;
    --muted: #6f7d75;
    --line: #dfe8e1;
    --white: #ffffff;
}

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(31,143,95,.13), transparent 30%),
        linear-gradient(180deg, #f8fbf6 0%, #edf5ee 100%);
    color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12372a 0%, #071f18 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 26px; }

.side-logo {
    color: white;
    font-size: 31px;
    font-weight: 900;
    letter-spacing: -.9px;
    margin-bottom: 3px;
}
.side-logo span { color: #86efac; }
.side-sub {
    color: #b7e8ca;
    font-size: 13px;
    margin-bottom: 22px;
}

.nav-btn button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    border-radius: 15px !important;
    padding: 13px 15px !important;
    margin: 3px 0 !important;
    background: rgba(255,255,255,.07) !important;
    color: #ecfdf5 !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    font-weight: 750 !important;
    box-shadow: none !important;
}
.nav-btn button:hover {
    background: rgba(134,239,172,.17) !important;
    color: white !important;
}
.nav-active {
    background: linear-gradient(135deg, #1f8f5f, #176f49);
    color: white;
    border-radius: 15px;
    padding: 13px 15px;
    margin: 7px 0;
    font-weight: 850;
    box-shadow: 0 12px 24px rgba(31,143,95,.25);
}

input, textarea, select,
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] > div {
    color: #13231c !important;
    background-color: #ffffff !important;
    border-color: #dbe7df !important;
    border-radius: 14px !important;
}
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] div,
[data-baseweb="select"] span,
[data-baseweb="popover"] div,
[data-baseweb="menu"] div {
    color: #13231c !important;
    background-color: #ffffff !important;
}
[data-baseweb="popover"], [data-baseweb="menu"] { background-color: #ffffff !important; }

label, .stTextInput label, .stNumberInput label, .stSelectbox label,
.stTextArea label, .stMultiSelect label, .stSlider label {
    color: #263d32 !important;
    font-weight: 800 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] { background: transparent !important; }

.hero {
    background: linear-gradient(135deg, #12372a 0%, #1f8f5f 100%);
    color: white;
    border-radius: 32px;
    padding: 30px;
    box-shadow: 0 24px 58px rgba(18,55,42,.22);
    min-height: 164px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    width: 245px;
    height: 245px;
    border-radius: 999px;
    right: -70px;
    top: -95px;
    background: rgba(255,255,255,.10);
}
.hero h1 {
    color: white;
    margin: 0;
    font-size: 35px;
    font-weight: 900;
    letter-spacing: -1px;
}
.hero p {
    color: rgba(255,255,255,.84);
    font-weight: 600;
    max-width: 780px;
}

.card {
    background: rgba(255,255,255,.96);
    border: 1px solid #dfe8e1;
    border-radius: 26px;
    padding: 22px;
    box-shadow: 0 16px 40px rgba(18,55,42,.075);
    min-height: 126px;
}
.card-title {
    color: #12372a;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 6px;
}
.muted {
    color: #6f7d75;
    font-size: 14px;
    font-weight: 600;
}
.kpi-label {
    color: #6f7d75;
    font-size: 12px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .45px;
}
.kpi-value {
    color: #12372a;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -.8px;
    margin-top: 7px;
}
.kpi-foot {
    color: #1f8f5f;
    font-size: 13px;
    font-weight: 850;
    margin-top: 8px;
}
.meal {
    background: white;
    border: 1px solid #dfe8e1;
    border-radius: 22px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 10px 25px rgba(18,55,42,.05);
}
.meal-head {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: start;
}
.meal-title {
    color: #12372a;
    font-weight: 900;
    font-size: 18px;
}
.meal-time {
    background: #eaf7ef;
    color: #176f49;
    padding: 7px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
}
.badge {
    display: inline-block;
    background: #eef8f2;
    color: #176f49;
    border: 1px solid #cdeedb;
    border-radius: 999px;
    padding: 6px 10px;
    margin: 9px 5px 0 0;
    font-size: 12px;
    font-weight: 900;
}
.option-card {
    background: #fbfdfb;
    border: 1px solid #dfe8e1;
    border-radius: 18px;
    padding: 14px;
    margin: 10px 0;
}
.option-name { font-weight: 900; color: #12372a; }
.ok-box {
    background: #eaf7ef;
    color: #166534;
    border: 1px solid #bce7cc;
    border-radius: 17px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}
.warn-box {
    background: #fff7ed;
    color: #9a3412;
    border: 1px solid #fed7aa;
    border-radius: 17px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}
.danger-box {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 17px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}
.stButton > button {
    border-radius: 14px !important;
    border: none !important;
    background: #1f8f5f !important;
    color: white !important;
    font-weight: 850 !important;
    padding: 12px 18px !important;
    box-shadow: 0 10px 22px rgba(31,143,95,.18) !important;
}
.stButton > button:hover {
    background: #176f49 !important;
    color: white !important;
}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dfe8e1;
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 14px 34px rgba(18,55,42,.07);
}
[data-testid="stMetricLabel"] * { color: #6f7d75 !important; font-weight: 800 !important; }
[data-testid="stMetricValue"] { color: #12372a !important; font-weight: 900 !important; }
.stProgress > div > div > div > div { background-color: #1f8f5f !important; }
hr { border: none; border-top: 1px solid #dfe8e1; margin: 20px 0; }

@media(max-width: 800px) {
    .hero h1 { font-size: 28px; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================
# BASE
# =========================
DEFAULT_FOODS = [
    {"nome": "Pão francês", "grupo": "Carboidrato", "porcao": "1 unidade", "cal": 135, "prot": 4, "carb": 28, "fat": 1},
    {"nome": "Pão integral", "grupo": "Carboidrato", "porcao": "2 fatias", "cal": 130, "prot": 6, "carb": 24, "fat": 2},
    {"nome": "Tapioca", "grupo": "Carboidrato", "porcao": "2 colheres", "cal": 140, "prot": 0, "carb": 34, "fat": 0},
    {"nome": "Cuscuz", "grupo": "Carboidrato", "porcao": "100g", "cal": 112, "prot": 3, "carb": 25, "fat": 1},
    {"nome": "Aveia", "grupo": "Carboidrato", "porcao": "30g", "cal": 115, "prot": 4, "carb": 20, "fat": 2},
    {"nome": "Arroz branco", "grupo": "Carboidrato", "porcao": "100g", "cal": 130, "prot": 3, "carb": 28, "fat": 0},
    {"nome": "Batata doce", "grupo": "Carboidrato", "porcao": "100g", "cal": 86, "prot": 2, "carb": 20, "fat": 0},
    {"nome": "Macarrão", "grupo": "Carboidrato", "porcao": "100g", "cal": 158, "prot": 6, "carb": 31, "fat": 1},
    {"nome": "Banana", "grupo": "Fruta", "porcao": "1 unidade", "cal": 90, "prot": 1, "carb": 23, "fat": 0},
    {"nome": "Maçã", "grupo": "Fruta", "porcao": "1 unidade", "cal": 70, "prot": 0, "carb": 19, "fat": 0},
    {"nome": "Mamão", "grupo": "Fruta", "porcao": "1 fatia", "cal": 55, "prot": 1, "carb": 14, "fat": 0},
    {"nome": "Ovo", "grupo": "Proteína", "porcao": "2 unidades", "cal": 140, "prot": 12, "carb": 1, "fat": 10},
    {"nome": "Frango grelhado", "grupo": "Proteína", "porcao": "100g", "cal": 165, "prot": 31, "carb": 0, "fat": 4},
    {"nome": "Carne magra", "grupo": "Proteína", "porcao": "100g", "cal": 210, "prot": 28, "carb": 0, "fat": 10},
    {"nome": "Peixe", "grupo": "Proteína", "porcao": "100g", "cal": 150, "prot": 26, "carb": 0, "fat": 5},
    {"nome": "Iogurte natural", "grupo": "Proteína", "porcao": "170g", "cal": 110, "prot": 9, "carb": 12, "fat": 3},
    {"nome": "Whey protein", "grupo": "Proteína", "porcao": "1 scoop", "cal": 120, "prot": 24, "carb": 3, "fat": 2},
    {"nome": "Feijão", "grupo": "Leguminosa", "porcao": "1 concha", "cal": 95, "prot": 6, "carb": 17, "fat": 1},
    {"nome": "Salada", "grupo": "Vegetal", "porcao": "à vontade", "cal": 35, "prot": 2, "carb": 7, "fat": 0},
    {"nome": "Legumes", "grupo": "Vegetal", "porcao": "100g", "cal": 55, "prot": 2, "carb": 11, "fat": 0},
    {"nome": "Azeite", "grupo": "Gordura", "porcao": "1 colher chá", "cal": 45, "prot": 0, "carb": 0, "fat": 5},
    {"nome": "Pasta de amendoim", "grupo": "Gordura", "porcao": "1 colher", "cal": 95, "prot": 4, "carb": 3, "fat": 8},
]

DEFAULT_MEALS = {
    "Café da manhã": {"hora": "07:30", "orientacao": "Escolha 1 carboidrato, 1 proteína e 1 fruta.", "opcoes": ["Pão francês", "Pão integral", "Tapioca", "Cuscuz", "Ovo", "Iogurte natural", "Banana", "Maçã"]},
    "Almoço": {"hora": "12:30", "orientacao": "Base com carboidrato, proteína, feijão e vegetais.", "opcoes": ["Arroz branco", "Feijão", "Frango grelhado", "Carne magra", "Peixe", "Salada", "Legumes", "Azeite"]},
    "Lanche": {"hora": "16:00", "orientacao": "Escolha uma opção proteica e uma fruta/carboidrato.", "opcoes": ["Iogurte natural", "Whey protein", "Aveia", "Banana", "Maçã", "Pão integral"]},
    "Jantar": {"hora": "20:00", "orientacao": "Refeição leve com proteína, vegetais e carboidrato se necessário.", "opcoes": ["Frango grelhado", "Carne magra", "Peixe", "Batata doce", "Salada", "Legumes", "Azeite"]}
}

def save_data():
    data = {
        "foods": st.session_state.foods,
        "allowed_meals": st.session_state.allowed_meals,
        "patients": st.session_state.patients,
        "daily": st.session_state.daily,
        "water_log": st.session_state.water_log,
        "history": st.session_state.history,
        "profile": st.session_state.profile,
    }
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

loaded = load_data()

if "logged" not in st.session_state:
    st.session_state.logged = False
if "role" not in st.session_state:
    st.session_state.role = "Paciente"
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "nome" not in st.session_state:
    st.session_state.nome = "Lorran Ribeiro"
if "foods" not in st.session_state:
    st.session_state.foods = loaded.get("foods", DEFAULT_FOODS)
if "allowed_meals" not in st.session_state:
    st.session_state.allowed_meals = loaded.get("allowed_meals", DEFAULT_MEALS)
if "patients" not in st.session_state:
    st.session_state.patients = loaded.get("patients", [
        {"Paciente": "Lorran Ribeiro", "Objetivo": "Emagrecimento", "Adesão": "84%", "Peso": "80.0 kg", "Status": "Em dia"},
        {"Paciente": "Paciente Demo", "Objetivo": "Hipertrofia", "Adesão": "71%", "Peso": "72.5 kg", "Status": "Atenção"},
    ])
if "daily" not in st.session_state:
    st.session_state.daily = loaded.get("daily", {"cal": 0, "prot": 0, "carb": 0, "fat": 0, "water": 0})
if "water_log" not in st.session_state:
    st.session_state.water_log = loaded.get("water_log", [])
if "history" not in st.session_state:
    st.session_state.history = loaded.get("history", [])
if "profile" not in st.session_state:
    st.session_state.profile = loaded.get("profile", {"peso": 80.0, "altura": 180, "idade": 25, "sexo": "Masculino", "atividade": "Moderado", "objetivo": "Emagrecer"})

# =========================
# HELPERS
# =========================
def food_by_name(name):
    return next((f for f in st.session_state.foods if f["nome"] == name), None)

def sum_foods(names):
    total = {"cal": 0, "prot": 0, "carb": 0, "fat": 0}
    for name in names:
        f = food_by_name(name)
        if f:
            for k in total:
                total[k] += int(f[k])
    return total

def calc_clinica(peso, altura, idade, sexo, atividade_nome, objetivo):
    fatores = {"Sedentário": 1.2, "Leve": 1.375, "Moderado": 1.55, "Intenso": 1.725}
    fator = fatores.get(atividade_nome, 1.55)
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    tmb = 10 * peso + 6.25 * altura - 5 * idade + (5 if sexo == "Masculino" else -161)
    gasto = tmb * fator
    meta = gasto - 500 if objetivo == "Emagrecer" else gasto + 300 if objetivo == "Ganhar massa" else gasto
    prot = peso * 2
    gordura = peso * 0.8
    carbo = max((meta - (prot * 4 + gordura * 9)) / 4, 0)
    agua = peso * 35
    return imc, tmb, gasto, meta, prot, gordura, carbo, agua

def pct(v, goal):
    return min(v / goal, 1.0) if goal else 0

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
    st.write("")

def kpi(label, value, foot):
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-foot">{foot}</div>
    </div>
    """, unsafe_allow_html=True)

def nav_button(label, page):
    if st.session_state.page == page:
        st.sidebar.markdown(f"<div class='nav-active'>{label}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.sidebar.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

def get_targets():
    p = st.session_state.profile
    return calc_clinica(float(p["peso"]), int(p["altura"]), int(p["idade"]), p["sexo"], p["atividade"], p["objetivo"])

imc, tmb, gasto, meta_cal, meta_prot, meta_fat, meta_carb, meta_agua = get_targets()

# =========================
# LOGIN
# =========================
if not st.session_state.logged:
    c1, c2 = st.columns([1.25, .75], gap="large")
    with c1:
        st.markdown("""
        <div class="hero" style="min-height:540px;padding:42px;">
            <h1 style="font-size:48px;">NutriSync</h1>
            <p style="font-size:19px;max-width:760px;">
                Plataforma limpa para organizar dieta, alimentos permitidos, registro diário, água, metas e acompanhamento nutricional.
            </p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px;">
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:22px;">
                    <b style="font-size:18px;color:white;">Paciente</b><br>
                    <span style="color:rgba(255,255,255,.82);">Seleciona o que comeu, registra água e acompanha metas.</span>
                </div>
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:22px;">
                    <b style="font-size:18px;color:white;">Nutricionista</b><br>
                    <span style="color:rgba(255,255,255,.82);">Monta planos, libera opções e acompanha resultados.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card' style='margin-top:52px;'>", unsafe_allow_html=True)
        st.subheader("Entrar")
        role = st.selectbox("Perfil", ["Paciente", "Nutricionista"])
        nome = st.text_input("Nome", value=st.session_state.nome)
        st.text_input("Senha", value="demo", type="password")
        if st.button("Acessar painel", use_container_width=True):
            st.session_state.logged = True
            st.session_state.role = role
            st.session_state.nome = nome
            st.session_state.page = "Dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("<div class='side-logo'>Nutri<span>Sync</span></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='side-sub'>{st.session_state.role} • {st.session_state.nome}</div>", unsafe_allow_html=True)

if st.session_state.role == "Paciente":
    pages = ["Dashboard", "Minha dieta", "Registrar consumo", "Água", "Evolução", "Perfil", "Assistente"]
else:
    pages = ["Dashboard", "Pacientes", "Plano alimentar", "Banco de alimentos", "Calculadora clínica", "Relatórios", "Configurações"]

for p in pages:
    nav_button(p, p)

st.sidebar.write("")
if st.sidebar.button("Salvar agora", use_container_width=True):
    save_data()
    st.sidebar.success("Salvo.")
if st.sidebar.button("Sair", use_container_width=True):
    save_data()
    st.session_state.logged = False
    st.rerun()

page = st.session_state.page

# =========================
# PACIENTE
# =========================
if st.session_state.role == "Paciente":
    if page == "Dashboard":
        hero("Dashboard do paciente", "Resumo do dia, metas principais e próximos passos.")
        d = st.session_state.daily
        adesao = round((pct(d["cal"], meta_cal) + pct(d["prot"], meta_prot) + pct(d["water"], meta_agua)) / 3 * 100)
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi("Calorias", f"{d['cal']} kcal", f"Meta {int(meta_cal)} kcal")
        with c2: kpi("Proteína", f"{d['prot']}g", f"Meta {int(meta_prot)}g")
        with c3: kpi("Água", f"{d['water']}ml", f"Meta {int(meta_agua)}ml")
        with c4: kpi("Adesão", f"{adesao}%", "média do dia")
        left, right = st.columns([1.15, .85], gap="large")
        with left:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Progresso de hoje</div>", unsafe_allow_html=True)
            for label, value, target, suffix in [
                ("Calorias", d["cal"], meta_cal, "kcal"),
                ("Proteína", d["prot"], meta_prot, "g"),
                ("Carboidrato", d["carb"], meta_carb, "g"),
                ("Gordura", d["fat"], meta_fat, "g"),
                ("Água", d["water"], meta_agua, "ml"),
            ]:
                st.write(label)
                st.progress(pct(value, target))
                st.caption(f"{int(value)} / {int(target)} {suffix}")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Feedback</div>", unsafe_allow_html=True)
            if d["prot"] < meta_prot:
                st.markdown(f"<div class='warn-box'>Faltam {int(meta_prot - d['prot'])}g de proteína hoje.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ok-box'>Proteína batida.</div>", unsafe_allow_html=True)
            if d["cal"] > meta_cal:
                st.markdown(f"<div class='danger-box'>Você passou {int(d['cal'] - meta_cal)} kcal da meta.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ok-box'>Ainda restam {int(meta_cal - d['cal'])} kcal disponíveis.</div>", unsafe_allow_html=True)
            if d["water"] < meta_agua:
                st.markdown(f"<div class='warn-box'>Beba mais {int(meta_agua - d['water'])}ml de água.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Minha dieta":
        hero("Minha dieta", "Veja o que foi liberado para cada refeição e selecione o que você comeu.")
        for meal_name, meal in st.session_state.allowed_meals.items():
            st.markdown(f"""
            <div class="meal">
                <div class="meal-head">
                    <div>
                        <div class="meal-title">{meal_name}</div>
                        <div class="muted">{meal['orientacao']}</div>
                    </div>
                    <div class="meal-time">{meal['hora']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            selected = st.multiselect(f"Selecione o que comeu no {meal_name.lower()}", meal["opcoes"], key=f"select_{meal_name}")
            total = sum_foods(selected)
            st.caption(f"Selecionado: {total['cal']} kcal • {total['prot']}g proteína • {total['carb']}g carbo • {total['fat']}g gordura")
            if selected:
                for item in selected:
                    f = food_by_name(item)
                    if f:
                        st.markdown(f"""
                        <div class="option-card">
                            <div class="option-name">{f['nome']}</div>
                            <div class="muted">{f['porcao']} • {f['grupo']}</div>
                            <span class="badge">{f['cal']} kcal</span>
                            <span class="badge">{f['prot']}g proteína</span>
                            <span class="badge">{f['carb']}g carbo</span>
                            <span class="badge">{f['fat']}g gordura</span>
                        </div>
                        """, unsafe_allow_html=True)
            if st.button("Adicionar ao dia", key=f"add_{meal_name}", use_container_width=True):
                st.session_state.daily["cal"] += total["cal"]
                st.session_state.daily["prot"] += total["prot"]
                st.session_state.daily["carb"] += total["carb"]
                st.session_state.daily["fat"] += total["fat"]
                save_data()
                st.success("Refeição registrada.")

    elif page == "Registrar consumo":
        hero("Registrar consumo", "Registre manualmente quando comer algo fora da seleção.")
        c1, c2, c3 = st.columns(3)
        with c1:
            cal = st.number_input("Calorias extras", min_value=0, value=0)
            prot = st.number_input("Proteína extra (g)", min_value=0, value=0)
        with c2:
            carb = st.number_input("Carboidrato extra (g)", min_value=0, value=0)
            fat = st.number_input("Gordura extra (g)", min_value=0, value=0)
        with c3:
            obs = st.text_area("Observação")
            if st.button("Adicionar consumo manual", use_container_width=True):
                st.session_state.daily["cal"] += cal
                st.session_state.daily["prot"] += prot
                st.session_state.daily["carb"] += carb
                st.session_state.daily["fat"] += fat
                save_data()
                st.success("Consumo adicionado.")

    elif page == "Água":
        hero("Água", "Registre a quantidade de água bebida ao longo do dia.")
        c1, c2 = st.columns([.85, 1.15], gap="large")
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Novo registro</div>", unsafe_allow_html=True)
            quick = st.selectbox("Atalho", ["250 ml", "500 ml", "750 ml", "1000 ml"])
            custom = st.number_input("Ou informe outra quantidade (ml)", min_value=0, value=0, step=50)
            if st.button("Registrar água", use_container_width=True):
                val = custom if custom > 0 else int(quick.split()[0])
                st.session_state.daily["water"] += val
                st.session_state.water_log.append({"Horário": datetime.now().strftime("%H:%M"), "Água (ml)": val})
                save_data()
                st.success(f"{val}ml adicionados.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            kpi("Água hoje", f"{st.session_state.daily['water']}ml", f"Meta {int(meta_agua)}ml")
            st.progress(pct(st.session_state.daily["water"], meta_agua))
            st.write("Registros do dia")
            if st.session_state.water_log:
                st.dataframe(pd.DataFrame(st.session_state.water_log), hide_index=True, use_container_width=True)
            else:
                st.caption("Nenhum registro de água ainda.")

    elif page == "Evolução":
        hero("Evolução", "Histórico visual simples para acompanhar progresso.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Peso</div>", unsafe_allow_html=True)
            peso_hist = [float(h.get("peso", 80)) for h in st.session_state.history] or [82, 81.4, 80.9, 80.3, 80.0]
            st.line_chart(pd.DataFrame({"Peso": peso_hist}))
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Consumo</div>", unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({"Calorias": [st.session_state.daily["cal"]], "Proteína": [st.session_state.daily["prot"]]}))
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Perfil":
        hero("Perfil", "Ajuste seus dados para atualizar metas e cálculos.")
        p = st.session_state.profile
        c1, c2 = st.columns(2)
        with c1:
            p["peso"] = st.number_input("Peso (kg)", min_value=20.0, value=float(p["peso"]))
            p["altura"] = st.number_input("Altura (cm)", min_value=120, value=int(p["altura"]))
            p["idade"] = st.number_input("Idade", min_value=10, value=int(p["idade"]))
        with c2:
            p["sexo"] = st.selectbox("Sexo", ["Masculino", "Feminino"], index=0 if p["sexo"] == "Masculino" else 1)
            p["atividade"] = st.selectbox("Atividade", ["Sedentário", "Leve", "Moderado", "Intenso"], index=["Sedentário","Leve","Moderado","Intenso"].index(p["atividade"]))
            p["objetivo"] = st.selectbox("Objetivo", ["Emagrecer", "Manter", "Ganhar massa"], index=["Emagrecer","Manter","Ganhar massa"].index(p["objetivo"]))
        if st.button("Salvar perfil e fechar dia", use_container_width=True):
            st.session_state.history.append({
                "data": datetime.now().strftime("%d/%m/%Y"),
                "peso": p["peso"],
                **st.session_state.daily
            })
            save_data()
            st.success("Perfil salvo e dia adicionado ao histórico.")

    elif page == "Assistente":
        hero("Assistente", "Orientações rápidas com base no consumo do dia.")
        st.text_area("Como foi sua dieta hoje?")
        if st.button("Gerar sugestão"):
            d = st.session_state.daily
            if d["prot"] < meta_prot:
                st.markdown("<div class='warn-box'>Priorize uma fonte de proteína na próxima refeição: ovos, frango, iogurte, carne magra ou whey.</div>", unsafe_allow_html=True)
            elif d["cal"] > meta_cal:
                st.markdown("<div class='warn-box'>Amanhã reduza beliscos fora do plano e calorias líquidas.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ok-box'>Seu dia está bem alinhado. Mantenha o padrão e registre água.</div>", unsafe_allow_html=True)

# =========================
# NUTRICIONISTA
# =========================
else:
    if page == "Dashboard":
        hero("Dashboard do nutricionista", "Pacientes, adesão, planos ativos e alertas em um painel limpo.")
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi("Pacientes ativos", str(len(st.session_state.patients)), "em acompanhamento")
        with c2: kpi("Adesão média", "84%", "últimos 7 dias")
        with c3: kpi("Planos ativos", str(len(st.session_state.allowed_meals)), "refeições configuradas")
        with c4: kpi("Alertas", "4", "precisam de revisão")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Carteira de pacientes</div>", unsafe_allow_html=True)
        for p in st.session_state.patients:
            adesao = int(p["Adesão"].replace("%", ""))
            st.write(f"**{p['Paciente']}** — {p['Objetivo']} • {p['Peso']} • {p['Status']}")
            st.progress(adesao / 100)
            st.caption(f"Adesão: {adesao}%")
            st.write("---")
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Pacientes":
        hero("Pacientes", "Cadastre e acompanhe seus pacientes.")
        with st.expander("Adicionar paciente"):
            nome = st.text_input("Nome do paciente")
            objetivo = st.selectbox("Objetivo", ["Emagrecimento", "Hipertrofia", "Manutenção"])
            peso = st.number_input("Peso inicial", min_value=20.0, value=80.0)
            if st.button("Cadastrar paciente"):
                st.session_state.patients.append({"Paciente": nome or "Novo paciente", "Objetivo": objetivo, "Adesão": "0%", "Peso": f"{peso:.1f} kg", "Status": "Novo"})
                save_data()
                st.success("Paciente cadastrado.")
        st.dataframe(st.session_state.patients, use_container_width=True, hide_index=True)

    elif page == "Plano alimentar":
        hero("Plano alimentar", "Selecione quais alimentos o paciente pode comer em cada refeição.")
        meal_name = st.selectbox("Refeição", list(st.session_state.allowed_meals.keys()))
        current = st.session_state.allowed_meals[meal_name]
        c1, c2 = st.columns([.8, 1.2], gap="large")
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            hora = st.text_input("Horário", value=current["hora"])
            orientacao = st.text_area("Orientação da refeição", value=current["orientacao"])
            grupos = sorted(set(f["grupo"] for f in st.session_state.foods))
            filtro = st.multiselect("Filtrar por grupo", grupos, default=grupos)
            food_options = [f["nome"] for f in st.session_state.foods if f["grupo"] in filtro]
            selected = st.multiselect("Alimentos permitidos", food_options, default=current["opcoes"])
            if st.button("Salvar refeição", use_container_width=True):
                st.session_state.allowed_meals[meal_name] = {"hora": hora, "orientacao": orientacao, "opcoes": selected}
                save_data()
                st.success("Refeição atualizada.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Prévia para o paciente</div>", unsafe_allow_html=True)
            st.write(f"**{meal_name} • {hora}**")
            st.caption(orientacao)
            for item in selected:
                f = food_by_name(item)
                if f:
                    st.markdown(f"""
                    <div class="option-card">
                        <div class="option-name">{f['nome']}</div>
                        <div class="muted">{f['porcao']} • {f['grupo']}</div>
                        <span class="badge">{f['cal']} kcal</span>
                        <span class="badge">{f['prot']}g proteína</span>
                        <span class="badge">{f['carb']}g carbo</span>
                        <span class="badge">{f['fat']}g gordura</span>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Banco de alimentos":
        hero("Banco de alimentos", "Lista base de alimentos para montar os planos.")
        with st.expander("Cadastrar novo alimento"):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome do alimento")
                grupo = st.selectbox("Grupo", ["Carboidrato", "Proteína", "Fruta", "Vegetal", "Leguminosa", "Gordura", "Outro"])
                porcao = st.text_input("Porção", value="100g")
            with c2:
                cal = st.number_input("Calorias", min_value=0, value=100)
                prot = st.number_input("Proteína (g)", min_value=0, value=0)
                carb = st.number_input("Carboidrato (g)", min_value=0, value=0)
                fat = st.number_input("Gordura (g)", min_value=0, value=0)
            if st.button("Adicionar alimento"):
                if nome:
                    st.session_state.foods.append({"nome": nome, "grupo": grupo, "porcao": porcao, "cal": cal, "prot": prot, "carb": carb, "fat": fat})
                    save_data()
                    st.success("Alimento cadastrado.")
        st.dataframe(pd.DataFrame(st.session_state.foods), use_container_width=True, hide_index=True)

    elif page == "Calculadora clínica":
        hero("Calculadora clínica", "IMC, TMB, gasto energético, meta calórica, macros e água.")
        c1, c2 = st.columns([.9, 1.1], gap="large")
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
            idade = st.number_input("Idade", min_value=10, value=25)
            peso = st.number_input("Peso (kg)", min_value=20.0, value=80.0)
            altura = st.number_input("Altura (cm)", min_value=120, value=180)
            atividade_nome = st.selectbox("Nível de atividade", ["Sedentário", "Leve", "Moderado", "Intenso"])
            objetivo = st.selectbox("Objetivo", ["Emagrecer", "Manter", "Ganhar massa"])
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            imc2, tmb2, gasto2, meta2, prot2, fat2, carb2, agua2 = calc_clinica(peso, altura, idade, sexo, atividade_nome, objetivo)
            r1, r2 = st.columns(2)
            with r1:
                kpi("IMC", f"{imc2:.1f}", "índice corporal")
                kpi("Gasto total", f"{int(gasto2)}", "kcal/dia")
                kpi("Proteína", f"{int(prot2)}g", "meta diária")
            with r2:
                kpi("TMB", f"{int(tmb2)}", "kcal basal")
                kpi("Meta calórica", f"{int(meta2)}", "kcal/dia")
                kpi("Água", f"{int(agua2)}ml", "estimativa diária")

    elif page == "Relatórios":
        hero("Relatórios", "Resumo semanal para decisão do nutricionista.")
        d = st.session_state.daily
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Resumo atual</div>
            <p><b>Paciente:</b> {st.session_state.nome}</p>
            <p><b>Calorias hoje:</b> {d['cal']} kcal</p>
            <p><b>Proteína hoje:</b> {d['prot']}g</p>
            <p><b>Água hoje:</b> {d['water']}ml</p>
            <div class="ok-box">Sugestão: revisar proteína se ficar abaixo da meta por mais de 2 dias.</div>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Configurações":
        hero("Configurações", "Gerencie dados locais da plataforma.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Salvar dados locais", use_container_width=True):
                save_data()
                st.success("Dados salvos.")
        with c2:
            if st.button("Zerar consumo do dia", use_container_width=True):
                st.session_state.daily = {"cal": 0, "prot": 0, "carb": 0, "fat": 0, "water": 0}
                st.session_state.water_log = []
                save_data()
                st.success("Consumo zerado.")
