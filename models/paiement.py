"""Modèle métier : un paiement effectué par un élève."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Paiement:
    eleve_id: int
    montant: float
    date_paiement: str
    mode_paiement: str
    id: Optional[int] = None

    def montant_formate(self) -> str:
        return f"{self.montant:,.0f} FCFA".replace(",", " ")