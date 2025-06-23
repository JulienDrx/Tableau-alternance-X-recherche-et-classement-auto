from flask import Blueprint, request, render_template, jsonify, send_file, redirect, current_app, flash, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog
from creer_bdd import creer_table_si_absente

gestion_bp = Blueprint("gestion", __name__)

# Dossier d'upload



# Config fichier et chemin BDD
CONFIG_FILE = Path("db_config.txt")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def demande_chemin_bdd():
    root = tk.Tk()
    root.withdraw()
    fichier = filedialog.asksaveasfilename(
        title="Où souhaitez-vous enregistrer la base de données ?",
        defaultextension=".db",
        filetypes=[("Base SQL", "*.db")],
        initialfile="BDD_alternance.db"
    )
    return Path(fichier) if fichier else None

# Lecture/initialisation du chemin vers la base de données
if CONFIG_FILE.exists():
    chemin_str = CONFIG_FILE.read_text(encoding="utf-8").strip()
    db_path = Path(chemin_str)
    if not db_path.exists():
        print(f"Base de données introuvable : {db_path}")
        db_path = None
else:
    db_path = None

if not db_path:
    chemin = demande_chemin_bdd()
    if not chemin:
        print("Aucun fichier sélectionné. Fermeture.")
        exit()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(str(chemin), encoding="utf-8")
    db_path = chemin
creer_table_si_absente(db_path)




    
    
@gestion_bp.route("/tableau", methods=["GET", "POST"])
def tableau():
    if request.method == "POST":
        entreprise = request.form['entreprise']
        url = request.form['url']
        nom_fichier = request.form['nom_fichier']
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']

        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        cur.execute('''INSERT INTO alternance (
            entreprise, url, sauvegarde_locale, date_candidature,
            retour_oui_ou_non, date_de_retour, commentaire)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (entreprise, url, nom_fichier, date_candidature,
             retour_oui_ou_non, date_de_retour, commentaire))
        con.commit()
        con.close()
        return redirect("/tableau")

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("SELECT * FROM alternance")
    tableau = cur.fetchall()
    con.close()
    return render_template("tableau.html", tableau=tableau)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@gestion_bp.route("/upload_cv", methods=["POST"])
def upload_cv():
    if "file" not in request.files:
        flash("Aucun fichier reçu", "error")
        return redirect(url_for("gestion.tableau"))

    file = request.files["file"]
    if file.filename == "":
        flash("Nom de fichier vide", "error")
        return redirect(url_for("gestion.tableau"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        flash(f"Fichier '{filename}' bien reçu ✅", "success")
        return redirect(url_for("gestion.tableau"))

    flash("Type de fichier non autorisé", "error")
    return redirect(url_for("gestion.tableau"))




@gestion_bp.route("/get_cv/<filename>")
def get_cv(filename):
    upload_path = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(upload_path, filename)
    if os.path.exists(path):
        return send_file(path)
    return jsonify({"erreur": "Fichier introuvable"}), 404


@gestion_bp.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()

    if request.method == 'POST':
        # On récupère les nouvelles données depuis le formulaire
        entreprise = request.form['entreprise']
        url = request.form['url']
        nom_fichier = request.form['nom_fichier']
        date_candidature = request.form['date_candidature']
        retour_oui_ou_non = request.form['retour_oui_ou_non']
        date_de_retour = request.form['date_de_retour']
        commentaire = request.form['commentaire']

        cur.execute('''
            UPDATE alternance SET 
                entreprise=?, url=?, sauvegarde_locale=?, 
                date_candidature=?, retour_oui_ou_non=?, 
                date_de_retour=?, commentaire=?
            WHERE id=?
        ''', (
            entreprise, url, nom_fichier, date_candidature,
            retour_oui_ou_non, date_de_retour, commentaire, id
        ))

        con.commit()
        con.close()
        return redirect('/tableau')

    # Sinon : méthode GET → afficher les données existantes
    cur.execute("SELECT * FROM alternance WHERE id=?", (id,))
    ligne = cur.fetchone()
    con.close()

    if ligne:
        return render_template("modifier.html", ligne=ligne)
    else:
        return "Candidature introuvable", 404

@gestion_bp.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute("DELETE FROM alternance WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect('/tableau')


@gestion_bp.route("/liste_cv")
def liste_cv():
    dossier = current_app.config["UPLOAD_FOLDER"]
    fichiers = os.listdir(dossier)
    return render_template("liste_cv.html", fichiers=fichiers)
