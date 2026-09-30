"""Exceptions métier utilisées par les services."""


class MetierError(Exception):
    """Classe de base pour toutes les exceptions métier."""
    pass


class ValidationError(MetierError):
    """Donnée invalide (montant négatif, date future, etc.)."""
    pass


class NotFoundError(MetierError):
    """Élément introuvable (élève, paiement, reçu)."""
    pass


class SoldeInsuffisantError(ValidationError):
    """Le paiement dépasse le solde restant dû."""
    pass