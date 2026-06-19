📊 Kpi_Finance_Personnelle_V1

Adieu le vieux fichier Excel austère !
Kpi_Finance_Personnelle_V1 est votre Directeur Financier (CFO) personnnel, conçu pour tourner localement sur votre serveur (LXC Proxmox, NAS...).

Que vous soyez en Portage Salarial ou Salarié classique (CDI/CDD), la plupart des simulateurs s'arrêtent au "Salaire Net". Cette application web auto-hébergée va plus loin : elle fait le pont entre vos revenus bruts, vos optimisations (Chèques Culture, TR, PEE) et vos dépenses réelles pour calculer et historiser votre Véritable Pouvoir d'Achat.

Un outil simple, léger, et 100 % privé pour reprendre le contrôle de votre capacité d'investissement.


✨ Fonctionnalités Principales


🎛️ Simulateur Double Profil :

Portage Salarial : Optimisation poussée (Frais fixes vs %, PEE 300%, Chèques Culture, IK).

Salarié Classique : Base de calcul sur le salaire brut avec maintien des avantages du CE (TR, Culture).


💾 Figeage et Budget Mensuel :

Sauvegardez l'état exact de vos finances d'un mois précis.

Saisissez vos dépenses incompressibles (Loyer, Factures) et vos investissements (PEA).


📈 Tableau de Bord & Historique :

Suivez vos KPIs (Revenus générés, Pouvoir d'achat restant, Total investi).

Filtrez vos résultats (mois, année, global).

Exportez toute votre base de données locale en un clic au format CSV/Excel.


🛠️ Stack Technique

Pensée pour la légèreté et l'auto-hébergement (consomme quelques Mo de RAM) :

Backend : Python 3 + Flask

Base de données : SQLite (Un seul fichier .db, aucun serveur lourd à maintenir)

Frontend : HTML5, CSS3, Vanilla JS (Zéro framework usine à gaz)

Déploiement : Script Bash avec création automatique d'un daemon systemd.




🚀 Installation Express (Linux / Debian / Ubuntu / LXC Proxmox)

Le projet s'installe tout seul et tourne en arrière-plan en moins de 2 minutes.

1. Clonez le dépôt sur votre machine :

git clone https://github.com/Florian-Brsn/Kpi_Finance_Personnelle.git
cd Kpi_Finance_Personnelle

2. Lancez le script d'installation automatique :

chmod +x install.sh
./install.sh
(Le script installe Python/Flask, configure l'environnement virtuel, et crée le service systemd pour que l'app se lance au démarrage).

3. Accédez à l'application :

Ouvrez un navigateur web sur n'importe quel appareil de votre réseau local :

http://VOTRE_IP_LOCALE:5000




🗺️ Roadmap (À venir dans la V1.X)

[ ] Ajout d'une catégorie d'investissement Cryptomonnaies.

[ ] Connexion API (ex: CoinGecko/Binance) pour actualiser la valeur du portfolio crypto en temps réel.

[ ] Intégration de graphiques visuels dynamiques (Chart.js) dans le tableau de bord.
