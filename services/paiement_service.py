"""Service métier pour l'enregistrement des paiements."""
from datetime import datetime

from services.exceptions import (
    NotFoundError, ValidationError, SoldeInsuffisantError
)

MODES_VALIDES = {"espèces", "chèque", "virement", "mobile_money"}
EPSILON = 0.01


class PaiementService:
    def __init__(self, db, eleve_repo, paiement_repo, recu_repo):
        self.db = db
        self.eleve_repo = eleve_repo
        self.paiement_repo = paiement_repo
        self.recu_repo = recu_repo

    def calculer_solde(self, eleve_id: int) -> float:
        eleve = self.eleve_repo.get(eleve_id)
        if eleve is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")
        paye = self.paiement_repo.somme_par_eleve(eleve_id)
        return round(eleve.montant_total - paye, 2)

    def _valider(self, eleve_id, montant, date_str, mode):
        try:
            montant = float(montant)
        except (TypeError, ValueError):
            raise ValidationError("Le montant doit être un nombre.")
        if montant <= 0:
            raise ValidationError("Le montant doit être strictement positif.")
        if round(montant, 2) != montant:
            raise ValidationError("Le montant ne peut avoir que 2 décimales.")

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Date invalide (format AAAA-MM-JJ).")
        if date > datetime.now():
            raise ValidationError("La date ne peut pas être dans le futur.")

        if mode not in MODES_VALIDES:
            raise ValidationError(f"Mode de paiement invalide : {mode}")

        eleve = self.eleve_repo.get(eleve_id)
        if eleve is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")

        solde = self.calculer_solde(eleve_id)
        if montant > solde + EPSILON:
            raise SoldeInsuffisantError(
                f"Le montant saisi ({montant:,.0f} FCFA) dépasse "
                f"le solde restant ({solde:,.0f} FCFA).".replace(",", " ")
            )
        return montant, date, eleve, solde

    def enregistrer(self, eleve_id, montant, date_str, mode):
        montant, date, eleve, solde = self._valider(
            eleve_id, montant, date_str, mode
        )

        with self.db.transaction() as c:
            cur = c.execute(
                "INSERT INTO paiement(eleve_id, montant, date_paiement, mode_paiement) "
                "VALUES(?, ?, ?, ?)",
                (eleve_id, montant, date_str, mode),
            )
            paiement_id = cur.lastrowid

            annee = datetime.now().year
            row = c.execute(
                "SELECT COUNT(*) AS n FROM recu WHERE numero LIKE ?",
                (f"REC-{annee}-%",),
            ).fetchone()
            numero = f"REC-{annee}-{row['n'] + 1:06d}"

            solde_apres = round(solde - montant, 2)
            cur2 = c.execute(
                "INSERT INTO recu(numero, paiement_id, date_emission, "
                "solde_avant, solde_apres, "
                "eleve_nom_snapshot, eleve_prenom_snapshot, "
                "eleve_classe_snapshot, eleve_annee_snapshot) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (numero, paiement_id,
                 datetime.now().isoformat(timespec="seconds"),
                 solde, solde_apres,
                 eleve.nom, eleve.prenom, eleve.classe, eleve.annee_scolaire),
            )
            recu_id = cur2.lastrowid

        return paiement_id, recu_id, numero