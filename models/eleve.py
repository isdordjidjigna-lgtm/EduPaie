"""Modèle métier : un élève inscrit dans l'établissement."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Eleve:
    nom: str
    prenom: str
    classe: str
    annee_scolaire: str
    montant_total: float
    id: Optional[int] = None
    date_creation: Optional[str] = None

    def nom_complet(self) -> str:
        return f"{self.nom} {self.prenom}"