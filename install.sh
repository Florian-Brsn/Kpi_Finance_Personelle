#!/bin/bash
echo "🚀 Démarrage de l'installation de PortageOS..."

# 1. Mise à jour et dépendances (sans sudo car on est déjà root)
apt update
apt install -y python3 python3-venv python3-pip sqlite3 git

# 2. Création de l'environnement virtuel
APP_DIR=$(pwd)
python3 -m venv venv
source venv/bin/activate

# 3. Installation des paquets Python
pip install -r requirements.txt

# 4. Configuration du service systemd (Démarrage automatique)
echo "⚙️ Configuration du lancement automatique (systemd)..."
SERVICE_FILE="/etc/systemd/system/portageos.service"

cat > $SERVICE_FILE <<EOF
[Unit]
Description=PortageOS - Dashboard Financier
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/flask run --host=0.0.0.0 --port=5000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 5. Activation et lancement du service
systemctl daemon-reload
systemctl enable portageos.service
systemctl restart portageos.service

echo "✅ Installation terminée avec succès !"
echo "👉 Ton application tourne en arrière-plan de manière autonome."
echo "🌐 Accède-y via l'IP de ton LXC sur le port 5000 (ex: http://IP_LXC:5000)"