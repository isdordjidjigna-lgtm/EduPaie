# EduPaie

Application desktop de gestion des paiements scolaires.

## Problème

De nombreuses écoles suivent les paiements des élèves à la main
(cahier, Excel), sans vue fiable sur qui a payé quoi ni combien
il reste à encaisser. Les reçus ne sont pas numérotés et sont
impossibles à retrouver en cas de litige.

## Solution

EduPaie est une application desktop qui :
- Enregistre les élèves et leurs frais de scolarité
- Enregistre chaque paiement (espèces, chèque, virement, mobile money)
- Calcule automatiquement le solde restant dû
- Émet un reçu numéroté à chaque versement (PDF)
- Permet la ré-impression à l'identique depuis l'historique

## Stack technique

- Python 3.10+
- PySide6 (interface graphique)
- SQLite (base de données)
- ReportLab (génération PDF)
- PyInstaller (packaging .exe)

## Installation (développement)

```bash
# Cloner le dépôt
git clone https://github.com/isdordjidjigna-lgtm/EduPaie.git
cd EduPaie

# Créer un environnement virtuel
python -m venv .venv

# Activer
# Windows Git Bash :
source .venv/Scripts/activate
# Windows cmd :
.venv\Scripts\activate.bat

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base avec le jeu de données
python -m database.seed

# Lancer l'application
python main.py