# AfricaEduVision
Application de data science pour visualiser et prévoir l’évolution de l’alphabétisation et du développement socio-économique en Afrique.
Elle permet d’analyser, de comparer et de prédire l’évolution de l’alphabétisation et des facteurs socio-économiques dans 30 pays africains.


##  Objectifs du projet

- Visualiser l’évolution de l’alphabétisation filles vs garçons (2006–2022).
- Explorer les liens entre éducation, fécondité, mariages précoces et PIB.
- Obtenir des prévisions à 5–10 ans avec des modèles de Machine Learning et Deep Learning.
- Comparer les trajectoires de différents pays africains.
- Analyser l’impact des politiques publiques sur l’éducation et la société.

---

##  Fonctionnalités principales

1. **Accueil** : Présentation générale et chiffres clés (alphabétisation et fécondité).
2. **Analyse exploratoire (EDA)** :
   - Exploration par pays et période.
   - Graphiques interactifs (courbes, barres, nuages de points).
   - Relations entre alphabétisation et facteurs socio-économiques.
   - Heatmap des corrélations.
   - Distribution des indicateurs.
3. **Prévisions** :
   - Modèle Prophet (séries temporelles).
   - Random Forest (Machine Learning supervisé).
   - LSTM (Deep Learning).
4. **Comparaisons** :
   - Classement des pays par indicateur.
   - Boxplots par pays.
   - Animation temporelle (style Gapminder).
5. **Méthodologie** :
   - Description du dataset.
   - Nettoyage et préparation des données.
   - Explication des variables.

---

##  Technologies utilisées

- **Python 3.13**
- **Streamlit** pour l’interface web interactive
- **Pandas / NumPy** pour la manipulation des données
- **Plotly Express & Graph Objects** pour les visualisations
- **Prophet** pour la prévision des séries temporelles
- **Scikit-learn** pour le Machine Learning (Random Forest)
- **TensorFlow / Keras** pour le Deep Learning (LSTM)

---

## Structure du projet

AfricaEduML/
│── frontend/
│ ├── Home.py # Page d’accueil
│ ├── pages/
│ │ ├── 1_EDA.py # Analyse exploratoire
│ │ ├── 2_Predictions.py # Prévisions
│ │ ├── 3_Comparaison.py # Comparaisons
│ │ └── 4_Methodologie.py # Méthodologie
│ ├── Images/ # Logos et visuels
│── data/
│ └── Africa_Education_Development_Top30_ClusterImputed.csv
│── Rapport_AfricaEduVision.docx
│── README.md

---

##  Installation et exécution

### 1. Cloner le projet sur bash

git clone https://github.com/toncompte/AfricaEduVision.git
cd AfricaEduVision/frontend

### 2. Créer un environnement virtuel

python -m venv .venv
source .venv/bin/activate # Linux / Mac
.venv\Scripts\activate # Windows

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Lancer l’application

streamlit run Home.py

## Résultats attendus

Une plateforme interactive pour comprendre les liens entre éducation et développement en Afrique.

Des visualisations claires et dynamiques.

Des prévisions fiables sur l’évolution de l’alphabétisation.

## Auteurs

Salimata TOGO.

