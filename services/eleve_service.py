"""Service métier pour les élèves et le calcul des soldes."""
from typing import Optional

from services.exceptions import NotFoundError, ValidationError

EPSILON = 0.01


class EleveService:
    def __init__(self, eleve_repo, paiement_repo):
        self.eleve_repo = eleve_repo
        self.paiement_repo = paiement_repo

    # ---------- CRUD ----------

    def _valider(self, nom, prenom, classe, annee, frais):
        if not nom.strip():
            raise ValidationError("Le nom est obligatoire.")
        if not prenom.strip():
            raise ValidationError("Le prénom est obligatoire.")
        if not classe.strip():
            raise ValidationError("La classe est obligatoire.")
        if not annee.strip():
            raise ValidationError("L'année scolaire est obligatoire.")
        try:
            frais = float(frais)
        except (TypeError, ValueError):
            raise ValidationError("Les frais doivent être un nombre.")
        if frais < 0:
            raise ValidationError("Les frais ne peuvent pas être négatifs.")
        return frais

    def creer(self, nom, prenom, classe, annee, frais) -> int:
        frais = self._valider(nom, prenom, classe, annee, frais)
        return self.eleve_repo.insert(
            nom.strip(), prenom.strip(), classe.strip(), annee.strip(), frais
        )

    def modifier(self, eleve_id, nom, prenom, classe, annee, frais):
        if self.eleve_repo.get(eleve_id) is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")
        frais = self._valider(nom, prenom, classe, annee, frais)
        self.eleve_repo.update(
            eleve_id, nom.strip(), prenom.strip(),
            classe.strip(), annee.strip(), frais
        )

    def supprimer(self, eleve_id):
        if self.eleve_repo.get(eleve_id) is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")
        if self.eleve_repo.a_des_paiements(eleve_id):
            raise ValidationError(
                "Impossible de supprimer : cet élève a des paiements enregistrés."
            )
        self.eleve_repo.delete(eleve_id)

    # ---------- Lectures ----------

    def lister_tous(self):
        return self.eleve_repo.lister_tous()

    def lister_classes(self):
        return self.eleve_repo.lister_classes()

    def get(self, eleve_id) -> Optional:
        return self.eleve_repo.get(eleve_id)

    # ---------- Règle métier centrale ----------

    def calculer_solde(self, eleve_id: int) -> float:
        """Solde = frais_total − somme des paiements. Jamais stocké."""
        eleve = self.eleve_repo.get(eleve_id)
        if eleve is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")
        total_paye = self.paiement_repo.somme_par_eleve(eleve_id)
        return round(eleve.montant_total - total_paye, 2)

    def statut(self, eleve_id: int) -> str:
        eleve = self.eleve_repo.get(eleve_id)
        if eleve is None:
            raise NotFoundError(f"Élève {eleve_id} introuvable.")
        solde = self.calculer_solde(eleve_id)
        total_paye = eleve.montant_total - solde

        if total_paye < EPSILON:
            return "Non payé"
        if abs(solde) < EPSILON:
            return "Soldé"
        return "Partiellement payé"