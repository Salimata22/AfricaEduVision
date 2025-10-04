# ===============================================
# LIBRAIRIES
# ===============================================
import streamlit as st
import pandas as pd
import os
import base64
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Prophet : pour prévisions séries temporelles
from prophet import Prophet

# Machine Learning classique
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Deep Learning (réseaux de neurones récurrents)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# ===============================================
# CONFIGURATION DE LA PAGE
# ===============================================
st.set_page_config(
    page_title="Prévisions - AfricaEduVision",
    page_icon="🌍",
    layout="wide"
)

# ===============================================
# CSS GLOBAL + HEADER
# ===============================================
st.markdown("""
    <style>
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

# ===============================================
# CHARGEMENT DU DATASET
# ===============================================
data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Africa_Education_Development_Top30_ClusterImputed.csv")
df = pd.read_csv(os.path.abspath(data_path))

# ===============================================
# SELECTION UTILISATEUR
# ===============================================
# Pays choisi
pays = st.selectbox(" Choisissez un pays :", sorted(df["Country Name"].unique()))

# Type de modèle à utiliser
modele_type = st.radio(
    " Choisissez un modèle :",
    ["Prophet (Séries temporelles)", "Random Forest (Machine Learning)", "LSTM (Deep Learning)"]
)

# ===============================================
# MODELE 1 : PROPHET
# ===============================================
if modele_type == "Prophet (Séries temporelles)":
    st.subheader(" Prévision avec Prophet")

    # Filtrer données pour le pays choisi
    df_pays = df[df["Country Name"] == pays][["Year", "Literacy_Female_Adult"]].dropna()

    # Adapter au format Prophet (colonnes ds = date, y = valeur)
    df_prophet = df_pays.rename(columns={"Year": "ds", "Literacy_Female_Adult": "y"})
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")

    # Entraîner le modèle
    model = Prophet()
    model.fit(df_prophet)

    # Générer prévisions futures jusqu’en 2030
    future = model.make_future_dataframe(periods=8, freq="Y")
    forecast = model.predict(future)

    # Graphique
    fig = px.line(forecast, x="ds", y="yhat",
                  title=f"Prévision alphabétisation femmes adultes ({pays})")
    fig.add_scatter(x=df_prophet["ds"], y=df_prophet["y"], mode="markers", name="Historique")
    st.plotly_chart(fig, use_container_width=True)

# ===============================================
# MODELE 2 : RANDOM FOREST (ML)
# ===============================================
elif modele_type == "Random Forest (Machine Learning)":
    st.subheader(" Prévision avec Random Forest")

    # Variables explicatives (facteurs socio-éco)
    X = df[["GDP_per_capita", "Education_Expenditure", "Urban_Population",
            "Fertility_Rate", "Child_Marriage_Under18"]]
    y = df["Literacy_Female_Adult"]

    # Nettoyer les valeurs manquantes
    X = X.fillna(X.median())
    y = y.fillna(y.median())

    # Entraîner le modèle sur tout le dataset (global)
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X, y)

    # Récupérer données du pays choisi
    df_pays = df[df["Country Name"] == pays].copy()
    last_year = int(df_pays["Year"].max())

    # Créer données futures (scénarios simples d’évolution)
    future_years = list(range(last_year + 1, 2031))
    future_data = pd.DataFrame({
        "Year": future_years,
        "GDP_per_capita": df_pays["GDP_per_capita"].iloc[-1] * (1.05 ** np.arange(1, len(future_years)+1)),
        "Education_Expenditure": df_pays["Education_Expenditure"].iloc[-1] * (1.03 ** np.arange(1, len(future_years)+1)),
        "Urban_Population": df_pays["Urban_Population"].iloc[-1] * (1.02 ** np.arange(1, len(future_years)+1)),
        "Fertility_Rate": df_pays["Fertility_Rate"].iloc[-1] * (0.98 ** np.arange(1, len(future_years)+1)),
        "Child_Marriage_Under18": df_pays["Child_Marriage_Under18"].iloc[-1] * (0.99 ** np.arange(1, len(future_years)+1))
    })

    # Prédire sur ces données futures
    X_future = future_data.drop(columns=["Year"])
    y_future_pred = rf.predict(X_future)

    # Graphique Historique + Prévisions
    fig_rf = go.Figure()
    fig_rf.add_scatter(x=df_pays["Year"], y=df_pays["Literacy_Female_Adult"],
                       mode="lines+markers", name="Historique", line=dict(color="blue"))
    fig_rf.add_scatter(x=future_data["Year"], y=y_future_pred,
                       mode="lines+markers", name="Prévisions RF", line=dict(color="red", dash="dot"))
    fig_rf.update_layout(title=f"Prévisions alphabétisation femmes ({pays}) jusqu'en 2030",
                         xaxis_title="Année", yaxis_title="Taux d'alphabétisation (%)")
    st.plotly_chart(fig_rf, use_container_width=True)

# ===============================================
# MODELE 3 : LSTM (Deep Learning)
# ===============================================
elif modele_type == "LSTM (Deep Learning)":
    st.subheader(" Prévision avec LSTM")

    # Filtrer données pays
    df_pays = df[df["Country Name"] == pays][["Year", "Literacy_Female_Adult"]].dropna()

    if len(df_pays) < 10:
        st.warning("Pas assez de données pour entraîner un LSTM.")
    else:
        # Normalisation des valeurs
        data = df_pays["Literacy_Female_Adult"].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)

        # Création des séquences (fenêtre de 3 ans)
        X, y_seq = [], []
        for i in range(3, len(scaled_data)):
            X.append(scaled_data[i-3:i, 0])
            y_seq.append(scaled_data[i, 0])
        X, y_seq = np.array(X), np.array(y_seq)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Modèle LSTM
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(X, y_seq, epochs=50, batch_size=1, verbose=0)

        # Prévisions futures jusqu’en 2030
        last_sequence = scaled_data[-3:]
        predictions = []
        for _ in range(2030 - int(df_pays["Year"].max())):
            X_pred = np.reshape(last_sequence, (1, last_sequence.shape[0], 1))
            pred = model.predict(X_pred, verbose=0)
            predictions.append(pred[0, 0])
            last_sequence = np.vstack((last_sequence[1:], pred))

        # Inverser la normalisation
        y_future_pred = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

        # Années futures
        future_years = list(range(int(df_pays["Year"].max())+1, 2031))

        # Graphique
        fig_dl = go.Figure()
        fig_dl.add_scatter(x=df_pays["Year"], y=df_pays["Literacy_Female_Adult"],
                           mode="lines+markers", name="Historique", line=dict(color="blue"))
        fig_dl.add_scatter(x=future_years, y=y_future_pred.flatten(),
                           mode="lines+markers", name="Prévisions LSTM", line=dict(color="red", dash="dot"))
        fig_dl.update_layout(title=f"Prévisions alphabétisation femmes ({pays}) jusqu'en 2030",
                             xaxis_title="Année", yaxis_title="Taux d'alphabétisation (%)")
        st.plotly_chart(fig_dl, use_container_width=True)
