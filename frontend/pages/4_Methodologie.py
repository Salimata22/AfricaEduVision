import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="Méthodologie - AfricaEduVision", page_icon="🌍", layout="wide")

# =========================
# CSS GLOBAL
# =========================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}

    .header {
        display: flex;
        align-items: center;
        background-color: #ECF0F1;
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .logo {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        margin-right: 20px;
        object-fit: cover;
    }
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #1ABC9C;
        margin: 0;
    }
    .subtitle {
        font-size: 14px;
        color: #2C3E50;
        margin: 0;
    }
    .menu {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
    }
    .menu a {
        background-color: white;
        color: #1ABC9C !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: none;
        border: 1px solid #1ABC9C;
    }
    .menu a:hover {
        background-color: #16A085;
        color: white !important;
        transform: scale(1.05);
    }
    .section {
        margin-top: 30px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Charger et convertir le logo en base64
# =========================
logo_path = os.path.join(os.path.dirname(__file__), "..", "Images", "AfricaEduVision.png")

def img_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = img_to_base64(logo_path)

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class="header">
    <img src="data:image/png;base64,{logo_base64}" class="logo">
    <div>
        <p class="main-title">AfricaEduVision</p>
        <p class="subtitle">Méthodologie du projet</p>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
st.markdown("""
<div class="menu">
    <a href="/"> Accueil</a>
    <a href="/EDA"> Analyse exploratoire</a>
    <a href="/Predictions"> Prévisions</a>
    <a href="/Comparaisons"> Comparaisons</a>
    <a href="/Methodologie"> Méthodologie</a>
    <a href="/Conclusion"> Conclusion</a>
</div>
""", unsafe_allow_html=True)

# =========================
# DATASET INFO
# =========================
st.title(" Méthodologie du projet")

data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Africa_Education_Development_Top30_ClusterImputed.csv")
df = pd.read_csv(os.path.abspath(data_path))

st.subheader(" Informations sur le dataset")
st.write(f"- Nombre de lignes : **{df.shape[0]}**")
st.write(f"- Nombre de colonnes : **{df.shape[1]}**")

# =========================
# DESCRIPTION DES VARIABLES
# =========================
st.subheader(" Description des variables")

variables = {
    "Country Name": "Nom du pays",
    "Country Code": "Code ISO du pays",
    "Year": "Année de l’observation",
    "Literacy_Female_Adult": "Taux d’alphabétisation des femmes adultes (≥15 ans)",
    "Literacy_Male_Adult": "Taux d’alphabétisation des hommes adultes (≥15 ans)",
    "Literacy_Female_Youth": "Taux d’alphabétisation des jeunes filles (15-24 ans)",
    "Literacy_Male_Youth": "Taux d’alphabétisation des jeunes garçons (15-24 ans)",
    "GDP_per_capita": "PIB par habitant (USD constant)",
    "Education_Expenditure": "Dépenses publiques en éducation (% du PIB)",
    "Urban_Population": "Part de la population urbaine (% de la population totale)",
    "Poverty": "Population vivant sous le seuil de pauvreté (% de la population)",
    "Child_Marriage_Under18": "Proportion de femmes mariées avant 18 ans (%)",
    "Child_Marriage_Under15": "Proportion de femmes mariées avant 15 ans (%)",
    "Net_Migration": "Solde migratoire (entrées – sorties)",
    "Fertility_Rate": "Taux de fécondité (nombre moyen d’enfants par femme)"
}

df_desc = pd.DataFrame(list(variables.items()), columns=["Variable", "Description"])
st.table(df_desc)

# =========================
# MÉTHODOLOGIE
# =========================
st.markdown("""
<div class="section">
<h3>1️ Collecte et préparation des données</h3>
<ul>
    <li>Données issues de la Banque mondiale et d'autres sources ouvertes.</li>
    <li>Nettoyage : suppression des pays avec >50% de valeurs manquantes.</li>
    <li>Imputation : interpolation linéaire et médiane par cluster de pays similaires.</li>
    <li>Sélection finale : 30 pays africains avec données exploitables (2000–2022).</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>2️ Analyse exploratoire (EDA)</h3>
<ul>
    <li>Visualisation des tendances par pays et par période.</li>
    <li>Étude des corrélations alphabétisation ↔ fécondité, mariages précoces, PIB.</li>
    <li>Comparaisons multi-pays : diagrammes en barres, radar chart, distributions, animations temporelles.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>3️ Modélisation prédictive en Python.</h3>
<ul>
    <li><b>Prophet</b> : prévisions sur séries temporelles.</li>
    <li><b>Random Forest</b> : apprentissage supervisé avec variables socio-économiques.</li>
    <li><b>LSTM</b> : réseau de neurones pour anticiper les tendances futures.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>4️ Visualisation interactive</h3>
<ul>
    <li>Développée avec <b>Streamlit</b> pour l’interactivité.</li>
    <li>Graphiques dynamiques créés avec <b>Plotly</b>.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>5️ Déploiement</h3>
<ul>
    <li>Architecture : Frontend (Streamlit) + Backend (FastAPI).</li>
    <li>Objectif : outil interactif pour chercheurs, étudiants et décideurs.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =========================
# LISTE DES PAYS
# =========================
st.subheader("  Liste des pays inclus dans l’étude")
pays = sorted(df["Country Name"].unique())
st.write(f"Nombre de pays : **{len(pays)}**")
df_pays = pd.DataFrame(pays, columns=["Pays inclus"])
st.table(df_pays)
