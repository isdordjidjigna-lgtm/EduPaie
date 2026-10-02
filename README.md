# EduPaie — Gestion des paiements scolaires

Application desktop de gestion des paiements pour les établissements scolaires.

**Auteur :** Isidore Komlan Djidjignan
**Dépôt :** https://github.com/isdordjidjigna-lgtm/EduPaie
**Date :** 29/09 - 02/10/2026

---

## Problème

De nombreuses écoles suivent les paiements des élèves à la main (cahier, Excel),
sans vue fiable sur qui a payé quoi ni combien il reste à encaisser. Les reçus
ne sont pas numérotés et sont impossibles à retrouver en cas de litige.

## Solution

EduPaie est une application desktop qui permet de :
- Enregistrer les élèves et leurs frais de scolarité
- Enregistrer chaque paiement (espèces, chèque, virement, mobile money)
- Calculer automatiquement le solde restant dû et le statut de paiement
- Émettre un reçu numéroté à chaque versement (PDF)
- Ré-imprimer un reçu à l'identique depuis l'historique

---

## Fonctionnalités

| # | Fonctionnalité | Description |
|---|---|---|
| 1 | **Gestion des élèves** | Ajouter / modifier / supprimer un élève. Recherche par nom, filtre par classe. |
| 2 | **Enregistrement d'un paiement** | Montant, date, mode. Anti-dépassement : refus si montant > solde restant. |
| 3 | **Calcul automatique du solde** | Solde = total dû − somme des paiements. Statut dérivé (Soldé / Partiellement payé / Non payé). |
| 4 | **Historique des paiements** | Liste chronologique par élève, avec ré-impression d'un reçu déjà émis. |
| 5 | **Génération du reçu PDF** | Numéro unique, snapshots de l'élève, montant, mode, soldes avant/après. |
| 6 | **Tableau de bord** | KPI globaux (élèves, encaissé, restant dû, non soldés) + filtre par statut. |

---

## Architecture

Le projet est structuré en **3 couches** :

```
┌─────────────────────────────────────────┐
│           UI (PySide6)                  │
│  MainWindow · DashboardView · ElevesView│
│  FicheEleveDialog · PaiementDialog      │
└────────────────┬────────────────────────┘
                 │ appels de services
                 ▼
┌─────────────────────────────────────────┐
│        MÉTIER (Services)                │
│  EleveService · PaiementService         │
│  RecuService · PDFGenerator             │
│  (validation, solde, anti-dépassement)  │
└────────────────┬────────────────────────┘
                 │ appels de repositories
                 ▼
┌─────────────────────────────────────────┐
│      DONNÉES (Repositories + SQLite)    │
│  EleveRepository · PaiementRepository   │
│  RecuRepository · Database              │
└─────────────────────────────────────────┘
```

**Règle d'or** : aucun widget ne contient de SQL. L'UI appelle les services,
qui appellent les repositories.

### Base de données

3 tables :
- **`eleve`** — nom, prénom, classe, année scolaire, frais totaux
- **`paiement`** — montant, date, mode (rattaché à un élève)
- **`recu`** — numéro unique, snapshots élève, soldes avant/après

Voir le MCD complet dans [`docs/mcd.md`](docs/mcd.md).

---

## Stack technique

| Techno | Version | Rôle |
|---|---|---|
| **Python** | 3.10+ | Langage |
| **PySide6** | 6.11.2 | Interface graphique (Qt) |
| **SQLite** | 3.x (stdlib) | Base de données |
| **ReportLab** | 4.2.5 | Génération PDF |
| **PyInstaller** | 6.x | Packaging `.exe` |

---

## Installation (développement)

### Prérequis

- Python 3.10 ou supérieur
- Git

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/isdordjidjigna-lgtm/EduPaie.git
cd EduPaie

# 2. Créer un environnement virtuel
python -m venv .venv

# 3. Activer le venv
# Windows Git Bash :
source .venv/Scripts/activate
# Windows cmd :
.venv\Scripts\activate.bat

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Initialiser la base avec le jeu de données
python -m database.seed

# 6. Lancer l'application
python main.py
```

---

## Utilisation de l'exécutable Windows

Un exécutable autonome **`EduPaie.exe`** est fourni (pas besoin de Python).

### Installation

1. Créez un dossier `EduPaie` (par exemple sur le Bureau)
2. Placez dans ce dossier :
   - `EduPaie.exe`
   - `edupaie.db`
3. Double-cliquez sur `EduPaie.exe`

Voir le guide détaillé dans [`docs/guide_installation.md`](docs/guide_installation.md).

---

## Structure du projet

```
EduPaie/
├── main.py                  # Point d'entrée + excepthook global
├── edupaie.db               # Base SQLite (générée par seed)
├── requirements.txt
├── README.md
├── edupaie.spec             # Spec PyInstaller
│
├── database/                # Couche données
│   ├── database.py          # Connexion + transactions
│   ├── schema.sql           # DDL (3 tables)
│   └── seed.py              # 15 élèves + 22 paiements
│
├── models/                  # Dataclasses
│   ├── eleve.py
│   ├── paiement.py
│   └── recu.py
│
├── repositories/            # SQL
│   ├── eleve_repository.py
│   ├── paiement_repository.py
│   └── recu_repository.py
│
├── services/                # Logique métier
│   ├── eleve_service.py
│   ├── paiement_service.py
│   ├── recu_service.py
│   ├── pdf_generator.py
│   └── exceptions.py
│
├── ui/                      # Interface PySide6
│   ├── main_window.py
│   ├── dashboard.py
│   ├── eleves.py
│   ├── eleve_form.py
│   ├── fiche_eleve.py
│   ├── paiement_dialog.py
│   ├── models.py
│   └── decorators.py
│
├── utils/
├── tests/
├── resources/
└── docs/                    # Documentation
    ├── mcd.md               # MCD / UML
    ├── documentation.md     # Documentation technique
    ├── manuel_utilisateur.md
    ├── guide_installation.md
    └── features/            # Docs des fonctionnalités (branches)
```

---

## Tests

Un jeu de tests manuels est décrit dans [`docs/documentation.md`](docs/documentation.md).

Scénarios à valider :
1. Saisir un montant négatif → refus
2. Saisir un montant > solde → refus
3. Saisir une date future → refus
4. Créer un élève, modifier, supprimer
5. Enregistrer un paiement, vérifier le reçu PDF
6. Ré-imprimer un reçu depuis l'historique

---

## Historique Git

Le projet utilise une **stratégie par branches** :

- `main` — branche principale stable
- `feature/1-gestion-eleves` → `feature/6-dashboard` — une branche par fonctionnalité du CDC
- `build/packaging` — exécutable Windows
- `backup-avant-refonte` — sauvegarde

Chaque branche est fusionnée dans `main` avec un merge commit visible.

Voir : `git log --oneline --graph --all`

---

## Auteur

**Isidore Komlan Djidjignan**
Étudiant en Développement Web et Web Mobile
Projet réalisé dans le cadre du brief pédagogique
Année 2026

## formateur
**ing. GBADAMASSI Abdou-Akim **.