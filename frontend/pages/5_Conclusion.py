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

# ===============================================
# LOGO EN BASE64
# ===============================================
logo_path = os.path.join(os.path.dirname(__file__), "..", "Images", "AfricaEduVision.png")

def img_to_base64(path):
    """Convertit le logo en base64 pour l’afficher dans le header."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = img_to_base64(logo_path)

# ===============================================
# HEADER AVEC LOGO + TITRE
# ===============================================
st.markdown(f"""
<div class="header">
    <img src="data:image/png;base64,{logo_base64}" class="logo">
    <div>
        <p class="main-title">AfricaEduVision</p>
        <p class="subtitle">Prévisions alphabétisation et développement</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================================
# MENU
# ===============================================
st.markdown("""
<div class="menu">
    <a href="/"> Accueil</a>
    <a href="/EDA"> Analyse exploratoire</a>
    <a href="/Predictions"> Prévisions</a>
    <a href="/Comparaison"> Comparaisons</a>
    <a href="/Methodologie"> Méthodologie</a>
    <a href="/Conclusion"> Conclusion</a>
</div>
""", unsafe_allow_html=True)


# =========================
# CONTENU DE LA CONCLUSION
# =========================
st.title("Conclusion et Réflexions personnelles")

st.markdown("""
### 1. Alphabétisation homme-femme  
Les données ont confirmé mes doutes.  
Il y a plus de femmes que d’hommes dans le monde et dans les pays, pourtant, de 2006 à 2022, le taux d’alphabétisation des femmes est resté inférieur à celui des hommes, même si les deux sont corrélés.

---

### 2. Alphabétisation et richesse des pays  
Lorsque le taux d’alphabétisation est bas, le PIB l’est aussi, sauf pour quelques exceptions.  
Est-ce parce que ces pays manquent d’argent pour investir dans l’éducation ?  
Ou est-ce parce qu’ils négligent l’éducation qu’ils restent pauvres ?  
Ces hypothèses méritent d’être vérifiées avec plus de données.

---

### 3. Mariages précoces et éducation des filles  
La relation entre mariage précoce et alphabétisation des femmes est frappante.  
En 2020, certains pays d’Afrique comptaient plus d’enfants mariés que scolarisés.  
Les pays avec les taux les plus bas d’alphabétisation féminine sont aussi ceux avec les taux les plus élevés de mariages précoces.  
Pourquoi une telle négligence au niveau des États ? Ont-ils vraiment pris la mesure du problème ?

---

### 4. Inégalités entre pays et zones  
Sur le même continent, certains pays dépassent 90 % d’alphabétisation, alors que d’autres restent sous 20 %.  
Comment expliquer de tels écarts ?  
Est-ce un manque de solidarité entre pays africains ?  
Ou bien l’éducation est-elle plus accessible en zone urbaine qu’en zone rurale ?  
Si oui, pourquoi néglige-t-on encore l’éducation en zone rurale ?

---

### 5. Mon avis personnel  
L’éducation doit être considérée comme une richesse aussi importante que l’agriculture ou les ressources naturelles.  
Toutes les femmes méritent une éducation, et le mariage précoce reste un frein majeur à l’épanouissement.  
Il faut imaginer un système où tous les pays d’Afrique – développés, en développement ou en retard – garantissent une éducation pour tous : jeunes, adultes, femmes et hommes, en zone rurale comme en ville.  
Et surtout, faire en sorte que le mot *mariage* n’entre dans le vocabulaire d’une jeune fille qu’après ses 18 ans.
""")

st.success("Cette conclusion exprime une réflexion personnelle basée sur les données, tout en soulevant des questions essentielles pour l’avenir de l’éducation en Afrique.")