"""Modèle de tableau Qt pour afficher les élèves."""
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

from services.eleve_service import EleveService


COLONNES = ["Nom", "Prénom", "Classe", "Frais dus", "Payé", "Solde", "Statut"]


class EleveTableModel(QAbstractTableModel):
    def __init__(self, eleve_service: EleveService):
        super().__init__()
        self.eleve_service = eleve_service
        self._rows = []  # liste de dicts avec toutes les infos calculées

    def refresh(self):
        """Recharge les données depuis la base."""
        self.beginResetModel()
        eleves = self.eleve_service.lister_tous()
        self._rows = []
        for e in eleves:
            solde = self.eleve_service.calculer_solde(e.id)
            paye = e.montant_total - solde
            statut = self.eleve_service.statut(e.id)
            self._rows.append({
                "eleve": e,
                "nom": e.nom,
                "prenom": e.prenom,
                "classe": e.classe,
                "frais": e.montant_total,
                "paye": paye,
                "solde": solde,
                "statut": statut,
            })
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return len(COLONNES)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return COLONNES[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0: return row["nom"]
            if col == 1: return row["prenom"]
            if col == 2: return row["classe"]
            if col == 3: return f"{row['frais']:,.0f}".replace(",", " ")
            if col == 4: return f"{row['paye']:,.0f}".replace(",", " ")
            if col == 5: return f"{row['solde']:,.0f}".replace(",", " ")
            if col == 6: return row["statut"]

        if role == Qt.TextAlignmentRole:
            if col in (3, 4, 5):
                return int(Qt.AlignRight | Qt.AlignVCenter)
            if col == 6:
                return int(Qt.AlignCenter)

        if role == Qt.ForegroundRole and col == 6:
            statut = row["statut"]
            if statut == "Soldé":
                return QColor(0, 130, 0)
            if statut == "Partiellement payé":
                return QColor(200, 100, 0)
            if statut == "Non payé":
                return QColor(180, 0, 0)

        return None

    def eleve_at(self, row_index: int):
        """Retourne l'objet Eleve à une ligne donnée."""
        if 0 <= row_index < len(self._rows):
            return self._rows[row_index]["eleve"]
        return None