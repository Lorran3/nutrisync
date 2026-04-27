
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
from pathlib import Path

st.set_page_config(
    page_title="NutriSync Ultra",
    page_icon="NS",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path("nutrisync_ultra_data.json")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ============================================================
# STYLE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #f4f8f3;
    --surface: rgba(255,255,255,.92);
    --surface2: #ffffff;
    --dark: #12372a;
    --dark2: #071f18;
    --green: #1f8f5f;
    --green2: #176f49;
    --green3: #eaf7ef;
    --text: #13231c;
    --muted: #6f7d75;
    --line: #dfe8e1;
    --red: #b91c1c;
    --redbg: #fef2f2;
    --amber: #92400e;
    --amberbg: #fffbeb;
    --blue: #1d4ed8;
    --bluebg: #eff6ff;
}

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(31,143,95,.16), transparent 30%),
        radial-gradient(circle at bottom right, rgba(31,143,95,.08), transparent 35%),
        linear-gradient(180deg, #fbfdf9 0%, #edf5ee 100%);
    color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.35rem; padding-bottom: 3rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12372a 0%, #071f18 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 26px; }

.side-logo { color: white; font-size: 31px; font-weight: 900; letter-spacing: -1px; margin-bottom: 3px; }
.side-logo span { color: #86efac; }
.side-sub { color: #b7e8ca; font-size: 13px; margin-bottom: 20px; line-height: 1.45; }

.nav-btn button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    border-radius: 16px !important;
    padding: 13px 15px !important;
    margin: 3px 0 !important;
    background: rgba(255,255,255,.07) !important;
    color: #ecfdf5 !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}
.nav-btn button:hover { background: rgba(134,239,172,.17) !important; color: white !important; }
.nav-active {
    background: linear-gradient(135deg, #1f8f5f, #176f49);
    color: white;
    border-radius: 16px;
    padding: 13px 15px;
    margin: 7px 0;
    font-weight: 900;
    box-shadow: 0 14px 28px rgba(31,143,95,.28);
}

/* Inputs */
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
.stTextArea label, .stMultiSelect label, .stSlider label,
.stFileUploader label {
    color: #263d32 !important;
    font-weight: 800 !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #12372a 0%, #1f8f5f 100%);
    color: white;
    border-radius: 34px;
    padding: 32px;
    box-shadow: 0 26px 60px rgba(18,55,42,.22);
    min-height: 168px;
    position: relative;
    overflow: hidden;
    margin-bottom: 18px;
}
.hero:after {
    content: "";
    position: absolute;
    width: 255px;
    height: 255px;
    border-radius: 999px;
    right: -75px;
    top: -98px;
    background: rgba(255,255,255,.11);
}
.hero h1 { color: white; margin: 0 0 9px 0; font-size: 38px; font-weight: 900; letter-spacing: -1.2px; }
.hero p { color: rgba(255,255,255,.86); font-weight: 650; max-width: 860px; margin:0; line-height:1.55; }

.card {
    background: rgba(255,255,255,.96);
    border: 1px solid #dfe8e1;
    border-radius: 28px;
    padding: 22px;
    box-shadow: 0 18px 44px rgba(18,55,42,.075);
}
.card-tight { padding: 16px; border-radius: 22px; }
.card-title { color: #12372a; font-size: 20px; font-weight: 900; margin-bottom: 6px; }
.card-sub { color: #6f7d75; font-size: 14px; font-weight: 650; margin-bottom: 12px; }
.muted { color: #6f7d75; font-size: 14px; font-weight: 600; }

.kpi-label { color: #6f7d75; font-size: 12px; font-weight: 850; text-transform: uppercase; letter-spacing: .45px; }
.kpi-value { color: #12372a; font-size: 34px; font-weight: 900; letter-spacing: -.9px; margin-top: 8px; }
.kpi-foot { color: #1f8f5f; font-size: 13px; font-weight: 850; margin-top: 9px; }

.pill {
    display:inline-block;
    border-radius: 999px;
    padding: 7px 11px;
    font-size:12px;
    font-weight:900;
    margin: 4px 6px 4px 0;
}
.pill-green { background:#eaf7ef; color:#176f49; border:1px solid #cdeedb; }
.pill-red { background:#fef2f2; color:#991b1b; border:1px solid #fecaca; }
.pill-amber { background:#fffbeb; color:#92400e; border:1px solid #fde68a; }
.pill-blue { background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; }

.alert-card {
    background:white;
    border:1px solid #dfe8e1;
    border-left: 6px solid #1f8f5f;
    border-radius: 22px;
    padding: 16px;
    margin: 10px 0;
    box-shadow: 0 10px 26px rgba(18,55,42,.055);
}
.alert-red { border-left-color:#dc2626; }
.alert-amber { border-left-color:#d97706; }
.alert-green { border-left-color:#1f8f5f; }
.alert-title { font-weight:900; color:#12372a; font-size:16px; }
.alert-desc { color:#6f7d75; font-size:13px; font-weight:650; margin-top:4px; }

.meal {
    background: white;
    border: 1px solid #dfe8e1;
    border-radius: 24px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 10px 25px rgba(18,55,42,.05);
}
.meal-head { display: flex; justify-content: space-between; gap: 12px; align-items: start; }
.meal-title { color: #12372a; font-weight: 900; font-size: 18px; }
.meal-time { background: #eaf7ef; color: #176f49; padding: 7px 10px; border-radius: 999px; font-size: 12px; font-weight: 900; }
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
.option-card { background: #fbfdfb; border: 1px solid #dfe8e1; border-radius: 18px; padding: 14px; margin: 10px 0; }
.option-name { font-weight: 900; color: #12372a; }

.ok-box { background: #eaf7ef; color: #166534; border: 1px solid #bce7cc; border-radius: 17px; padding: 14px 16px; font-weight: 800; margin: 9px 0; }
.warn-box { background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; border-radius: 17px; padding: 14px 16px; font-weight: 800; margin: 9px 0; }
.danger-box { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-radius: 17px; padding: 14px 16px; font-weight: 800; margin: 9px 0; }

.chat-box { background: white; border: 1px solid #dfe8e1; border-radius: 24px; padding: 18px; max-height: 500px; overflow-y: auto; box-shadow: 0 12px 28px rgba(18,55,42,.055); }
.chat-msg { padding: 12px 14px; border-radius: 16px; margin: 10px 0; max-width: 82%; }
.chat-patient { background: #eaf7ef; margin-left: auto; color: #12372a; }
.chat-nutri { background: #f3f4f6; color: #12372a; }

.stButton > button {
    border-radius: 15px !important;
    border: none !important;
    background: #1f8f5f !important;
    color: white !important;
    font-weight: 850 !important;
    padding: 12px 18px !important;
    box-shadow: 0 10px 22px rgba(31,143,95,.18) !important;
}
.stButton > button:hover { background: #176f49 !important; color: white !important; }
.stProgress > div > div > div > div { background-color: #1f8f5f !important; }

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dfe8e1;
    border-radius: 24px;
    padding: 18px;
    box-shadow: 0 14px 34px rgba(18,55,42,.07);
}
[data-testid="stMetricLabel"] * { color:#6f7d75 !important; font-weight:800 !important; }
[data-testid="stMetricValue"] { color:#12372a !important; font-weight:900 !important; }

@media(max-width: 800px) {
    .hero h1 { font-size: 29px; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .kpi-value { font-size: 28px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DEFAULT DATA
# ============================================================
DEFAULT_FOODS = [
    {"nome":"Pão francês","grupo":"Carboidrato","porcao":"1 unidade","cal":135,"prot":4,"carb":28,"fat":1},
    {"nome":"Pão integral","grupo":"Carboidrato","porcao":"2 fatias","cal":130,"prot":6,"carb":24,"fat":2},
    {"nome":"Tapioca","grupo":"Carboidrato","porcao":"2 colheres","cal":140,"prot":0,"carb":34,"fat":0},
    {"nome":"Cuscuz","grupo":"Carboidrato","porcao":"100g","cal":112,"prot":3,"carb":25,"fat":1},
    {"nome":"Aveia","grupo":"Carboidrato","porcao":"30g","cal":115,"prot":4,"carb":20,"fat":2},
    {"nome":"Arroz branco","grupo":"Carboidrato","porcao":"100g","cal":130,"prot":3,"carb":28,"fat":0},
    {"nome":"Batata doce","grupo":"Carboidrato","porcao":"100g","cal":86,"prot":2,"carb":20,"fat":0},
    {"nome":"Macarrão","grupo":"Carboidrato","porcao":"100g","cal":158,"prot":6,"carb":31,"fat":1},
    {"nome":"Banana","grupo":"Fruta","porcao":"1 unidade","cal":90,"prot":1,"carb":23,"fat":0},
    {"nome":"Maçã","grupo":"Fruta","porcao":"1 unidade","cal":70,"prot":0,"carb":19,"fat":0},
    {"nome":"Mamão","grupo":"Fruta","porcao":"1 fatia","cal":55,"prot":1,"carb":14,"fat":0},
    {"nome":"Ovo","grupo":"Proteína","porcao":"2 unidades","cal":140,"prot":12,"carb":1,"fat":10},
    {"nome":"Frango grelhado","grupo":"Proteína","porcao":"100g","cal":165,"prot":31,"carb":0,"fat":4},
    {"nome":"Carne magra","grupo":"Proteína","porcao":"100g","cal":210,"prot":28,"carb":0,"fat":10},
    {"nome":"Peixe","grupo":"Proteína","porcao":"100g","cal":150,"prot":26,"carb":0,"fat":5},
    {"nome":"Iogurte natural","grupo":"Proteína","porcao":"170g","cal":110,"prot":9,"carb":12,"fat":3},
    {"nome":"Whey protein","grupo":"Proteína","porcao":"1 scoop","cal":120,"prot":24,"carb":3,"fat":2},
    {"nome":"Feijão","grupo":"Leguminosa","porcao":"1 concha","cal":95,"prot":6,"carb":17,"fat":1},
    {"nome":"Salada","grupo":"Vegetal","porcao":"à vontade","cal":35,"prot":2,"carb":7,"fat":0},
    {"nome":"Legumes","grupo":"Vegetal","porcao":"100g","cal":55,"prot":2,"carb":11,"fat":0},
    {"nome":"Azeite","grupo":"Gordura","porcao":"1 colher chá","cal":45,"prot":0,"carb":0,"fat":5},
    {"nome":"Pasta de amendoim","grupo":"Gordura","porcao":"1 colher","cal":95,"prot":4,"carb":3,"fat":8},
]

DEFAULT_PATIENTS = [
    {"Paciente":"Lorran Ribeiro","Objetivo":"Emagrecimento","Adesão":"84%","Peso":"80.0 kg","Status":"Em dia"},
    {"Paciente":"Kassia Ribeiro","Objetivo":"Manutenção","Adesão":"91%","Peso":"62.0 kg","Status":"Excelente"},
    {"Paciente":"Paciente Demo","Objetivo":"Hipertrofia","Adesão":"71%","Peso":"72.5 kg","Status":"Atenção"},
    {"Paciente":"Ana Souza","Objetivo":"Reeducação","Adesão":"93%","Peso":"68.2 kg","Status":"Excelente"},
    {"Paciente":"Lucas Martins","Objetivo":"Hipertrofia","Adesão":"62%","Peso":"77.1 kg","Status":"Atenção"},
]

DEFAULT_PLAN = {
    "Café da manhã":{"hora":"07:30","orientacao":"Escolha 1 carboidrato, 1 proteína e 1 fruta.","opcoes":["Pão francês","Pão integral","Tapioca","Ovo","Iogurte natural","Banana","Maçã"]},
    "Almoço":{"hora":"12:30","orientacao":"Base com carboidrato, proteína, feijão e vegetais.","opcoes":["Arroz branco","Feijão","Frango grelhado","Carne magra","Salada","Legumes","Azeite"]},
    "Lanche":{"hora":"16:00","orientacao":"Escolha uma opção proteica e uma fruta/carboidrato.","opcoes":["Iogurte natural","Whey protein","Aveia","Banana","Maçã","Pão integral"]},
    "Jantar":{"hora":"20:00","orientacao":"Refeição leve com proteína, vegetais e carboidrato se necessário.","opcoes":["Frango grelhado","Carne magra","Peixe","Batata doce","Salada","Legumes"]},
}

# ============================================================
# DATA LAYER
# ============================================================
def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def init_state():
    data = load_data()
    defaults = {
        "logged": False,
        "role": "Paciente",
        "page": "Dashboard",
        "nome": "Lorran Ribeiro",
        "foods": data.get("foods", DEFAULT_FOODS),
        "patients": data.get("patients", DEFAULT_PATIENTS),
        "selected_patient": data.get("selected_patient", "Lorran Ribeiro"),
        "plans": data.get("plans", {p["Paciente"]: DEFAULT_PLAN.copy() for p in DEFAULT_PATIENTS}),
        "daily_by_patient": data.get("daily_by_patient", {}),
        "water_by_patient": data.get("water_by_patient", {}),
        "profile_by_patient": data.get("profile_by_patient", {}),
        "history_by_patient": data.get("history_by_patient", {}),
        "chat_by_patient": data.get("chat_by_patient", {}),
        "photos_by_patient": data.get("photos_by_patient", {}),
        "checkins_by_patient": data.get("checkins_by_patient", {}),
        "photo_reviews_by_patient": data.get("photo_reviews_by_patient", {}),
        "notification_settings": data.get("notification_settings", {"water": True, "meal": True, "protein": True}),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def save_data():
    data = {
        "foods": st.session_state.foods,
        "patients": st.session_state.patients,
        "selected_patient": st.session_state.selected_patient,
        "plans": st.session_state.plans,
        "daily_by_patient": st.session_state.daily_by_patient,
        "water_by_patient": st.session_state.water_by_patient,
        "profile_by_patient": st.session_state.profile_by_patient,
        "history_by_patient": st.session_state.history_by_patient,
        "chat_by_patient": st.session_state.chat_by_patient,
        "photos_by_patient": st.session_state.photos_by_patient,
        "checkins_by_patient": st.session_state.checkins_by_patient,
        "photo_reviews_by_patient": st.session_state.photo_reviews_by_patient,
        "notification_settings": st.session_state.notification_settings,
    }
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def patient_names():
    return [p["Paciente"] for p in st.session_state.patients]

def ensure_patient(name):
    st.session_state.plans.setdefault(name, DEFAULT_PLAN.copy())
    st.session_state.daily_by_patient.setdefault(name, {"cal":0,"prot":0,"carb":0,"fat":0,"water":0})
    st.session_state.water_by_patient.setdefault(name, [])
    st.session_state.profile_by_patient.setdefault(name, {"peso":80.0,"altura":180,"idade":25,"sexo":"Masculino","atividade":"Moderado","objetivo":"Emagrecer"})
    st.session_state.history_by_patient.setdefault(name, sample_history(name))
    st.session_state.chat_by_patient.setdefault(name, [])
    st.session_state.photos_by_patient.setdefault(name, [])
    st.session_state.checkins_by_patient.setdefault(name, [])
    st.session_state.photo_reviews_by_patient.setdefault(name, {})

def sample_history(name):
    base_weight = 80 if "Lorran" in name else 62 if "Kassia" in name else 74
    out = []
    for i in range(7):
        d = date.today() - timedelta(days=6-i)
        out.append({
            "data": d.strftime("%d/%m"),
            "peso": round(base_weight - (i*0.18), 1),
            "cal": 1700 + (i*45),
            "prot": 95 + (i*6),
            "water": 1600 + (i*120),
            "adesao": min(96, 68 + i*4)
        })
    return out

for p in patient_names():
    ensure_patient(p)

def current_patient():
    if st.session_state.role == "Paciente":
        return st.session_state.nome if st.session_state.nome in patient_names() else st.session_state.selected_patient
    return st.session_state.selected_patient

# ============================================================
# HELPERS
# ============================================================
def food_by_name(name):
    return next((f for f in st.session_state.foods if f["nome"] == name), None)

def sum_foods(names):
    total = {"cal":0,"prot":0,"carb":0,"fat":0}
    for name in names:
        f = food_by_name(name)
        if f:
            for k in total:
                total[k] += int(f[k])
    return total

def calc_clinica(peso, altura, idade, sexo, atividade_nome, objetivo):
    fatores = {"Sedentário":1.2,"Leve":1.375,"Moderado":1.55,"Intenso":1.725}
    fator = fatores.get(atividade_nome, 1.55)
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    tmb = 10*peso + 6.25*altura - 5*idade + (5 if sexo == "Masculino" else -161)
    gasto = tmb * fator
    meta = gasto - 500 if objetivo == "Emagrecer" else gasto + 300 if objetivo == "Ganhar massa" else gasto
    prot = peso * 2
    gordura = peso * 0.8
    carbo = max((meta - (prot*4 + gordura*9))/4, 0)
    agua = peso * 35
    return imc, tmb, gasto, meta, prot, gordura, carbo, agua

def targets(name):
    p = st.session_state.profile_by_patient[name]
    return calc_clinica(float(p["peso"]), int(p["altura"]), int(p["idade"]), p["sexo"], p["atividade"], p["objetivo"])

def pct(v, goal):
    return min(v/goal, 1.0) if goal else 0

def adherence_for(name):
    d = st.session_state.daily_by_patient[name]
    _, _, _, meta_cal, meta_prot, _, _, meta_agua = targets(name)
    return round((pct(d["cal"], meta_cal) + pct(d["prot"], meta_prot) + pct(d["water"], meta_agua))/3*100)

def streak(name):
    checks = sorted(set(st.session_state.checkins_by_patient.get(name, [])), reverse=True)
    if not checks:
        return 0
    today = date.today()
    count = 0
    for i in range(0, 365):
        d = (today - timedelta(days=i)).isoformat()
        if d in checks:
            count += 1
        else:
            if i == 0:
                continue
            break
    return count

def generate_alerts(name):
    d = st.session_state.daily_by_patient[name]
    hist = st.session_state.history_by_patient[name]
    _, _, _, meta_cal, meta_prot, _, _, meta_agua = targets(name)
    alerts = []
    if d["cal"] == 0:
        alerts.append(("red", "Paciente sem registro hoje", "Nenhuma refeição registrada até agora."))
    if d["prot"] < meta_prot * .55:
        alerts.append(("amber", "Proteína abaixo do esperado", f"Consumiu {int(d['prot'])}g de {int(meta_prot)}g planejados."))
    if d["water"] < meta_agua * .5:
        alerts.append(("amber", "Hidratação baixa", f"Água registrada: {int(d['water'])}ml."))
    if d["cal"] > meta_cal * 1.08:
        alerts.append(("red", "Calorias acima da meta", f"Passou cerca de {int(d['cal']-meta_cal)} kcal."))
    if len(st.session_state.checkins_by_patient[name]) >= 3:
        alerts.append(("green", "Boa consistência", f"Sequência atual de {streak(name)} dias."))
    if hist:
        last = hist[-1]
        if last.get("adesao", 0) >= 85:
            alerts.append(("green", "Adesão forte na semana", f"Última adesão registrada: {last.get('adesao')}%."))
    return alerts

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def kpi(label, value, foot):
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-foot">{foot}</div>
    </div>
    """, unsafe_allow_html=True)

def alert_card(kind, title, desc):
    cls = "alert-red" if kind == "red" else "alert-amber" if kind == "amber" else "alert-green"
    pill = "pill-red" if kind == "red" else "pill-amber" if kind == "amber" else "pill-green"
    tag = "Atenção" if kind == "red" else "Ajuste" if kind == "amber" else "Bom"
    st.markdown(f"""
    <div class="alert-card {cls}">
        <span class="pill {pill}">{tag}</span>
        <div class="alert-title">{title}</div>
        <div class="alert-desc">{desc}</div>
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

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logged:
    left, right = st.columns([1.22, .78], gap="large")
    with left:
        st.markdown("""
        <div class="hero" style="min-height:570px;padding:46px;">
            <h1 style="font-size:52px;">NutriSync Ultra</h1>
            <p style="font-size:19px;max-width:790px;">
                Plataforma premium para nutricionistas acompanharem pacientes com dieta individual,
                check-in, fotos, chat, relatórios e alertas inteligentes.
            </p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:34px;">
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.16);border-radius:26px;padding:22px;">
                    <b style="font-size:18px;color:white;">Para o paciente</b><br>
                    <span style="color:rgba(255,255,255,.84);">Registra refeições, água, fotos, peso e check-in com interface simples.</span>
                </div>
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.16);border-radius:26px;padding:22px;">
                    <b style="font-size:18px;color:white;">Para o nutricionista</b><br>
                    <span style="color:rgba(255,255,255,.84);">Enxerga alertas, evolução, relatórios, fotos e dieta por paciente.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Entrar no NutriSync")
        st.caption("Ambiente demonstrativo para validação")
        role = st.selectbox("Perfil", ["Paciente", "Nutricionista"])
        if role == "Paciente":
            nome = st.selectbox("Paciente", patient_names())
        else:
            nome = st.text_input("Nome", value="Nutricionista")
        st.text_input("Senha", value="demo", type="password")
        if st.button("Acessar plataforma", use_container_width=True):
            st.session_state.logged = True
            st.session_state.role = role
            st.session_state.nome = nome
            if role == "Paciente":
                st.session_state.selected_patient = nome
            st.session_state.page = "Dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("<div class='side-logo'>Nutri<span>Sync</span></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='side-sub'>{st.session_state.role}<br>{st.session_state.nome}</div>", unsafe_allow_html=True)

if st.session_state.role == "Nutricionista":
    st.session_state.selected_patient = st.sidebar.selectbox(
        "Paciente ativo",
        patient_names(),
        index=patient_names().index(st.session_state.selected_patient) if st.session_state.selected_patient in patient_names() else 0
    )
    ensure_patient(st.session_state.selected_patient)

if st.session_state.role == "Paciente":
    pages = ["Dashboard", "Minha dieta", "Registrar consumo", "Água", "Fotos", "Chat", "Check-in", "Evolução", "Perfil"]
else:
    pages = ["Dashboard", "Central de alertas", "Pacientes", "Plano alimentar", "Banco de alimentos", "Chat", "Fotos", "Relatório semanal", "Calculadora clínica", "Configurações"]

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

pname = current_patient()
ensure_patient(pname)
daily = st.session_state.daily_by_patient[pname]
imc, tmb, gasto, meta_cal, meta_prot, meta_fat, meta_carb, meta_agua = targets(pname)
page = st.session_state.page

# toast-like in-app reminders
if st.session_state.role == "Paciente":
    if st.session_state.notification_settings.get("water", True) and daily["water"] < meta_agua * .5 and page != "Água":
        st.toast("Lembrete: hidratação ainda está baixa hoje.")
    if st.session_state.notification_settings.get("meal", True) and daily["cal"] == 0 and page != "Minha dieta":
        st.toast("Lembrete: registre sua primeira refeição.")

# ============================================================
# DASHBOARD
# ============================================================
if page == "Dashboard":
    title = "Dashboard do paciente" if st.session_state.role == "Paciente" else "Dashboard executivo"
    subtitle = f"Acompanhamento atual de {pname} com metas, tendências e alertas acionáveis."
    hero(title, subtitle)

    if st.session_state.role == "Nutricionista":
        cols = st.columns(4)
        att = sum(1 for n in patient_names() if any(a[0] in ["red","amber"] for a in generate_alerts(n)))
        avg = round(sum(adherence_for(n) for n in patient_names()) / max(len(patient_names()), 1))
        with cols[0]: kpi("Pacientes ativos", len(patient_names()), "em acompanhamento")
        with cols[1]: kpi("Precisam atenção", att, "alertas abertos")
        with cols[2]: kpi("Adesão média", f"{avg}%", "carteira atual")
        with cols[3]: kpi("Paciente ativo", pname.split()[0], "selecionado")
        st.write("")

    adesao = adherence_for(pname)
    cols = st.columns(4)
    with cols[0]: kpi("Calorias", f"{daily['cal']} kcal", f"Meta {int(meta_cal)} kcal")
    with cols[1]: kpi("Proteína", f"{daily['prot']}g", f"Meta {int(meta_prot)}g")
    with cols[2]: kpi("Água", f"{daily['water']}ml", f"Meta {int(meta_agua)}ml")
    with cols[3]: kpi("Sequência", f"{streak(pname)} dias", f"Adesão {adesao}%")

    left, mid, right = st.columns([1.05, 1.05, .9], gap="large")
    with left:
        st.markdown('<div class="card-title">Progresso do dia</div>', unsafe_allow_html=True)
        for label, value, target, suffix in [
            ("Calorias", daily["cal"], meta_cal, "kcal"),
            ("Proteína", daily["prot"], meta_prot, "g"),
            ("Carboidrato", daily["carb"], meta_carb, "g"),
            ("Gordura", daily["fat"], meta_fat, "g"),
            ("Água", daily["water"], meta_agua, "ml"),
        ]:
            st.write(label)
            st.progress(pct(value, target))
            st.caption(f"{int(value)} / {int(target)} {suffix}")

    with mid:
        st.markdown('<div class="card-title">Evolução semanal</div>', unsafe_allow_html=True)
        hist = pd.DataFrame(st.session_state.history_by_patient[pname])
        if not hist.empty:
            st.line_chart(hist.set_index("data")[["peso", "adesao"]])
        else:
            st.info("Sem histórico suficiente.")

    with right:
        st.markdown('<div class="card-title">Alertas inteligentes</div>', unsafe_allow_html=True)
        alerts = generate_alerts(pname)
        for kind, title, desc in alerts[:4]:
            alert_card(kind, title, desc)

# ============================================================
# CENTRAL ALERTAS
# ============================================================
elif page == "Central de alertas":
    hero("Central de alertas", "Pacientes que precisam de ação agora, priorizados automaticamente.")
    rows = []
    for n in patient_names():
        alerts = generate_alerts(n)
        risk = sum(3 if a[0]=="red" else 2 if a[0]=="amber" else 0 for a in alerts)
        rows.append({"Paciente": n, "Risco": risk, "Adesão": f"{adherence_for(n)}%", "Alertas": len(alerts)})
    df = pd.DataFrame(rows).sort_values("Risco", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.write("")
    for n in df["Paciente"].tolist():
        st.markdown(f"### {n}")
        for kind, title, desc in generate_alerts(n):
            alert_card(kind, title, desc)

# ============================================================
# PACIENTE FOOD FLOW
# ============================================================
elif page == "Minha dieta":
    hero("Minha dieta", f"Plano alimentar liberado para {pname}.")
    plan = st.session_state.plans[pname]
    for meal_name, meal in plan.items():
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
        selected = st.multiselect(f"Selecione o que comeu no {meal_name.lower()}", meal["opcoes"], key=f"select_{pname}_{meal_name}")
        total = sum_foods(selected)
        st.caption(f"Selecionado: {total['cal']} kcal • {total['prot']}g proteína • {total['carb']}g carbo • {total['fat']}g gordura")
        if selected:
            cgrid = st.columns(min(3, len(selected)))
            for idx, item in enumerate(selected):
                f = food_by_name(item)
                if f:
                    with cgrid[idx % len(cgrid)]:
                        st.markdown(f"""
                        <div class="option-card">
                            <div class="option-name">{f['nome']}</div>
                            <div class="muted">{f['porcao']} • {f['grupo']}</div>
                            <span class="badge">{f['cal']} kcal</span>
                            <span class="badge">{f['prot']}g proteína</span>
                        </div>
                        """, unsafe_allow_html=True)
        if st.button(f"Adicionar {meal_name} ao dia", key=f"add_{pname}_{meal_name}", use_container_width=True):
            for k in total:
                daily[k] += total[k]
            save_data()
            st.success("Refeição registrada.")

elif page == "Registrar consumo":
    hero("Registrar consumo", f"Registro manual para {pname}.")
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
            daily["cal"] += cal; daily["prot"] += prot; daily["carb"] += carb; daily["fat"] += fat
            save_data()
            st.success("Consumo adicionado.")

elif page == "Água":
    hero("Água", f"Registro de água de {pname}.")
    c1, c2 = st.columns([.85, 1.15], gap="large")
    with c1:
        st.markdown('<div class="card card-tight">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Novo registro</div>', unsafe_allow_html=True)
        quick = st.selectbox("Atalho", ["250 ml", "500 ml", "750 ml", "1000 ml"])
        custom = st.number_input("Outra quantidade (ml)", min_value=0, value=0, step=50)
        if st.button("Registrar água", use_container_width=True):
            val = custom if custom > 0 else int(quick.split()[0])
            daily["water"] += val
            st.session_state.water_by_patient[pname].append({"Horário": datetime.now().strftime("%H:%M"), "Água (ml)": val})
            save_data()
            st.success(f"{val}ml adicionados.")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        kpi("Água hoje", f"{daily['water']}ml", f"Meta {int(meta_agua)}ml")
        st.progress(pct(daily["water"], meta_agua))
        if st.session_state.water_by_patient[pname]:
            st.dataframe(pd.DataFrame(st.session_state.water_by_patient[pname]), hide_index=True, use_container_width=True)

# ============================================================
# PHOTOS + CHAT + CHECKIN
# ============================================================
elif page == "Fotos":
    hero("Fotos das refeições", f"Envio, histórico e avaliação de refeições de {pname}.")
    if st.session_state.role == "Paciente":
        c1, c2 = st.columns([.8, 1.2], gap="large")
        with c1:
            refeicao = st.selectbox("Refeição", list(st.session_state.plans[pname].keys()))
            obs = st.text_area("Observação da foto")
            img = st.file_uploader("Enviar foto da refeição", type=["png","jpg","jpeg"])
            if img and st.button("Salvar foto", use_container_width=True):
                filename = f"{pname.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{img.name}"
                path = UPLOAD_DIR / filename
                path.write_bytes(img.getbuffer())
                item = {"id": filename, "data": datetime.now().strftime("%d/%m/%Y %H:%M"), "refeicao": refeicao, "obs": obs, "arquivo": str(path)}
                st.session_state.photos_by_patient[pname].append(item)
                save_data()
                st.success("Foto salva.")
        with c2:
            st.markdown('<div class="ok-box">Dica: envie foto logo após a refeição para facilitar a avaliação do nutricionista.</div>', unsafe_allow_html=True)
    photos = list(reversed(st.session_state.photos_by_patient[pname]))
    if photos:
        for ph in photos:
            c1, c2 = st.columns([.55, .45], gap="large")
            with c1:
                st.markdown(f"**{ph['refeicao']}** — {ph['data']}")
                st.caption(ph.get("obs",""))
                if Path(ph["arquivo"]).exists():
                    st.image(ph["arquivo"], use_container_width=True)
            with c2:
                reviews = st.session_state.photo_reviews_by_patient[pname]
                current = reviews.get(ph["id"], {"status":"Pendente","comentario":""})
                st.markdown(f"<span class='pill pill-blue'>Status: {current['status']}</span>", unsafe_allow_html=True)
                if st.session_state.role == "Nutricionista":
                    status = st.selectbox("Avaliação", ["Pendente","Aprovada","Ajustar","Fora da dieta"], index=["Pendente","Aprovada","Ajustar","Fora da dieta"].index(current["status"]), key=f"status_{ph['id']}")
                    comentario = st.text_area("Comentário", value=current["comentario"], key=f"com_{ph['id']}")
                    if st.button("Salvar avaliação", key=f"rev_{ph['id']}"):
                        reviews[ph["id"]] = {"status":status, "comentario":comentario}
                        save_data()
                        st.success("Avaliação salva.")
                elif current["comentario"]:
                    st.write("Comentário do nutricionista:")
                    st.info(current["comentario"])
            st.write("---")
    else:
        st.info("Nenhuma foto enviada ainda.")

elif page == "Chat":
    hero("Chat com contexto", f"Conversa de acompanhamento de {pname}.")
    c1, c2 = st.columns([.72,.28], gap="large")
    with c1:
        messages = st.session_state.chat_by_patient[pname]
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for m in messages[-40:]:
            cls = "chat-patient" if m["from"] == "Paciente" else "chat-nutri"
            st.markdown(f"<div class='chat-msg {cls}'><b>{m['from']}</b><br>{m['text']}<br><span class='muted'>{m['time']}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        msg = st.text_area("Mensagem", key="chat_msg")
        sender = "Paciente" if st.session_state.role == "Paciente" else "Nutricionista"
        if st.button("Enviar mensagem", use_container_width=True):
            if msg.strip():
                messages.append({"from": sender, "text": msg.strip(), "time": datetime.now().strftime("%d/%m %H:%M")})
                save_data()
                st.rerun()
    with c2:
        st.markdown('<div class="card-title">Contexto rápido</div>', unsafe_allow_html=True)
        kpi("Calorias", f"{daily['cal']}", f"meta {int(meta_cal)}")
        kpi("Proteína", f"{daily['prot']}g", f"meta {int(meta_prot)}g")
        kpi("Água", f"{daily['water']}ml", f"meta {int(meta_agua)}ml")

elif page == "Check-in":
    hero("Check-in diário", "Mantenha consistência e acompanhe sua sequência.")
    today = date.today().isoformat()
    checked = today in st.session_state.checkins_by_patient[pname]
    c1, c2, c3 = st.columns(3)
    with c1: kpi("Sequência", f"{streak(pname)} dias", "dias consecutivos")
    with c2: kpi("Check-ins", len(st.session_state.checkins_by_patient[pname]), "total")
    with c3: kpi("Hoje", "Feito" if checked else "Pendente", "status")
    if checked:
        st.markdown("<div class='ok-box'>Check-in de hoje já realizado.</div>", unsafe_allow_html=True)
    else:
        if st.button("Fazer check-in de hoje", use_container_width=True):
            st.session_state.checkins_by_patient[pname].append(today)
            save_data()
            st.success("Check-in realizado.")

# ============================================================
# EVOLUTION, PROFILE
# ============================================================
elif page == "Evolução":
    hero("Evolução", f"Histórico real e gráficos de {pname}.")
    hist = st.session_state.history_by_patient[pname]
    if hist:
        df = pd.DataFrame(hist)
        st.dataframe(df, hide_index=True, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card-title">Peso e adesão</div>', unsafe_allow_html=True)
            st.line_chart(df.set_index("data")[["peso","adesao"]])
        with c2:
            st.markdown('<div class="card-title">Consumo</div>', unsafe_allow_html=True)
            st.bar_chart(df.set_index("data")[["cal","prot","water"]])
    else:
        st.info("Sem histórico ainda. Salve o dia no Perfil.")

elif page == "Perfil":
    hero("Perfil", f"Dados de {pname} para cálculo de metas.")
    prof = st.session_state.profile_by_patient[pname]
    c1, c2 = st.columns(2)
    with c1:
        prof["peso"] = st.number_input("Peso (kg)", min_value=20.0, value=float(prof["peso"]))
        prof["altura"] = st.number_input("Altura (cm)", min_value=120, value=int(prof["altura"]))
        prof["idade"] = st.number_input("Idade", min_value=10, value=int(prof["idade"]))
    with c2:
        prof["sexo"] = st.selectbox("Sexo", ["Masculino","Feminino"], index=0 if prof["sexo"]=="Masculino" else 1)
        prof["atividade"] = st.selectbox("Atividade", ["Sedentário","Leve","Moderado","Intenso"], index=["Sedentário","Leve","Moderado","Intenso"].index(prof["atividade"]))
        prof["objetivo"] = st.selectbox("Objetivo", ["Emagrecer","Manter","Ganhar massa"], index=["Emagrecer","Manter","Ganhar massa"].index(prof["objetivo"]))
    if st.button("Salvar perfil e fechar dia", use_container_width=True):
        st.session_state.history_by_patient[pname].append({
            "data": datetime.now().strftime("%d/%m"),
            "peso": prof["peso"],
            **daily,
            "adesao": adherence_for(pname)
        })
        save_data()
        st.success("Perfil salvo e dia adicionado ao histórico.")

# ============================================================
# NUTRI ONLY
# ============================================================
elif page == "Pacientes":
    hero("Pacientes", "Carteira, cadastro e status dos pacientes.")
    with st.expander("Adicionar paciente"):
        nome = st.text_input("Nome do paciente")
        objetivo = st.selectbox("Objetivo", ["Emagrecimento","Hipertrofia","Manutenção","Reeducação"])
        peso = st.number_input("Peso inicial", min_value=20.0, value=80.0)
        if st.button("Cadastrar paciente"):
            if nome:
                st.session_state.patients.append({"Paciente":nome,"Objetivo":objetivo,"Adesão":"0%","Peso":f"{peso:.1f} kg","Status":"Novo"})
                ensure_patient(nome)
                save_data()
                st.success("Paciente cadastrado.")
    rows = []
    for p in st.session_state.patients:
        name = p["Paciente"]
        rows.append({**p, "Adesão atual": f"{adherence_for(name)}%", "Sequência": streak(name), "Alertas": len(generate_alerts(name))})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

elif page == "Plano alimentar":
    hero("Plano alimentar", f"Dieta específica para {pname}.")
    plan = st.session_state.plans[pname]
    meal_name = st.selectbox("Refeição", list(plan.keys()))
    current = plan[meal_name]
    c1, c2 = st.columns([.8, 1.2], gap="large")
    with c1:
        hora = st.text_input("Horário", value=current["hora"])
        orientacao = st.text_area("Orientação da refeição", value=current["orientacao"])
        grupos = sorted(set(f["grupo"] for f in st.session_state.foods))
        filtro = st.multiselect("Filtrar por grupo", grupos, default=grupos)
        food_options = [f["nome"] for f in st.session_state.foods if f["grupo"] in filtro]
        selected = st.multiselect("Alimentos permitidos", food_options, default=current["opcoes"])
        if st.button("Salvar dieta deste paciente", use_container_width=True):
            st.session_state.plans[pname][meal_name] = {"hora":hora, "orientacao":orientacao, "opcoes":selected}
            save_data()
            st.success(f"Dieta de {pname} atualizada.")
    with c2:
        st.markdown('<div class="card-title">Prévia para o paciente</div>', unsafe_allow_html=True)
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

elif page == "Banco de alimentos":
    hero("Banco de alimentos", "Cadastre e organize alimentos usados nos planos.")
    with st.expander("Cadastrar novo alimento"):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome do alimento")
            grupo = st.selectbox("Grupo", ["Carboidrato","Proteína","Fruta","Vegetal","Leguminosa","Gordura","Outro"])
            porcao = st.text_input("Porção", value="100g")
        with c2:
            cal = st.number_input("Calorias", min_value=0, value=100)
            prot = st.number_input("Proteína (g)", min_value=0, value=0)
            carb = st.number_input("Carboidrato (g)", min_value=0, value=0)
            fat = st.number_input("Gordura (g)", min_value=0, value=0)
        if st.button("Adicionar alimento"):
            if nome:
                st.session_state.foods.append({"nome":nome,"grupo":grupo,"porcao":porcao,"cal":cal,"prot":prot,"carb":carb,"fat":fat})
                save_data()
                st.success("Alimento cadastrado.")
    st.dataframe(pd.DataFrame(st.session_state.foods), use_container_width=True, hide_index=True)

elif page == "Relatório semanal":
    hero("Relatório semanal", f"Resumo profissional automático de {pname}.")
    hist = pd.DataFrame(st.session_state.history_by_patient[pname])
    d = daily
    checks = len(st.session_state.checkins_by_patient[pname])
    photos = len(st.session_state.photos_by_patient[pname])
    chats = len(st.session_state.chat_by_patient[pname])
    avg_adesao = round(hist["adesao"].mean()) if not hist.empty and "adesao" in hist else adherence_for(pname)
    delta_weight = "-"
    if not hist.empty and "peso" in hist and len(hist) >= 2:
        delta_weight = round(float(hist["peso"].iloc[-1]) - float(hist["peso"].iloc[0]), 1)
    report = f"""RELATÓRIO SEMANAL — NUTRISYNC

Paciente: {pname}
Adesão média: {avg_adesao}%
Variação de peso: {delta_weight} kg
Check-ins registrados: {checks}
Fotos enviadas: {photos}
Mensagens no chat: {chats}

Resumo do dia atual:
- Calorias: {d['cal']} kcal
- Proteína: {d['prot']}g
- Carboidratos: {d['carb']}g
- Gorduras: {d['fat']}g
- Água: {d['water']}ml

Análise automática:
{chr(10).join(['- ' + a[1] + ': ' + a[2] for a in generate_alerts(pname)])}

Sugestão:
Revisar pontos de baixa adesão, reforçar proteína e hidratação, e acompanhar fotos das refeições com comentários objetivos.
"""
    st.text_area("Relatório gerado", value=report, height=380)
    st.download_button("Baixar relatório em TXT", report, file_name=f"relatorio_{pname.replace(' ','_')}.txt", use_container_width=True)

elif page == "Calculadora clínica":
    hero("Calculadora clínica", f"Metas de {pname}.")
    prof = st.session_state.profile_by_patient[pname]
    c1, c2 = st.columns([.9, 1.1], gap="large")
    with c1:
        sexo = st.selectbox("Sexo", ["Masculino","Feminino"], index=0 if prof["sexo"]=="Masculino" else 1)
        idade = st.number_input("Idade", min_value=10, value=int(prof["idade"]))
        peso = st.number_input("Peso (kg)", min_value=20.0, value=float(prof["peso"]))
        altura = st.number_input("Altura (cm)", min_value=120, value=int(prof["altura"]))
        atividade = st.selectbox("Nível de atividade", ["Sedentário","Leve","Moderado","Intenso"], index=["Sedentário","Leve","Moderado","Intenso"].index(prof["atividade"]))
        objetivo = st.selectbox("Objetivo", ["Emagrecer","Manter","Ganhar massa"], index=["Emagrecer","Manter","Ganhar massa"].index(prof["objetivo"]))
        if st.button("Salvar metas no paciente", use_container_width=True):
            st.session_state.profile_by_patient[pname] = {"peso":peso,"altura":altura,"idade":idade,"sexo":sexo,"atividade":atividade,"objetivo":objetivo}
            save_data()
            st.success("Metas salvas.")
    with c2:
        imc2, tmb2, gasto2, meta2, prot2, fat2, carb2, agua2 = calc_clinica(peso, altura, idade, sexo, atividade, objetivo)
        c21, c22 = st.columns(2)
        with c21:
            kpi("IMC", f"{imc2:.1f}", "índice corporal")
            kpi("Gasto total", f"{int(gasto2)}", "kcal/dia")
            kpi("Proteína", f"{int(prot2)}g", "meta diária")
        with c22:
            kpi("TMB", f"{int(tmb2)}", "kcal basal")
            kpi("Meta calórica", f"{int(meta2)}", "kcal/dia")
            kpi("Água", f"{int(agua2)}ml", "estimativa diária")

elif page == "Configurações":
    hero("Configurações", "Gerencie dados locais e lembretes.")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.notification_settings["water"] = st.checkbox("Lembretes de água", value=st.session_state.notification_settings.get("water", True))
        st.session_state.notification_settings["meal"] = st.checkbox("Lembretes de refeição", value=st.session_state.notification_settings.get("meal", True))
        st.session_state.notification_settings["protein"] = st.checkbox("Alertas de proteína", value=st.session_state.notification_settings.get("protein", True))
        if st.button("Salvar configurações", use_container_width=True):
            save_data()
            st.success("Configurações salvas.")
    with c2:
        if st.button("Zerar consumo do paciente ativo", use_container_width=True):
            st.session_state.daily_by_patient[pname] = {"cal":0,"prot":0,"carb":0,"fat":0,"water":0}
            st.session_state.water_by_patient[pname] = []
            save_data()
            st.success("Consumo zerado.")
