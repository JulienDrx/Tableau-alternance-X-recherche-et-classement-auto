from flask import Blueprint, request, jsonify, render_template
import os
import requests
import re
from dotenv import load_dotenv
from docx import Document
import fitz
from io import BytesIO
from urllib.parse import quote
from bs4 import BeautifulSoup
from .scraping import extraire_texte_depuis_url

load_dotenv()

recherche_bp = Blueprint("recherche", __name__)

api_key = os.getenv("api_key")
search_engine_id = os.getenv("search_engine_id")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

liste_exclue = [
    "https://www.epitech.eu/",
    "https://lille.cesi.fr/",
    "https://2iacademy.com/",
    "https://www.cesi.fr/"
]

@recherche_bp.route("/")
def index():
    uploads_path = os.path.join(os.path.dirname(__file__), "..", "uploads")
    uploads_path = os.path.abspath(uploads_path)
    fichiers_cv = os.listdir(uploads_path)
    return render_template("index.html", fichiers_cv=fichiers_cv)

def google_search(search_query, api_key, search_engine_id, exclude_sites=None, start=1, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"

    exclude_sites_query = ""
    if exclude_sites:
        exclude_sites_query = " -site:".join(exclude_sites)
        search_query += f" -site:{exclude_sites_query}"

    job_boards = ["site:indeed.fr", "site:monster.fr", "site:welcometothejungle.com"]
    job_boards_query = " OR ".join(job_boards)
    search_query = f"{search_query} ({job_boards_query})"
    search_query += "+Lille"

    params = {
        'q': search_query,
        'key': api_key,
        'cx': search_engine_id,
        'start': start,
        **kwargs
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la requête : {response.status_code}")
        return None

def extraire_texte_depuis_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        texte = soup.get_text(separator=' ', strip=True)
        return texte[:5000]  # on coupe à 5000 caractères max
    except Exception as e:
        print(f"Erreur scraping {url} : {e}")
        return ""




@recherche_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    all_results = []
    start = 1
    num = 10

    while True:
        results = google_search(
            query,
            api_key,
            search_engine_id,
            exclude_sites=liste_exclue,
            num=num,
            start=start,
            lr="lang_fr",
            dateRestrict="m1"
        )

        if not results or 'items' not in results:
            break

        search_results = results.get('items', [])
        if not search_results:
            break

        all_results.extend(search_results)
        start += num
        if len(search_results) < num:
            break

    if all_results:
        formatted_results = []
        for item in all_results:
            formatted_results.append({
                "title": item['title'],
                "link": item['link'],
                "description": item['snippet']
            })
        return jsonify(formatted_results)
    else:
        return jsonify({"error": "No results found"}), 404


@recherche_bp.route("/score_offre", methods=["POST"])
def score_offre():
    data = request.json
    link = data.get("link", "")
    cv_name = data.get("cv", "")

    if not link or not cv_name:
        return jsonify({"error": "Données manquantes"}), 400

    description = extraire_texte_depuis_url(link)
    if not description:
        return jsonify({"error": "Impossible de lire la page de l'offre"}), 400

    cv_url = f"http://localhost:5000/get_cv/{quote(cv_name)}"
    profil_utilisateur = fetch_cv_text(cv_url)

    if not profil_utilisateur:
        return jsonify({"error": "CV introuvable ou vide"}), 400

    score = scorer_offre(description, profil_utilisateur, mistral_api_key)
    return jsonify({"score": score})

def fetch_cv_text(cv_url):
    response = requests.get(cv_url)
    if response.status_code != 200:
        print("Erreur lors du téléchargement du CV")
        return ""

    if cv_url.endswith(".docx"):
        doc = Document(BytesIO(response.content))
        return "\n".join([p.text for p in doc.paragraphs])

    elif cv_url.endswith(".pdf"):
        text = ""
        doc = fitz.open(stream=response.content, filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text
    return ""

def scorer_offre(description, profil, api_key):
    prompt = f"Voici une offre : {description}\nCe profil : {profil}\nNote sur 10 ?"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        output = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"(\d+(?:[.,]\d*)?)", output)
        return float(match.group(1).replace(',', '.')) if match else 0.0
    else:
        print("Erreur Mistral:", response.text)
        return 0.0
