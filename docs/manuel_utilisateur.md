# Manuel utilisateur — EduPaie

**Application desktop de gestion des paiements scolaires**

---

## 1. Lancer l'application

Double-cliquez sur l'icône **EduPaie** sur le Bureau, ou ouvrez le Menu Démarrer et tapez **EduPaie**.

Le **tableau de bord** s'affiche à l'ouverture.

---

## 2. Naviguer dans l'application

La **barre latérale gauche** contient deux menus :

| Menu | Rôle |
|------|------|
| **📊 Tableau de bord** | Vue d'ensemble : nombre d'élèves, total encaissé, restant dû, élèves non soldés |
| **👥 Élèves** | Liste des élèves, recherche, filtre, ajout, modification, suppression |

Le menu actif est surligné en **bleu**.

---

## 3. Consulter le tableau de bord

Le tableau de bord affiche **4 indicateurs clés** :

| Indicateur | Signification |
|------------|---------------|
| **Nombre d'élèves** | Total d'élèves enregistrés |
| **Total encaissé** | Somme de tous les paiements reçus |
| **Total restant dû** | Somme des soldes restants |
| **Élèves non soldés** | Nombre d'élèves dont le solde > 0 |

Sous les indicateurs, une **liste complète** des élèves avec leur statut coloré.

**Filtre** : utilisez la liste déroulante **« Filtrer par statut »** pour n'afficher que :
- Tous les statuts
- Soldé (vert)
- Partiellement payé (orange)
- Non payé (rouge)

---

## 4. Enregistrer un élève

1. Cliquez sur **👥 Élèves** dans la barre latérale
2. Cliquez sur **➕ Ajouter un élève** (en haut à droite, bouton bleu)
3. Remplissez les champs :
   - **Nom** (obligatoire)
   - **Prénom** (obligatoire)
   - **Classe** (obligatoire) — ex. : 5ème B
   - **Année scolaire** (obligatoire) — ex. : 2025-2026
   - **Montant total dû** (obligatoire) — ex. : 250000
4. Cliquez sur **Enregistrer**

L'élève apparaît dans la liste.

---

## 5. Rechercher ou filtrer un élève

**Recherche par nom/prénom** :
- Tapez dans le champ **« Rechercher (nom, prenom)... »**
- La liste se filtre automatiquement

**Filtre par classe** :
- Utilisez la liste déroulante **« Toutes les classes »**
- Choisissez une classe

**Réinitialiser les filtres** :
- Cliquez sur le bouton **« Réinitialiser »**

---

## 6. Enregistrer un paiement

1. Dans la liste des élèves, **double-cliquez** sur l'élève concerné
   (ou sélectionnez-le puis cliquez sur **📄 Voir la fiche**)
2. Dans la fiche élève, cliquez sur **➕ Enregistrer un paiement** (bouton vert)
3. Remplissez :
   - **Montant** (obligatoire, > 0)
   - **Date** (obligatoire)
   - **Mode de paiement** : espèces, chèque, virement, mobile money
4. Cliquez sur **Valider**

**Règles de validation** :
- Si le montant **dépasse le solde restant** → message d'erreur, enregistrement refusé
- Si le montant est **nul ou négatif** → message d'erreur
- Si **tous les champs** sont valides → paiement enregistré, PDF généré, solde recalculé

---

## 7. Consulter, revoir ou imprimer un reçu

### Consulter un reçu déjà émis

1. Ouvrez la **fiche de l'élève** (double-clic sur l'élève)
2. Faites défiler jusqu'à l'**historique des paiements**
3. Trouvez la ligne du reçu concerné
4. Cliquez sur **🔍 Revoir** → le PDF s'ouvre

### Imprimer un reçu

1. Le PDF est ouvert dans votre lecteur
2. Faites **Ctrl + P** pour imprimer
3. Sélectionnez votre imprimante
4. Validez

---

## 8. Modifier ou supprimer un élève

### Modifier

1. Sélectionnez l'élève dans la liste
2. Cliquez sur **✏️ Modifier**
3. Modifiez les champs
4. Cliquez sur **Enregistrer**

### Supprimer

1. Sélectionnez l'élève dans la liste
2. Cliquez sur **🗑️ Supprimer** (bouton rouge)
3. Confirmez la suppression

⚠️ **Attention** : la suppression d'un élève supprime **aussi** tous ses paiements et reçus.

---

## 9. Comprendre les statuts

| Statut | Couleur | Signification |
|--------|---------|---------------|
| **Soldé** | 🟢 Vert | Le solde est à 0 — tout est payé |
| **Partiellement payé** | 🟠 Orange | Un paiement a été fait, mais il reste un solde |
| **Non payé** | 🔴 Rouge | Aucun paiement enregistré |

---

## 10. En cas d'erreur

- **Champ vide** → message indiquant le champ à remplir
- **Montant invalide** → message demandant un montant positif
- **Montant > solde** → message indiquant le solde restant
- **Erreur inattendue** → message avec fichier `edupaie_errors.log` (envoyez ce fichier en cas de problème)

---

## 11. Fermer l'application

Cliquez sur la **croix** en haut à droite de la fenêtre.

---

## 12. Besoin d'aide ?

Consultez la documentation technique ou contactez l'administrateur.

**Auteur** : Isidore Komlan Djidjignan
**Dépôt** : https://github.com/isdordjidjigna-lgtm/EduPaie