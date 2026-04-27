
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NutriSync", page_icon="🥗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #f3f7f2;
    --dark: #103b2c;
    --dark2: #0b2b20;
    --green: #24a66a;
    --green2: #188653;
    --soft: #e8f7ef;
    --text: #13231c;
    --muted: #718078;
    --line: #dfe9e2;
    --white: #ffffff;
}

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(36,166,106,.12), transparent 32%),
        linear-gradient(180deg, #f7faf5 0%, #edf5ed 100%);
    color: var(--text);
}

/* remove cara padrão */
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.7rem; padding-bottom: 3rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123b2d 0%, #09261d 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 28px;
}

.side-logo {
    color: white;
    font-size: 31px;
    font-weight: 900;
    letter-spacing: -.9px;
    margin-bottom: 4px;
}
.side-logo span { color: #7df0ae; }
.side-sub {
    color: #a7f3d0;
    font-size: 13px;
    margin-bottom: 22px;
}

/* Botões de navegação em caixa */
.nav-btn button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    border-radius: 16px !important;
    padding: 13px 15px !important;
    margin: 2px 0 !important;
    background: rgba(255,255,255,.07) !important;
    color: #ecfdf5 !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}

.nav-btn button:hover {
    background: rgba(125,240,174,.18) !important;
    color: white !important;
}

.nav-active {
    background: linear-gradient(135deg, #24a66a, #13834e);
    color: white;
    border-radius: 16px;
    padding: 13px 15px;
    margin: 6px 0;
    font-weight: 900;
    box-shadow: 0 12px 24px rgba(36,166,106,.26);
}

/* Corrige campos brancos/letras invisíveis */
input, textarea, select {
    color: #13231c !important;
    background: #ffffff !important;
    border: 1px solid #dbe7df !important;
    border-radius: 14px !important;
}

[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] div {
    color: #13231c !important;
    background-color: #ffffff !important;
}

[data-baseweb="select"] span {
    color: #13231c !important;
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
    color: #263d32 !important;
    font-weight: 800 !important;
}

.stMarkdown, p, span, div {
    color: inherit;
}

/* Cards */
.hero {
    background: linear-gradient(135deg, #143d2e 0%, #1e8d58 100%);
    color: white;
    border-radius: 32px;
    padding: 28px;
    box-shadow: 0 24px 60px rgba(16,59,44,.22);
    min-height: 170px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 999px;
    right: -55px;
    top: -75px;
    background: rgba(255,255,255,.11);
}
.hero h1 {
    color: white;
    margin: 0;
    font-size: 36px;
    font-weight: 900;
    letter-spacing: -1px;
}
.hero p {
    color: rgba(255,255,255,.83);
    font-weight: 600;
    max-width: 680px;
}

.card {
    background: rgba(255,255,255,.92);
    border: 1px solid rgba(223,233,226,.95);
    border-radius: 28px;
    padding: 22px;
    box-shadow: 0 18px 45px rgba(16,59,44,.08);
    min-height: 128px;
}

.card-title {
    color: #123b2d;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 6px;
}

.muted {
    color: #718078;
    font-size: 14px;
    font-weight: 600;
}

.kpi-label {
    color: #718078;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .4px;
}
.kpi-value {
    color: #123b2d;
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -.8px;
    margin-top: 7px;
}
.kpi-foot {
    color: #24a66a;
    font-size: 13px;
    font-weight: 900;
    margin-top: 8px;
}

.meal {
    background: white;
    border: 1px solid #dfe9e2;
    border-radius: 22px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 10px 25px rgba(16,59,44,.05);
}
.meal-head {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: start;
}
.meal-title {
    color: #123b2d;
    font-weight: 900;
    font-size: 18px;
}
.meal-time {
    background: #e8f7ef;
    color: #188653;
    padding: 7px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
}
.badge {
    display: inline-block;
    background: #eef8f2;
    color: #188653;
    border: 1px solid #cdeedb;
    border-radius: 999px;
    padding: 6px 10px;
    margin: 9px 5px 0 0;
    font-size: 12px;
    font-weight: 900;
}
.ok-box {
    background: #e8f7ef;
    color: #166534;
    border: 1px solid #bce7cc;
    border-radius: 18px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}
.warn-box {
    background: #fff7ed;
    color: #9a3412;
    border: 1px solid #fed7aa;
    border-radius: 18px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}
.danger-box {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 18px;
    padding: 14px 16px;
    font-weight: 800;
    margin: 9px 0;
}

.stButton > button {
    border-radius: 15px !important;
    border: none !important;
    background: linear-gradient(135deg, #24a66a, #168650) !important;
    color: white !important;
    font-weight: 900 !important;
    padding: 12px 18px !important;
    box-shadow: 0 12px 24px rgba(36,166,106,.2) !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, #1f965e, #126f43) !important;
    color: white !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
}

/* Métricas padrão */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dfe9e2;
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 16px 38px rgba(16,59,44,.07);
}
[data-testid="stMetricLabel"] * {
    color: #718078 !important;
    font-weight: 800 !important;
}
[data-testid="stMetricValue"] {
    color: #123b2d !important;
    font-weight: 900 !important;
}

/* Radio escondido não usado */
.stRadio { display: none; }

hr { border: none; border-top: 1px solid #dfe9e2; margin: 20px 0; }

@media(max-width: 800px) {
    .hero h1 { font-size: 29px; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False
if "role" not in st.session_state:
    st.session_state.role = "Paciente"
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "nome" not in st.session_state:
    st.session_state.nome = "Lorran Ribeiro"
if "daily" not in st.session_state:
    st.session_state.daily = {"cal": 0, "prot": 0, "carb": 0, "fat": 0, "water": 0}
if "meals" not in st.session_state:
    st.session_state.meals = [
        {"refeicao": "Café da manhã", "hora": "07:30", "alimentos": "Ovos mexidos, pão integral, banana e café sem açúcar", "cal": 450, "prot": 28, "carb": 48, "fat": 16},
        {"refeicao": "Almoço", "hora": "12:30", "alimentos": "Arroz, feijão, frango grelhado, legumes e salada", "cal": 720, "prot": 48, "carb": 82, "fat": 18},
        {"refeicao": "Lanche", "hora": "16:00", "alimentos": "Iogurte natural, aveia e fruta", "cal": 310, "prot": 22, "carb": 42, "fat": 7},
        {"refeicao": "Jantar", "hora": "20:00", "alimentos": "Carne magra, batata doce, legumes e salada", "cal": 590, "prot": 44, "carb": 55, "fat": 19},
    ]
if "patients" not in st.session_state:
    st.session_state.patients = [
        {"Paciente": "Lorran Ribeiro", "Objetivo": "Emagrecimento", "Adesão": "84%", "Peso": "80.0 kg", "Status": "Em dia"},
        {"Paciente": "Paciente Demo", "Objetivo": "Hipertrofia", "Adesão": "71%", "Peso": "72.5 kg", "Status": "Atenção"},
        {"Paciente": "Paciente Teste", "Objetivo": "Manutenção", "Adesão": "93%", "Peso": "64.2 kg", "Status": "Excelente"},
    ]

def calc_clinica(peso, altura, idade, sexo, atividade, objetivo):
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    tmb = 10 * peso + 6.25 * altura - 5 * idade + (5 if sexo == "Masculino" else -161)
    gasto = tmb * atividade
    meta = gasto - 500 if objetivo == "Emagrecer" else gasto + 300 if objetivo == "Ganhar massa" else gasto
    prot = peso * 2
    gordura = peso * 0.8
    carbo = max((meta - (prot * 4 + gordura * 9)) / 4, 0)
    agua = peso * 35
    return imc, tmb, gasto, meta, prot, gordura, carbo, agua

def pct(v, goal):
    return min(v / goal, 1.0) if goal else 0

def hero(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
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
    active = st.session_state.page == page
    if active:
        st.sidebar.markdown(f"<div class='nav-active'>{label}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.sidebar.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if not st.session_state.logged:
    c1, c2 = st.columns([1.25, .75], gap="large")
    with c1:
        st.markdown("""
        <div class="hero" style="min-height:560px;padding:42px;">
            <h1 style="font-size:48px;">NutriSync</h1>
            <p style="font-size:19px;max-width:760px;">Controle nutricional com plano alimentar, registro diário, metas, cálculo clínico e acompanhamento visual.</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px;">
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:22px;">
                    <b style="font-size:18px;color:white;">Paciente</b><br>
                    <span style="color:rgba(255,255,255,.82);">Acessa dieta, marca refeições e acompanha calorias, proteína e água.</span>
                </div>
                <div style="background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:22px;">
                    <b style="font-size:18px;color:white;">Nutricionista</b><br>
                    <span style="color:rgba(255,255,255,.82);">Cria planos, calcula metas e acompanha pacientes em um painel limpo.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card' style='margin-top:52px;'>", unsafe_allow_html=True)
        st.subheader("Entrar")
        st.caption("Ambiente demo")
        role = st.selectbox("Escolha seu perfil", ["Paciente", "Nutricionista"])
        nome = st.text_input("Nome", value="Lorran Ribeiro")
        senha = st.text_input("Senha", value="demo", type="password")
        if st.button("Acessar painel", use_container_width=True):
            st.session_state.logged = True
            st.session_state.role = role
            st.session_state.nome = nome
            st.session_state.page = "Dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("<div class='side-logo'>Nutri<span>Sync</span></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='side-sub'>{st.session_state.role} • {st.session_state.nome}</div>", unsafe_allow_html=True)

if st.session_state.role == "Paciente":
    pages = [
        ("📊 Dashboard", "Dashboard"),
        ("🍽️ Minha dieta", "Minha dieta"),
        ("✅ Registrar dia", "Registrar dia"),
        ("📈 Evolução", "Evolução"),
        ("💬 Assistente", "Assistente"),
    ]
else:
    pages = [
        ("📊 Dashboard", "Dashboard"),
        ("👥 Pacientes", "Pacientes"),
        ("🍽️ Criar dieta", "Criar dieta"),
        ("🧮 Calculadora", "Calculadora clínica"),
        ("📄 Relatórios", "Relatórios"),
    ]

for label, page in pages:
    nav_button(label, page)

st.sidebar.write("")
st.sidebar.write("")
if st.sidebar.button("Sair", use_container_width=True):
    st.session_state.logged = False
    st.rerun()

# metas demo
imc, tmb, gasto, meta_cal, meta_prot, meta_fat, meta_carb, meta_agua = calc_clinica(80, 180, 25, "Masculino", 1.55, "Emagrecer")
page = st.session_state.page

# ---------------- PACIENTE ----------------
if st.session_state.role == "Paciente":

    if page == "Dashboard":
        hero("Dashboard do Paciente", "Resumo claro do dia, metas principais e próximos passos.")
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
            st.write("Calorias")
            st.progress(pct(d["cal"], meta_cal))
            st.caption(f"{d['cal']} / {int(meta_cal)} kcal")
            st.write("Proteína")
            st.progress(pct(d["prot"], meta_prot))
            st.caption(f"{d['prot']} / {int(meta_prot)}g")
            st.write("Água")
            st.progress(pct(d["water"], meta_agua))
            st.caption(f"{d['water']} / {int(meta_agua)}ml")
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Feedback inteligente</div>", unsafe_allow_html=True)
            if d["prot"] < meta_prot:
                st.markdown(f"<div class='warn-box'>Faltam {int(meta_prot - d['prot'])}g de proteína hoje.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ok-box'>Proteína batida. Excelente.</div>", unsafe_allow_html=True)
            if d["cal"] > meta_cal:
                st.markdown(f"<div class='danger-box'>Você passou {int(d['cal'] - meta_cal)} kcal da meta.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ok-box'>Ainda restam {int(meta_cal - d['cal'])} kcal disponíveis.</div>", unsafe_allow_html=True)
            if d["water"] < meta_agua:
                st.markdown(f"<div class='warn-box'>Beba mais {int(meta_agua - d['water'])}ml de água.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Minha dieta":
        hero("Minha dieta", "Plano alimentar separado por horário, com macros e registro rápido.")
        for i, meal in enumerate(st.session_state.meals):
            st.markdown(f"""
            <div class="meal">
                <div class="meal-head">
                    <div>
                        <div class="meal-title">{meal['refeicao']}</div>
                        <div class="muted">{meal['alimentos']}</div>
                    </div>
                    <div class="meal-time">{meal['hora']}</div>
                </div>
                <span class="badge">{meal['cal']} kcal</span>
                <span class="badge">{meal['prot']}g proteína</span>
                <span class="badge">{meal['carb']}g carbo</span>
                <span class="badge">{meal['fat']}g gordura</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Marcar como consumido", key=f"eat_{i}"):
                st.session_state.daily["cal"] += meal["cal"]
                st.session_state.daily["prot"] += meal["prot"]
                st.session_state.daily["carb"] += meal["carb"]
                st.session_state.daily["fat"] += meal["fat"]
                st.success("Refeição adicionada ao dia.")

    elif page == "Registrar dia":
        hero("Registrar dia", "Atualize manualmente seu consumo de hoje.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.daily["cal"] = st.number_input("Calorias consumidas", min_value=0, value=st.session_state.daily["cal"])
            st.session_state.daily["prot"] = st.number_input("Proteína consumida (g)", min_value=0, value=st.session_state.daily["prot"])
        with c2:
            st.session_state.daily["carb"] = st.number_input("Carboidrato (g)", min_value=0, value=st.session_state.daily["carb"])
            st.session_state.daily["fat"] = st.number_input("Gordura (g)", min_value=0, value=st.session_state.daily["fat"])
        with c3:
            st.session_state.daily["water"] = st.number_input("Água (ml)", min_value=0, value=st.session_state.daily["water"], step=250)
            peso = st.number_input("Peso de hoje (kg)", min_value=20.0, value=80.0)
        st.markdown("<div class='ok-box'>Registro atualizado no painel.</div>", unsafe_allow_html=True)

    elif page == "Evolução":
        hero("Evolução", "Histórico visual simples para acompanhar progresso.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Peso</div>", unsafe_allow_html=True)
            st.line_chart(pd.DataFrame({"Peso": [82, 81.4, 80.9, 80.3, 80.0], "Meta": [79, 79, 79, 79, 79]}))
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Adesão</div>", unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({"Adesão": [72, 81, 76, 88, 84]}))
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Assistente":
        hero("Assistente", "Orientações rápidas com base no seu dia.")
        msg = st.text_area("Como foi sua dieta hoje?")
        if st.button("Gerar sugestão"):
            d = st.session_state.daily
            if d["prot"] < meta_prot:
                st.markdown("<div class='warn-box'>Priorize uma fonte de proteína na próxima refeição: ovos, frango, iogurte, carne magra ou whey.</div>", unsafe_allow_html=True)
            elif d["cal"] > meta_cal:
                st.markdown("<div class='warn-box'>Amanhã reduza beliscos fora do plano e calorias líquidas.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ok-box'>Seu dia está bem alinhado. Mantenha o padrão e registre água.</div>", unsafe_allow_html=True)

# ---------------- NUTRICIONISTA ----------------
else:

    if page == "Dashboard":
        hero("Dashboard do Nutricionista", "Pacientes, adesão, planos ativos e alertas em um painel limpo.")
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi("Pacientes ativos", "12", "+3 este mês")
        with c2: kpi("Adesão média", "84%", "últimos 7 dias")
        with c3: kpi("Planos ativos", "9", "em acompanhamento")
        with c4: kpi("Alertas", "4", "precisam de revisão")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Carteira de pacientes</div>", unsafe_allow_html=True)
        for p in st.session_state.patients:
            nome = p["Paciente"]
            adesao = int(p["Adesão"].replace("%", ""))
            st.write(f"**{nome}** — {p['Objetivo']} • {p['Peso']} • {p['Status']}")
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
                st.success("Paciente cadastrado.")
        st.dataframe(st.session_state.patients, use_container_width=True, hide_index=True)

    elif page == "Criar dieta":
        hero("Criar dieta", "Monte o plano alimentar que aparecerá para o paciente.")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        refeicao = st.text_input("Refeição", value="Café da manhã")
        hora = st.text_input("Horário", value="07:30")
        alimentos = st.text_area("Alimentos", value="Ovos mexidos, pão integral e banana")
        c1, c2, c3, c4 = st.columns(4)
        with c1: cal = st.number_input("Calorias", min_value=0, value=450)
        with c2: prot = st.number_input("Proteína", min_value=0, value=28)
        with c3: carb = st.number_input("Carboidrato", min_value=0, value=48)
        with c4: fat = st.number_input("Gordura", min_value=0, value=16)
        if st.button("Adicionar ao plano"):
            st.session_state.meals.append({"refeicao": refeicao, "hora": hora, "alimentos": alimentos, "cal": cal, "prot": prot, "carb": carb, "fat": fat})
            st.success("Refeição adicionada ao plano do paciente.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Plano atual")
        for meal in st.session_state.meals:
            st.markdown(f"""
            <div class="meal">
                <div class="meal-head">
                    <div><div class="meal-title">{meal['refeicao']}</div><div class="muted">{meal['alimentos']}</div></div>
                    <div class="meal-time">{meal['hora']}</div>
                </div>
                <span class="badge">{meal['cal']} kcal</span>
                <span class="badge">{meal['prot']}g proteína</span>
                <span class="badge">{meal['carb']}g carbo</span>
                <span class="badge">{meal['fat']}g gordura</span>
            </div>
            """, unsafe_allow_html=True)

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
            fator = {"Sedentário": 1.2, "Leve": 1.375, "Moderado": 1.55, "Intenso": 1.725}[atividade_nome]
            objetivo = st.selectbox("Objetivo", ["Emagrecer", "Manter", "Ganhar massa"])
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            imc, tmb, gasto, meta, prot, fat, carb, agua = calc_clinica(peso, altura, idade, sexo, fator, objetivo)
            r1, r2 = st.columns(2)
            with r1:
                kpi("IMC", f"{imc:.1f}", "índice corporal")
                kpi("Gasto total", f"{int(gasto)}", "kcal/dia")
                kpi("Proteína", f"{int(prot)}g", "meta diária")
            with r2:
                kpi("TMB", f"{int(tmb)}", "kcal basal")
                kpi("Meta calórica", f"{int(meta)}", "kcal/dia")
                kpi("Água", f"{int(agua)}ml", "estimativa diária")

    elif page == "Relatórios":
        hero("Relatórios", "Resumo semanal para decisão do nutricionista.")
        st.markdown("""
        <div class="card">
            <div class="card-title">Resumo semanal</div>
            <p><b>Paciente:</b> Lorran Ribeiro</p>
            <p><b>Adesão média:</b> 84%</p>
            <p><b>Peso:</b> 82kg → 80kg</p>
            <p><b>Ponto de atenção:</b> proteína abaixo da meta em 2 dias.</p>
            <div class="ok-box">Sugestão: manter calorias e reforçar proteína no café da manhã e no lanche.</div>
        </div>
        """, unsafe_allow_html=True)
