import requests
from bs4 import BeautifulSoup

def extraire_texte_depuis_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        texte = soup.get_text(separator=' ', strip=True)
        return texte[:5000]  # Limiter la taille pour Mistral
    except Exception as e:
        print(f"[SCRAPING ERREUR] {url} → {e}")
        return ""
