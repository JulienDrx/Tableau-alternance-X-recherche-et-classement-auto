
# 🧠 Tableau alternance X recherche et classement auto

Ce projet est une application web en Flask qui combine :
- 📊 un **tableau de suivi des candidatures**
- 🔍 une **recherche automatique d'offres d'alternance** via l'API Google Custom Search
- 🤖 un **scoring intelligent** des offres grâce à l'API **Mistral AI**
- 📂 une **gestion des CV** avec envoi, stockage et utilisation dans l'analyse

## 🚀 Fonctionnalités principales

- Ajouter / modifier / supprimer des candidatures via un tableau clair
- Rechercher automatiquement des offres en ligne
- Envoyer son CV (PDF ou DOCX) et l'utiliser pour scorer chaque offre
- Obtenir un score personnalisé par l'IA Mistral en fonction de votre profil
- Visualiser et télécharger les CV enregistrés

## 🔧 Technologies utilisées

- Python 3.11+
- Flask (avec Blueprints)
- SQLite (base de données simple intégrée)
- HTML / CSS / JS Vanilla
- API Google Custom Search
- API Mistral (mistral-small / mistral-tiny)
- BeautifulSoup pour le scraping des annonces

## 📁 Structure du projet

```
.
├── app.py                  # Point d'entrée principal
├── gestion/                # Module pour la gestion des candidatures et CV
├── recherche/              # Module pour la recherche d'offres + scoring
├── templates/              # Fichiers HTML (Jinja)
├── uploads/                # CV uploadés
└── creer_bdd.py            # Script de création initiale de la BDD
```

## ⚙️ Lancer l’application

1. Cloner le repo :
```bash
git clone https://github.com/JulienDrx/Tableau-alternance-X-recherche-et-classement-auto
cd Tableau-alternance-X-recherche-et-classement-auto
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l’app :
```bash
python app.py
```

4. Accéder à l’app :
```
http://localhost:5000
```

## 🔑 Clés API nécessaires

Créer un fichier `.env` contenant :

```
GOOGLE_API_KEY=...
GOOGLE_CX_ID=...
MISTRAL_API_KEY=...
```

## 📌 À venir (TODO)

- Pagination des résultats Google
- Gestion multi-CV dans l’analyse Mistral
- Déploiement sur Render / Railway

---

💡 Développé avec passion par [@JulienDrx](https://github.com/JulienDrx)
