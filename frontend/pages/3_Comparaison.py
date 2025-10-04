# ===============================================
# LIBRAIRIES
# ===============================================
import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import plotly.graph_objects as go

# ===============================================
# CONFIGURATION DE LA PAGE
# ===============================================
st.set_page_config(
    page_title="Comparaisons - AfricaEduVision",
    page_icon="🌍",
    layout="wide"
)

# ===============================================
# CSS GLOBAL
# ===============================================
st.markdown("""
    <style>
    /* Masquer la sidebar par défaut */
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}

    /* Header (logo + titre) */
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
    /* Menu */
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
    </style>
""", unsafe_allow_html=True)

# ===============================================
# LOGO EN BASE64
# ===============================================
logo_path = os.path.join(os.path.dirname(__file__), "..", "Images", "AfricaEduVision.png")

def img_to_base64(path):
    """Convertit l’image du logo en base64 pour l’intégrer dans le header."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = img_to_base64(logo_path)

# ===============================================
# HEADER + MENU
# ===============================================
st.markdown(f"""
<div class="header">
    <img src="data:image/png;base64,{logo_base64}" class="logo">
    <div>
        <p class="main-title">AfricaEduVision</p>
        <p class="subtitle">Comparaisons multi-pays</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="menu">
    <a href="/"> Accueil</a>
    <a href="/EDA"> Analyse exploratoire</a>
    <a href="/Predictions"> Prévisions</a>
    <a href="/Comparaisons"> Comparaisons</a>
    <a href="/Methodologie"> Méthodologie</a>
</div>
""", unsafe_allow_html=True)

# ===============================================
# CHARGEMENT DU DATASET
# ===============================================
data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Africa_Education_Development_Top30_ClusterImputed.csv")
df = pd.read_csv(os.path.abspath(data_path))

# ===============================================
# INDICATEURS DISPONIBLES
# ===============================================
indicateurs = {
    "Alphabétisation femmes adultes": "Literacy_Female_Adult",
    "Alphabétisation hommes adultes": "Literacy_Male_Adult",
    "Alphabétisation jeunes filles (15-24)": "Literacy_Female_Youth",
    "Alphabétisation jeunes garçons (15-24)": "Literacy_Male_Youth",
    "Fécondité (enfants/femme)": "Fertility_Rate",
    "Mariages précoces (<18 ans)": "Child_Marriage_Under18",
    "PIB par habitant": "GDP_per_capita"
}

st.title(" Comparaisons multi-pays")

# ===============================================
# 1️ DIAGRAMME EN BARRES (CLASSEMENT PAYS)
# ===============================================
st.subheader(" Classement des pays par indicateur")

# Sélecteurs pour année + indicateur
annee_bar = st.selectbox("Choisissez une année :", sorted(df["Year"].unique()))
indic_bar = st.selectbox("Choisissez un indicateur :", list(indicateurs.keys()))

# Filtrer et trier les données
colonne_bar = indicateurs[indic_bar]
df_bar = df[df["Year"] == annee_bar].sort_values(by=colonne_bar, ascending=False)

# Bar chart
fig_bar = px.bar(
    df_bar,
    x="Country Name",
    y=colonne_bar,
    title=f"{indic_bar} en {annee_bar} (Top 30 pays)",
    labels={"Country Name": "Pays", colonne_bar: indic_bar}
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===============================================
# 2️ BOXPLOT (DISTRIBUTION)
# ===============================================
st.subheader(" Distribution par indicateur")

annee_box = st.selectbox("Année pour le boxplot :", sorted(df["Year"].unique()), key="box")
indic_box = st.selectbox("Indicateur :", list(indicateurs.keys()), key="box2")

col_box = indicateurs[indic_box]
df_box = df[df["Year"] == annee_box]

fig_box = px.box(
    df_box,
    x="Country Name",
    y=col_box,
    title=f"Distribution de {indic_box} par pays ({annee_box})",
    labels={"Country Name": "Pays", col_box: indic_box}
)
st.plotly_chart(fig_box, use_container_width=True)

# ===============================================
# 3️ ANIMATION TEMPORELLE (STYLE GAPMINDER)
# ===============================================
st.subheader(" Animation temporelle (style Gapminder)")

x_indic = st.selectbox("Axe X :", list(indicateurs.keys()), key="animx")
y_indic = st.selectbox("Axe Y :", list(indicateurs.keys()), key="animy")

fig_anim = px.scatter(
    df,
    x=indicateurs[x_indic],
    y=indicateurs[y_indic],
    animation_frame="Year",            # animation par année
    animation_group="Country Name",    # chaque pays = une trajectoire
    size="GDP_per_capita",             # taille des bulles
    color="Country Name",              # couleur par pays
    hover_name="Country Name",         # affichage au survol
    log_x=False,
    size_max=60,
    labels={indicateurs[x_indic]: x_indic, indicateurs[y_indic]: y_indic}
)
fig_anim.update_layout(title=f"Évolution temporelle : {y_indic} vs {x_indic}")
st.plotly_chart(fig_anim, use_container_width=True)
