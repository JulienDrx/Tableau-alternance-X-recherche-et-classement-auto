import sqlite3

def creer_table_si_absente(db_path):
    """
    Crée la table 'alternance' dans la base de données si elle n'existe pas déjà.
    """
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS alternance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise TEXT,
            url TEXT,
            sauvegarde_locale TEXT,
            date_candidature TEXT,
            retour_oui_ou_non TEXT,
            date_de_retour TEXT,
            commentaire TEXT
        )
    ''')
    con.commit()
    con.close()
