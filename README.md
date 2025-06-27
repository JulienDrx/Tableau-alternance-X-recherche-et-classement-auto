# 🧠 Candidature Assist

**Candidature Assist** est une application web Python conçue pour faciliter la recherche d'alternance, l'analyse automatique de la pertinence d’une offre avec un CV, et le suivi des candidatures via une interface simple et interactive.

---

## 🚀 Fonctionnalités principales

- 🔎 **Recherche automatisée** d’offres d’alternance par mots-clés
- 📄 **Upload sécurisé de CV**, utilisés comme contexte pour un scoring LLM
- 🤖 **Évaluation de compatibilité** entre une offre et le CV sélectionné grâce à l’API **Mistral**
- 📊 **Tableau de suivi des candidatures** (dates, entreprises, retours, commentaires…)
- 🛡️ **Sécurité avancée** : protection CSRF, filtrage des uploads, entêtes HTTP sécurisés

---

## 🛠️ Stack technique

- Python 3.11+
- Flask (avec Blueprints)
- Flask-WTF pour la gestion des formulaires sécurisés
- Flask-Talisman pour les headers CSP / sécurité HTTP
- Mistral API (via requêtes HTTP)
- SQLite (persistant)
- HTML/CSS, JavaScript (fetch, AJAX)

---

## 🔒 Sécurité

- ✅ Protection CSRF sur tous les formulaires (`Flask-WTF`)
- ✅ Restrictions sur les fichiers uploadés (PDF/DOC/DOCX, max 2 Mo)
- ✅ Sécurisation HTTP avec `Flask-Talisman` (CSP, nosniff, X-Frame, etc.)
- ✅ Variables d’environnement via `.env` (**jamais pushé**), modèle fourni dans `.env.exemple`


---

## 📁 Structure du projet

```
candidature-assist/
├── app.py                   # Point d’entrée Flask
├── recherche/               # Logique de recherche et API Mistral
├── gestion/                 # Upload de CV, tableau de suivi
├── templates/               # Pages HTML (Jinja2)
├── static/                  # CSS / JavaScript
├── uploads/                 # Fichiers utilisateur
├── .env.exemple             # Modèle de configuration (à copier)
├── requirements.txt         # Dépendances du projet
└── tests.py                 # Tests fonctionnels
```

---

## ⚙️ Installation locale (dev)

```bash
git clone https://github.com/JulienDrx/candidature-assist.git
cd candidature-assist

python -m venv venv
source venv/bin/activate         # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt

cp .env.exemple .env             # puis configure ta clé Mistral etc.
flask run
```

---

## 🧠 API Mistral

Le CV uploadé est injecté dans un prompt vers l’API **Mistral**, qui renvoie un score de compatibilité (sur 10) avec chaque offre détectée.  
Ce score est affiché avec une **explication générée automatiquement**.

---

## 📦 À venir

- Authentification utilisateur
- Export Excel / CSV
- Mode multi-CV + notation comparative
- Déploiement sur Render ou Railway

---

## 👤 Auteur

**Julien Drieux**  
🔗 [LinkedIn](https://www.linkedin.com/in/julien-drieux)

---

## 📜 Licence

Projet open-source sous licence Apache 2.0.
