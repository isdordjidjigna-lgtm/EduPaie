"""Service métier pour les reçus (émission, ré-impression)."""
from services.exceptions import NotFoundError


class RecuService:
    def __init__(self, recu_repo, paiement_repo):
        self.recu_repo = recu_repo
        self.paiement_repo = paiement_repo

    def get(self, recu_id: int):
        recu = self.recu_repo.get(recu_id)
        if recu is None:
            raise NotFoundError(f"Reçu {recu_id} introuvable.")
        return recu

    def lister_par_eleve(self, eleve_id: int):
        return self.recu_repo.lister_par_eleve(eleve_id)

    def donnees_pour_pdf(self, recu_id: int) -> dict:
        recu = self.get(recu_id)
        paiement = self.paiement_repo.get(recu.paiement_id)
        if paiement is None:
            raise NotFoundError(f"Paiement {recu.paiement_id} introuvable.")

        return {
            "numero": recu.numero,
            "date_emission": recu.date_emission,
            "nom": recu.eleve_nom_snapshot,
            "prenom": recu.eleve_prenom_snapshot,
            "classe": recu.eleve_classe_snapshot,
            "annee": recu.eleve_annee_snapshot,
            "montant": paiement.montant,
            "mode": paiement.mode_paiement,
            "date_paiement": paiement.date_paiement,
            "solde_avant": recu.solde_avant,
            "solde_apres": recu.solde_apres,
            "nb_impressions": recu.nb_impressions,
        }

    def marquer_imprime(self, recu_id: int):
        self.recu_repo.incrementer_impressions(recu_id)