# Guide d'installation — EduPaie

Ce guide explique comment installer et lancer **EduPaie** sur une machine Windows.

---

## 1. Prérequis

- Système : **Windows 10 ou Windows 11** (64 bits)
- Espace disque : **~300 Mo**
- **Aucune installation de Python n'est requise** (l'exécutable est autonome)

---

## 2. Installation

### Étape 1 — Récupérer l'installeur

Deux possibilités :

- **Option A** — Télécharger le fichier `Setup_EduPaie.exe` depuis le dépôt Git
  (section *Releases* ou depuis `installer_output/`).
- **Option B** — Compiler soi-même (voir §4).

### Étape 2 — Lancer l'installeur

1. **Double-cliquez** sur `Setup_EduPaie.exe`
2. Une fenêtre d'installation s'ouvre
3. Cliquez sur **Suivant** → **Suivant** → **Installer**
4. Attendez la fin (~30 secondes)
5. Cliquez sur **Terminer**

L'installeur :

- Copie `EduPaie.exe` et `edupaie.db` dans le dossier d'installation
- Crée un raccourci sur le **Bureau**
- Ajoute EduPaie au **Menu Démarrer**
- Permet une désinstallation propre via le **Panneau de configuration**

### Étape 3 — Lancer l'application

**Trois méthodes possibles :**

- Double-cliquez sur le raccourci **EduPaie** sur le Bureau
- Menu Démarrer → tapez **EduPaie** → **Entrée**
- Ouvrez le dossier d'installation et double-cliquez sur `EduPaie.exe`

---

## 3. Première utilisation

Au premier lancement :

1. L'application affiche le **tableau de bord** avec les statistiques
2. La base de démonstration contient **15 élèves** et **22 paiements**
3. Vous pouvez immédiatement :
   - Consulter la liste des élèves
   - Enregistrer un paiement
   - Générer un reçu PDF

---

## 4. Désinstallation

1. **Panneau de configuration** → **Programmes et fonctionnalités**
2. Trouvez **EduPaie** dans la liste
3. **Clic droit** → **Désinstaller**
4. Confirmez

⚠️ **Attention** : la désinstallation supprime l'application **ET** la base `edupaie.db`.
Sauvegardez vos données avant si nécessaire.

---

## 5. Compilation manuelle (développeurs)

Si vous voulez recompiler l'application vous-même :

### Prérequis

- **Python 3.10 ou supérieur**
- **Git**
- **Inno Setup** (pour l'installeur)

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/isdordjidjigna-lgtm/EduPaie.git
cd EduPaie

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/Scripts/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Compiler l'exécutable
pyinstaller edupaie.spec

# 5. Copier la base à côté de l'exécutable
cp edupaie.db dist/

# 6. (Optionnel) Regénérer l'installeur
# Ouvrir installer.iss dans Inno Setup Compiler
# Menu Build → Compile (ou Ctrl+F9)