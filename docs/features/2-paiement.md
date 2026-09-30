# Fonctionnalité 2 — Enregistrement d'un paiement

- Montant, date, mode (espèces / chèque / virement / mobile money)
- Rattaché à un élève
- Anti-dépassement : refus si montant > solde restant

Fichiers concernés :
- ui/paiement_dialog.py
- services/paiement_service.py
- services/exceptions.py
