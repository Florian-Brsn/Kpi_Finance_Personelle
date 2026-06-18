from flask import Flask, render_template, request, jsonify, Response
import sqlite3
import csv
import io

app = Flask(__name__)
DB_FILE = 'portage_os.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Table des statistiques mensuelles globales
    c.execute('''CREATE TABLE IF NOT EXISTS monthly_stats (
                    month_year TEXT PRIMARY KEY,
                    ca REAL, culture REAL, pee REAL, super_net REAL, pouvoir_achat_total REAL
                )''')
    # Table du détail des dépenses et investissements
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month_year TEXT, category TEXT, name TEXT, amount REAL
                )''')
    conn.commit()
    conn.close()

# Initialisation de la BDD au démarrage
init_db()

@app.route('/')
def index():
    # Charge le fichier index.html situé dans le dossier templates
    return render_template('index.html')

@app.route('/api/save_month', methods=['POST'])
def save_month():
    data = request.json
    month_year = data['month_year']
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. Sauvegarde des métriques principales (écrase si le mois existe déjà)
    c.execute('''REPLACE INTO monthly_stats (month_year, ca, culture, pee, super_net, pouvoir_achat_total) 
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (month_year, data['ca'], data['culture'], data['pee'], data['super_net'], data['pouvoir_achat_total']))
    
    # 2. Nettoyage des anciennes dépenses pour ce mois, puis insertion des nouvelles
    c.execute('DELETE FROM expenses WHERE month_year = ?', (month_year,))
    for exp in data['expenses']:
        c.execute('INSERT INTO expenses (month_year, category, name, amount) VALUES (?, ?, ?, ?)',
                  (month_year, exp['category'], exp['name'], exp['amount']))
        
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"Mois {month_year} figé et sauvegardé dans la base !"})

@app.route('/api/get_history', methods=['GET'])
def get_history():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Requête pour agréger les données et les renvoyer au tableau de bord web
    c.execute('''
        SELECT m.month_year, m.ca, m.super_net, m.pouvoir_achat_total, m.pee, 
               COALESCE(SUM(CASE WHEN e.category='investissement' THEN e.amount ELSE 0 END), 0) as total_pea,
               COALESCE(SUM(CASE WHEN e.category='depense' THEN e.amount ELSE 0 END), 0) as total_depenses
        FROM monthly_stats m
        LEFT JOIN expenses e ON m.month_year = e.month_year
        GROUP BY m.month_year ORDER BY m.month_year DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

@app.route('/api/export', methods=['GET'])
def export_csv():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT m.month_year, m.ca, m.super_net, m.pouvoir_achat_total, m.pee, 
                        COALESCE(SUM(CASE WHEN e.category='investissement' THEN e.amount ELSE 0 END), 0) as total_pea,
                        COALESCE(SUM(CASE WHEN e.category='depense' THEN e.amount ELSE 0 END), 0) as total_depenses
                 FROM monthly_stats m
                 LEFT JOIN expenses e ON m.month_year = e.month_year
                 GROUP BY m.month_year ORDER BY m.month_year DESC''')
    rows = c.fetchall()
    conn.close()

    # Génération du fichier CSV à télécharger
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Mois', 'Revenus (CA/Brut)', 'Cash Super Net', 'Pouvoir Achat Total', 'Investi PEE', 'Investi PEA', 'Dépenses Courantes'])
    writer.writerows(rows)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=export_portage_os.csv"})

if __name__ == '__main__':
    # host='0.0.0.0' permet d'exposer l'application sur le réseau local
    app.run(debug=True, host='0.0.0.0')