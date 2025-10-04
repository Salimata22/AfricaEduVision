# =========================
# LIBRAIRIES
# =========================
import streamlit as st         # Framework pour créer l'application web interactive
import pandas as pd            # Pour manipuler les données tabulaires (CSV, DataFrame…)
import os                      # Pour gérer les chemins des fichiers (logo, images…)
import base64                  # Pour convertir une image en texte encodé (Base64), utile pour l'intégrer directement dans le HTML

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(
    page_title="AfricaEduVision",   # Titre de l'onglet du navigateur
    page_icon="🌍",                 # Icône de la page
    layout="wide",                  # Mise en page large (plein écran)
    initial_sidebar_state="collapsed" # Masquer la barre latérale par défaut
)

# Masquer le menu natif et le footer de Streamlit pour avoir une interface plus propre
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# =========================
# CSS GLOBAL
# =========================
st.markdown("""
    <style>
    /* HEADER (barre du haut contenant le logo et le titre) */
    .header {
        display: flex;                /* Alignement horizontal */
        align-items: center;          /* Centrer verticalement */
        background-color: #ECF0F1;    /* Couleur de fond gris clair */
        padding: 15px 25px;           /* Espacement interne */
        border-radius: 8px;           /* Coins arrondis */
        margin-bottom: 10px;          /* Espacement bas */
    }
    .logo {
        width: 65px; height: 65px;    /* Taille fixe du logo */
        border-radius: 50%;           /* Cercle */
        margin-right: 15px;           /* Espace entre logo et titre */
        object-fit: cover;            /* Bien centrer l'image */
    }
    .title-block {
        display: flex;
        flex-direction: column;       /* Titre et sous-titre l'un au-dessus de l'autre */
        justify-content: center;
    }
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #1ABC9C;               /* Vert clair */
        margin: 0;
    }
    .subtitle {
        font-size: 14px;
        color: #2C3E50;               /* Gris foncé */
        margin: 0;
    }

    /* MENU (barre de navigation) */
    .menu {
        display: flex;
        justify-content: center;      /* Centrer les liens au milieu */
        gap: 15px;                    /* Espacement entre les boutons */
        margin-top: 10px;
    }
    .menu a {
        background-color: white;
        color: #1ABC9C !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: none;        /* Pas de soulignement */
        transition: 0.3s;             /* Animation douce */
        border: 1px solid #1ABC9C;
    }
    .menu a:hover {
        background-color: #16A085;    /* Change de couleur au survol */
        color: white !important;
        transform: scale(1.05);       /* Zoom léger */
    }

    /* CHIFFRES CLÉS (section statistiques en bas de page) */
    .metrics {
        display: flex;
        justify-content: space-around; /* Espacement égal entre chaque bloc */
        margin-top: 40px;
        padding: 20px;
        background-color: #ECF0F1;     /* Même couleur que le header */
        border-radius: 10px;
    }
    .metric {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .metric-value {
        font-size: 26px;
        color: #1F618D;                /* Bleu pour attirer l'œil */
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)


# =========================
# LOGO (conversion en base64 pour être intégré en HTML)
# =========================
logo_path = os.path.join(os.path.dirname(__file__), "Images", "AfricaEduVision.png")

def img_to_base64(path):
    """Convertit une image en base64 pour l'afficher dans le HTML."""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = img_to_base64(logo_path)


# =========================
# HEADER (logo + titre)
# =========================
st.markdown(f"""
<div class="header">
    <img src="data:image/png;base64,{logo_base64}" class="logo">
    <div class="title-block">
        <p class="main-title">AfricaEduVision</p>
        <p class="subtitle">Alphabétisation et développement en Afrique</p>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# MENU
# =========================
st.markdown("""
<div class="menu">
    <a href="/">Accueil</a>
    <a href="/EDA">Analyse exploratoire</a>
    <a href="/Predictions">Prévisions</a>
    <a href="/Comparaison">Comparaisons</a>
    <a href="/Methodologie">Méthodologie</a>
</div>
""", unsafe_allow_html=True)


# =========================
# CONTENU PRINCIPAL
# =========================
col1, col2 = st.columns([2, 1])  # Division de la page en deux colonnes

with col1:
    # Texte de présentation (liste des fonctionnalités du site)
    st.markdown("""
    <div style="margin-top:30px;">
        <h4> Ce que vous pouvez faire ici :</h4>
        <ul>
            <li>Visualiser l’évolution de l’alphabétisation filles vs garçons (2006–2022).</li>
            <li>Explorer les liens entre éducation, fécondité, mariages précoces et PIB.</li>
            <li>Obtenir des prévisions à 5–10 ans grâce au Machine Learning.</li>
            <li>Comparer les trajectoires de différents pays africains.</li>
            <li>Analyser l’impact des politiques publiques sur l’éducation et la société.</li>
            <li>Découvrir des scénarios prospectifs pour imaginer l’avenir de l’Afrique.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Image de présentation (femme)
    femme_path = os.path.join(os.path.dirname(__file__), "Images", "FemmePresentation.png")
    if os.path.exists(femme_path):
        st.image(femme_path, caption="", use_container_width=False, output_format="PNG")

        # Forcer l'image en cercle avec CSS
        st.markdown("""
        <style>
        [data-testid="stImage"] img {
            border-radius: 50% !important;
            object-fit: cover;
        }
        </style>
        """, unsafe_allow_html=True)


# =========================
# CHIFFRES CLÉS
# =========================
# Charger le dataset et calculer les moyennes générales
data_path = os.path.join("data", "Africa_Education_Development_Top30_ClusterImputed.csv")
df = pd.read_csv(data_path)

mean_female = df["Literacy_Female_Adult"].mean()   # Moyenne alphabétisation femmes adultes
mean_male = df["Literacy_Male_Adult"].mean()       # Moyenne alphabétisation hommes adultes
mean_fertility = df["Fertility_Rate"].mean()       # Moyenne du taux de fécondité

# Bloc affichant les 3 chiffres clés
st.markdown(f"""
<div class="metrics">
    <div class="metric">
        Alphabétisation Femmes<br>
        <div class="metric-value">{mean_female:.1f} %</div>
    </div>
    <div class="metric">
        Alphabétisation Hommes<br>
        <div class="metric-value">{mean_male:.1f} %</div>
    </div>
    <div class="metric">
        Fécondité moyenne<br>
        <div class="metric-value">{mean_fertility:.2f} enfants/femme</div>
    </div>
</div>
""", unsafe_allow_html=True)
