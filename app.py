
import streamlit as st

st.set_page_config(page_title="NutriSync", page_icon="🥗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
*{font-family:'Inter',sans-serif}
.stApp{background:#f4f7f3}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#12372a,#0f2d23)}
[data-testid="stSidebar"] *{color:#ecfdf5!important}
.main-title{font-size:34px;font-weight:800;color:#12372a;margin-bottom:4px}
.subtitle{color:#6b7280;font-size:15px;margin-bottom:22px}
.card{background:white;border:1px solid #e5e7eb;border-radius:24px;padding:22px;box-shadow:0 14px 35px rgba(15,45,35,.07);min-height:130px}
.metric-label{color:#6b7280;font-size:14px;font-weight:600}
.metric-value{color:#1f8f5f;font-size:30px;font-weight:800;margin-top:8px}
.small{color:#6b7280;font-size:13px}
.green-box{background:#eaf7ef;border:1px solid #bce7cc;color:#166534;border-radius:18px;padding:16px;font-weight:600}
.warn-box{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:18px;padding:16px;font-weight:600}
.food-card{background:#fff;border:1px solid #e5e7eb;border-radius:20px;padding:18px;margin-bottom:12px}
.food-title{font-weight:800;color:#12372a;font-size:18px}
.badge{display:inline-block;background:#eaf7ef;color:#1f8f5f;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:800;margin-right:6px;margin-top:10px}
.stButton>button{border-radius:14px;background:#1f8f5f;color:white;border:none;font-weight:800;padding:12px 18px}
.stButton>button:hover{background:#166b49;color:white;border:none}
[data-testid="stMetric"]{background:white;border:1px solid #e5e7eb;border-radius:24px;padding:18px;box-shadow:0 14px 35px rgba(15,45,35,.06)}
</style>
""", unsafe_allow_html=True)

if "logged" not in st.session_state: st.session_state.logged=False
if "role" not in st.session_state: st.session_state.role="Paciente"
if "nome" not in st.session_state: st.session_state.nome="Lorran Ribeiro"
if "daily" not in st.session_state: st.session_state.daily={"cal":0,"prot":0,"carb":0,"fat":0,"water":0}
if "meals" not in st.session_state:
    st.session_state.meals=[
        {"refeicao":"Café da manhã","hora":"07:30","alimentos":"Ovos mexidos, pão integral e banana","cal":450,"prot":28,"carb":48,"fat":16},
        {"refeicao":"Almoço","hora":"12:30","alimentos":"Arroz, feijão, frango grelhado e salada","cal":720,"prot":48,"carb":82,"fat":18},
        {"refeicao":"Lanche","hora":"16:00","alimentos":"Iogurte natural, aveia e fruta","cal":310,"prot":22,"carb":42,"fat":7},
        {"refeicao":"Jantar","hora":"20:00","alimentos":"Carne magra, legumes e batata doce","cal":590,"prot":44,"carb":55,"fat":19},
    ]
if "patients" not in st.session_state:
    st.session_state.patients=[
        {"nome":"Lorran Ribeiro","objetivo":"Emagrecimento","adesao":84,"peso":80.0},
        {"nome":"Paciente Demo","objetivo":"Hipertrofia","adesao":71,"peso":72.5},
        {"nome":"Paciente Teste","objetivo":"Manutenção","adesao":93,"peso":64.2},
    ]

def calc_clinica(peso, altura, idade, sexo, atividade, objetivo):
    altura_m=altura/100
    imc=peso/(altura_m**2)
    tmb=10*peso+6.25*altura-5*idade+(5 if sexo=="Masculino" else -161)
    gasto=tmb*atividade
    meta=gasto-500 if objetivo=="Emagrecer" else gasto+300 if objetivo=="Ganhar massa" else gasto
    prot=peso*2.0
    fat=peso*.8
    carb=max((meta-(prot*4+fat*9))/4,0)
    agua=peso*35
    return imc,tmb,gasto,meta,prot,fat,carb,agua

def pct(v,g): return min(v/g,1.0) if g else 0
def header(t,s):
    st.markdown(f"<div class='main-title'>{t}</div><div class='subtitle'>{s}</div>",unsafe_allow_html=True)
def card_metric(label,value,hint=""):
    st.markdown(f"<div class='card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='small'>{hint}</div></div>",unsafe_allow_html=True)

# Login
if not st.session_state.logged:
    left,right=st.columns([1.15,.85],gap="large")
    with left:
        st.markdown("""
        <div style="padding:38px;border-radius:32px;background:linear-gradient(135deg,#12372a,#1f8f5f);color:white;min-height:520px;box-shadow:0 20px 55px rgba(18,55,42,.18)">
        <div style="font-size:42px;font-weight:900;margin-bottom:14px;">NutriSync</div>
        <div style="font-size:21px;font-weight:700;line-height:1.4;margin-bottom:24px;">Gestão nutricional com dieta, metas, adesão e evolução.</div>
        <div style="background:rgba(255,255,255,.12);padding:18px;border-radius:22px;margin-bottom:14px;"><b>Paciente</b><br>Visualiza dieta, registra refeições, água, calorias e macros.</div>
        <div style="background:rgba(255,255,255,.12);padding:18px;border-radius:22px;margin-bottom:14px;"><b>Nutricionista</b><br>Cadastra pacientes, monta planos e acompanha adesão.</div>
        <div style="background:rgba(255,255,255,.12);padding:18px;border-radius:22px;"><b>Feedback automático</b><br>Alertas práticos com base no consumo e nas metas.</div>
        </div>""",unsafe_allow_html=True)
    with right:
        st.markdown("<br><br>",unsafe_allow_html=True)
        st.subheader("Entrar no sistema")
        st.caption("Versão demonstrativa para uso pessoal")
        st.session_state.role=st.radio("Perfil",["Paciente","Nutricionista"],horizontal=True)
        st.session_state.nome=st.text_input("Nome",value=st.session_state.nome)
        st.text_input("Senha",value="demo",type="password")
        if st.button("Acessar NutriSync",use_container_width=True):
            st.session_state.logged=True
            st.rerun()
    st.stop()

st.sidebar.markdown("## NutriSync")
st.sidebar.caption(f"{st.session_state.role} • {st.session_state.nome}")
if st.sidebar.button("Sair",use_container_width=True):
    st.session_state.logged=False
    st.rerun()

if st.session_state.role=="Paciente":
    page=st.sidebar.radio("Menu",["Dashboard","Minha dieta","Registrar dia","Evolução","Assistente"],label_visibility="collapsed")
else:
    page=st.sidebar.radio("Menu",["Dashboard","Pacientes","Criar dieta","Calculadora clínica","Relatórios"],label_visibility="collapsed")

imc,tmb,gasto,meta_cal,meta_prot,meta_fat,meta_carb,meta_agua=calc_clinica(80,180,25,"Masculino",1.55,"Emagrecer")

if st.session_state.role=="Paciente":
    if page=="Dashboard":
        header("Dashboard do Paciente","Resumo do dia, metas principais e próximos passos.")
        d=st.session_state.daily
        c1,c2,c3,c4=st.columns(4)
        with c1: card_metric("Calorias",f"{d['cal']} kcal",f"Meta: {int(meta_cal)} kcal")
        with c2: card_metric("Proteína",f"{d['prot']} g",f"Meta: {int(meta_prot)} g")
        with c3: card_metric("Água",f"{d['water']} ml",f"Meta: {int(meta_agua)} ml")
        adesao=round((pct(d["cal"],meta_cal)+pct(d["prot"],meta_prot)+pct(d["water"],meta_agua))/3*100)
        with c4: card_metric("Adesão",f"{adesao}%","Média do dia")
        left,right=st.columns([1.2,.8],gap="large")
        with left:
            st.markdown("<div class='card'>",unsafe_allow_html=True)
            st.subheader("Progresso de hoje")
            st.write("Calorias"); st.progress(pct(d["cal"],meta_cal)); st.write(f"{d['cal']} / {int(meta_cal)} kcal")
            st.write("Proteína"); st.progress(pct(d["prot"],meta_prot)); st.write(f"{d['prot']} / {int(meta_prot)} g")
            st.write("Água"); st.progress(pct(d["water"],meta_agua)); st.write(f"{d['water']} / {int(meta_agua)} ml")
            st.markdown("</div>",unsafe_allow_html=True)
        with right:
            st.markdown("<div class='card'>",unsafe_allow_html=True)
            st.subheader("Feedback")
            if d["prot"]<meta_prot: st.markdown(f"<div class='warn-box'>Faltam {int(meta_prot-d['prot'])}g de proteína hoje.</div>",unsafe_allow_html=True)
            else: st.markdown("<div class='green-box'>Proteína batida. Excelente.</div>",unsafe_allow_html=True)
            st.write("")
            if d["cal"]>meta_cal: st.markdown(f"<div class='warn-box'>Você passou {int(d['cal']-meta_cal)} kcal da meta.</div>",unsafe_allow_html=True)
            else: st.markdown(f"<div class='green-box'>Você ainda tem {int(meta_cal-d['cal'])} kcal disponíveis.</div>",unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)

    elif page=="Minha dieta":
        header("Minha dieta","Plano alimentar organizado por refeição.")
        for i,meal in enumerate(st.session_state.meals):
            st.markdown(f"<div class='food-card'><div class='food-title'>{meal['refeicao']} • {meal['hora']}</div><div class='small'>{meal['alimentos']}</div><span class='badge'>{meal['cal']} kcal</span><span class='badge'>{meal['prot']}g proteína</span><span class='badge'>{meal['carb']}g carbo</span><span class='badge'>{meal['fat']}g gordura</span></div>",unsafe_allow_html=True)
            if st.button(f"Marcar como consumido: {meal['refeicao']}",key=f"eat_{i}"):
                for k in ["cal","prot","carb","fat"]: st.session_state.daily[k]+=meal[k]
                st.success("Refeição adicionada ao seu dia.")

    elif page=="Registrar dia":
        header("Registrar dia","Atualize manualmente o que você consumiu hoje.")
        c1,c2,c3=st.columns(3)
        with c1:
            st.session_state.daily["cal"]=st.number_input("Calorias",min_value=0,value=st.session_state.daily["cal"])
            st.session_state.daily["prot"]=st.number_input("Proteína (g)",min_value=0,value=st.session_state.daily["prot"])
        with c2:
            st.session_state.daily["carb"]=st.number_input("Carboidrato (g)",min_value=0,value=st.session_state.daily["carb"])
            st.session_state.daily["fat"]=st.number_input("Gordura (g)",min_value=0,value=st.session_state.daily["fat"])
        with c3:
            st.session_state.daily["water"]=st.number_input("Água (ml)",min_value=0,value=st.session_state.daily["water"],step=250)
            st.number_input("Peso de hoje (kg)",min_value=20.0,value=80.0)
        st.success("Dados atualizados no painel.")

    elif page=="Evolução":
        header("Evolução","Acompanhamento simples para uso pessoal.")
        st.line_chart({"Peso":[82,81.4,80.9,80.3,80.0],"Meta":[79,79,79,79,79]})
        st.bar_chart({"Adesão":[72,81,76,88,84]})

    else:
        header("Assistente","Sugestões rápidas com base na sua rotina.")
        st.text_area("Escreva como foi seu dia")
        if st.button("Gerar sugestão"):
            d=st.session_state.daily
            if d["prot"]<meta_prot: st.markdown("<div class='warn-box'>Priorize uma fonte de proteína na próxima refeição: ovos, frango, iogurte, carne magra ou whey.</div>",unsafe_allow_html=True)
            elif d["cal"]>meta_cal: st.markdown("<div class='warn-box'>Amanhã tente reduzir calorias líquidas e beliscos fora do plano.</div>",unsafe_allow_html=True)
            else: st.markdown("<div class='green-box'>Seu dia está bem alinhado. Mantenha o padrão e registre água.</div>",unsafe_allow_html=True)

else:
    if page=="Dashboard":
        header("Dashboard do Nutricionista","Visão geral dos pacientes, adesão e planos ativos.")
        c1,c2,c3,c4=st.columns(4)
        with c1: card_metric("Pacientes ativos","12","+3 este mês")
        with c2: card_metric("Adesão média","84%","últimos 7 dias")
        with c3: card_metric("Planos ativos","9","em acompanhamento")
        with c4: card_metric("Alertas","4","precisam de revisão")
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader("Carteira de pacientes")
        for p in st.session_state.patients:
            st.write(f"**{p['nome']}** — {p['objetivo']} • {p['peso']} kg")
            st.progress(p["adesao"]/100)
            st.caption(f"Adesão: {p['adesao']}%")
        st.markdown("</div>",unsafe_allow_html=True)

    elif page=="Pacientes":
        header("Pacientes","Cadastro e acompanhamento rápido.")
        with st.expander("Adicionar paciente"):
            nome=st.text_input("Nome do paciente")
            objetivo=st.selectbox("Objetivo",["Emagrecimento","Hipertrofia","Manutenção"])
            peso=st.number_input("Peso inicial",min_value=20.0,value=80.0)
            if st.button("Cadastrar paciente"):
                st.session_state.patients.append({"nome":nome or "Novo paciente","objetivo":objetivo,"adesao":0,"peso":peso})
                st.success("Paciente cadastrado.")
        st.dataframe(st.session_state.patients,use_container_width=True)

    elif page=="Criar dieta":
        header("Criar dieta","Monte o plano alimentar que o paciente verá no app.")
        refeicao=st.text_input("Refeição",value="Café da manhã")
        hora=st.text_input("Horário",value="07:30")
        alimentos=st.text_area("Alimentos",value="Ovos mexidos, pão integral e banana")
        c1,c2,c3,c4=st.columns(4)
        with c1: cal=st.number_input("Calorias",min_value=0,value=450)
        with c2: prot=st.number_input("Proteína",min_value=0,value=28)
        with c3: carb=st.number_input("Carboidrato",min_value=0,value=48)
        with c4: fat=st.number_input("Gordura",min_value=0,value=16)
        if st.button("Adicionar ao plano"):
            st.session_state.meals.append({"refeicao":refeicao,"hora":hora,"alimentos":alimentos,"cal":cal,"prot":prot,"carb":carb,"fat":fat})
            st.success("Refeição adicionada ao plano do paciente.")
        st.subheader("Plano atual")
        for meal in st.session_state.meals:
            st.markdown(f"**{meal['refeicao']} ({meal['hora']})** — {meal['alimentos']}  \n{meal['cal']} kcal • {meal['prot']}g proteína")

    elif page=="Calculadora clínica":
        header("Calculadora clínica","Calcule IMC, TMB, gasto energético, meta calórica e macros.")
        c1,c2=st.columns([.9,1.1],gap="large")
        with c1:
            sexo=st.selectbox("Sexo",["Masculino","Feminino"])
            idade=st.number_input("Idade",min_value=10,value=25)
            peso=st.number_input("Peso (kg)",min_value=20.0,value=80.0)
            altura=st.number_input("Altura (cm)",min_value=120,value=180)
            atividade_nome=st.selectbox("Nível de atividade",["Sedentário","Leve","Moderado","Intenso"])
            fator={"Sedentário":1.2,"Leve":1.375,"Moderado":1.55,"Intenso":1.725}[atividade_nome]
            objetivo=st.selectbox("Objetivo",["Emagrecer","Manter","Ganhar massa"])
        with c2:
            imc,tmb,gasto,meta,prot,fat,carb,agua=calc_clinica(peso,altura,idade,sexo,fator,objetivo)
            c21,c22=st.columns(2)
            with c21:
                st.metric("IMC",f"{imc:.1f}"); st.metric("TMB",f"{int(tmb)} kcal"); st.metric("Meta calórica",f"{int(meta)} kcal")
            with c22:
                st.metric("Proteína",f"{int(prot)} g"); st.metric("Carboidrato",f"{int(carb)} g"); st.metric("Água",f"{int(agua)} ml")

    else:
        header("Relatórios","Resumo simples para tomada de decisão.")
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader("Resumo semanal")
        st.write("Paciente: **Lorran Ribeiro**")
        st.write("Adesão média: **84%**")
        st.write("Peso: **82kg → 80kg**")
        st.write("Ponto de atenção: consumo de proteína abaixo da meta em 2 dias.")
        st.markdown("<div class='green-box'>Sugestão: manter calorias e reforçar proteína no café da manhã e lanche.</div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
