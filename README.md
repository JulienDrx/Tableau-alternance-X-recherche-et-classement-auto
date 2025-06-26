# 🔍 Tableau Alternance — Recherche & Scoring Automatique

Une application Flask pour rechercher des offres d'alternance, les analyser avec Mistral AI, importer des CV, et suivre vos candidatures dans un tableau interactif.

---

## 🚀 Fonctionnalités

- 🔎 Recherche d’offres d’alternance via **Google Custom Search API**
- 🧠 Analyse des offres avec **Mistral AI** (note /10 + explication)
- 📄 Import et sélection de **CV personnalisés** pour le scoring
- 📊 Suivi des candidatures dans un **tableau interactif**
- 🧹 Interface HTML avec **CSS personnalisée** et formulaire intuitif
- 🔗 Gestion des liens d’offres extraites depuis des pages listes (Indeed, WTTJ...)

---

## 📦 Technologies

- Python 3 + Flask
- HTML / CSS
- SQLite
- Google Custom Search API
- Mistral Chat API
- BeautifulSoup (scraping HTML)
- Requests

---

## 🧪 Configuration requise

- Python 3.10 ou supérieur
- Un fichier `.env` contenant vos clés :

```env
api_key=VOTRE_GOOGLE_API_KEY
search_engine_id=VOTRE_CSE_ID
MISTRAL_API_KEY=VOTRE_MISTRAL_KEY
FLASK_SECRET_KEY=cle-secrete
```

---

## ▶️ Lancer le projet

```bash
# (Optionnel) Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Flask
python app.py
```

---

## 🗂 Arborescence du projet

```
.
├── app.py
├── creer_bdd.py
├── .env
├── .gitignore
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── tableau.html
│   ├── modifier.html
│   └── liste_cv.html
├── static/
│   └── style.css
├── gestion/
│   └── routes.py
├── recherche/
│   ├── routes.py
│   └── scraping.py
```

---

## 📝 Améliorations possibles

- Tri des offres par score Mistral
- Intégration Bootstrap ou Tailwind pour un style pro
- Historique des analyses ou versionnage des candidatures
- Export CSV des candidatures

---

## 🤝 Contribuer

N'hésitez pas à forker ce projet, proposer une pull request ou poser une question !

---

## 📜 Licence

Projet personnel à visée pédagogique.
