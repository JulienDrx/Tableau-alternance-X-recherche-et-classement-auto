import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extraire_texte_depuis_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        href =a["href"]

        liens = []
        for a in soup.find_all("a", href=True):

            texte = soup.get_text(separator=' ', strip=True)
            return texte[:5000]  # Limiter la taille pour Mistral
    except Exception as e:
        print(f"[SCRAPING ERREUR] {url} → {e}")
        return ""


def extraire_liens_offres_depuis_page_liste(url_page):
    """
    Explore une page contenant plusieurs offres (ex: page LinkedIn) et retourne la liste des liens individuels d'offres.
    """
    try:
        response = requests.get(url_page, timeout=5)
        if response.status_code != 200:
            print(f"[Erreur HTTP] {url_page} → {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        liens_trouves = []

        # 🟢 CORRECTION ICI : le for est suivi d'un bloc indenté
        for a in soup.find_all("a", href=True):
            href = a["href"]
            lien_complet = urljoin(url_page, href)

            # 🔍 Filtrage par mots-clés
            if any(keyword in href for keyword in ["/offre", "/job", "/emploi", "offer", "jobs"]):
                if lien_complet not in liens_trouves:
                    liens_trouves.append(lien_complet)

        print(f"[✔] {len(liens_trouves)} offres trouvées sur {url_page}")
        return liens_trouves

    except Exception as e:
        print(f"[❌ scraping erreur] {url_page} → {e}")
        return []
