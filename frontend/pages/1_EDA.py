# ===============================================
# LIBRAIRIES
# ===============================================
import plotly.express as px       # Pour créer des graphiques interactifs
import streamlit as st            # Pour construire l’application web
import pandas as pd               # Pour gérer et manipuler le dataset
import os                         # Pour gérer les chemins de fichiers
import base64                     # Pour convertir le logo en base64 (affichage dans header HTML)

# ===============================================
# CONFIGURATION DE LA PAGE
# ===============================================
st.set_page_config(
    page_title="Analyse exploratoire - AfricaEduVision", # Titre de l’onglet du navigateur
    page_icon="🌍",                                      # Icône (globe)
    layout="wide"                                        # Mise en page large
)

# ===============================================
# CSS GLOBAL
# ===============================================
st.markdown("""
    <style>
    /* Masquer la sidebar native de Streamlit */
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}

    /* HEADER : logo + titre */
    .header {
        display: flex;                  
        align-items: center;            
        background-color: #ECF0F1;      
        padding: 15px 25px;
        border-radius: 8px;             
        margin-bottom: 10px;
    }
    .logo {
        width: 65px; height: 65px;      
        border-radius: 50%;             
        margin-right: 20px;
        object-fit: cover;
    }
    .title-block {                      
        display: flex;
        flex-direction: column;
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

    /* MENU de navigation */
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
        transition: 0.3s;
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
# LOGO (en base64 pour affichage dans HTML)
# ===============================================
logo_path = os.path.join(os.path.dirname(__file__), "..", "Images", "AfricaEduVision.png")

def img_to_base64(path):
    """Convertit le logo en base64 pour l’afficher dans le header."""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = img_to_base64(logo_path)

# ===============================================
# HEADER AVEC LOGO + TITRE
# ===============================================
st.markdown(f"""
<div class="header">
    <img src="data:image/png;base64,{logo_base64}" class="logo">
    <div class="title-block">
        <p class="main-title">AfricaEduVision</p>
        <p class="subtitle">Alphabétisation et développement en Afrique</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================================
# MENU DE NAVIGATION
# ===============================================
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

# Affichage du titre et d’un aperçu du dataset
st.title("Analyse exploratoire")
st.write("Voici un aperçu du dataset utilisé pour l'analyse :")
st.dataframe(df.head(20))

# ===============================================
# FILTRES INTERACTIFS (Pays + Période)
# ===============================================
pays = st.selectbox("Choisissez un pays :", sorted(df["Country Name"].unique()))

annees = st.slider("Choisissez la plage d'années :", 
                   int(df["Year"].min()), 
                   int(df["Year"].max()), 
                   (2006, 2022))

# Application du filtre
df_filtre = df[(df["Country Name"] == pays) & 
               (df["Year"] >= annees[0]) & 
               (df["Year"] <= annees[1])]

st.write(f"### Données filtrées pour {pays} ({annees[0]}–{annees[1]})")
st.dataframe(df_filtre)

# ===============================================
# INDICATEURS DISPONIBLES
# ===============================================
indicateurs_disponibles = {
    "Alphabétisation femmes adultes" : "Literacy_Female_Adult",
    "Alphabétisation hommes adultes" : "Literacy_Male_Adult",
    "Alphabétisation jeunes filles (15-24)" : "Literacy_Female_Youth",
    "Alphabétisation jeunes garçons (15-24)" : "Literacy_Male_Youth",
    "Fécondité (enfants/femme)" : "Fertility_Rate",
    "Mariages précoces (<18 ans)" : "Child_Marriage_Under18",
    "PIB par habitant" : "GDP_per_capita"
}

# Multiselect : utilisateur choisit les indicateurs
choix = st.multiselect(
    "Choisissez les indicateurs à visualiser :", 
    options=list(indicateurs_disponibles.keys()), 
    default=["Alphabétisation femmes adultes", "Alphabétisation hommes adultes"]
)
colonnes_selectionnees = [indicateurs_disponibles[c] for c in choix]

# ===============================================
# TYPE DE GRAPHIQUE
# ===============================================
graph_type = st.radio(
    "Choisissez le type de graphique :", 
    ["Courbes", "Barres", "Nuage de points"], 
    horizontal=True
)

# Génération du graphique
if colonnes_selectionnees:
    if graph_type == "Courbes":
        fig = px.line(df_filtre, x="Year", y=colonnes_selectionnees,
                      labels={"value": "Valeur", "Year": "Année"},
                      title=f"Évolution des indicateurs choisis ({pays})")
    elif graph_type == "Barres":
        fig = px.bar(df_filtre, x="Year", y=colonnes_selectionnees,
                     barmode="group", labels={"value": "Valeur", "Year": "Année"},
                     title=f"Comparaison par barres ({pays})")
    else:
        fig = px.scatter(df_filtre, x="Year", y=colonnes_selectionnees,
                         labels={"value": "Valeur", "Year": "Année"},
                         title=f"Nuage de points des indicateurs ({pays})")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Veuillez sélectionner au moins un indicateur.")

# ===============================================
# RELATION : Alphabétisation femmes VS autres facteurs
# ===============================================
st.markdown("---")
st.subheader(" Explorer les relations entre alphabétisation et autres facteurs")

facteurs = {
    "Fécondité (enfants/femme)" : "Fertility_Rate",
    "Mariages précoces (<18 ans)" : "Child_Marriage_Under18",
    "PIB par habitant" : "GDP_per_capita"
}

facteur_choisi = st.selectbox(" Choisissez un facteur à comparer :", list(facteurs.keys()))
colonne_facteur = facteurs[facteur_choisi]

# Scatter + droite de tendance
fig_corr = px.scatter(df_filtre, x="Literacy_Female_Adult", y=colonne_facteur,
                      color="Year", trendline="ols", hover_name="Year",
                      labels={"Literacy_Female_Adult": "Alphabétisation femmes adultes (%)",
                              colonne_facteur: facteur_choisi,
                              "Year": "Année"},
                      title=f"Relation entre alphabétisation des femmes et {facteur_choisi} ({pays})")
st.plotly_chart(fig_corr, use_container_width=True)


# =========================
# HEATMAP DE CORRÉLATIONS
# =========================
st.markdown("---")
st.subheader(" Corrélations globales entre indicateurs")

colonnes_numeriques = df.select_dtypes(include=["float64", "int64"]).columns
df_corr = df[colonnes_numeriques].corr()

fig_corr_matrix = px.imshow(
    df_corr,
    text_auto=True,   # Affiche les coefficients dans la matrice
    color_continuous_scale="RdBu_r",
    title="Matrice de corrélation entre les indicateurs"
)

st.plotly_chart(fig_corr_matrix, use_container_width=True)

