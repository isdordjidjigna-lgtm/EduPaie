"""Modèle métier : un reçu émis pour un paiement.

Les snapshots (nom, prénom, classe, année) garantissent que la
ré-impression du reçu reste identique même si l'élève change de
classe plus tard.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Recu:
    numero: str
    paiement_id: int
    date_emission: str
    solde_avant: float
    solde_apres: float
    eleve_nom_snapshot: str
    eleve_prenom_snapshot: str
    eleve_classe_snapshot: str
    eleve_annee_snapshot: str
    id: Optional[int] = None
    nb_impressions: int = 0

    def est_reimpression(self) -> bool:
        return self.nb_impressions > 0