"""Modèle de tableau Qt pour afficher les élèves."""
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

from services.eleve_service import EleveService


COLONNES = ["ID", "Nom", "Prénom", "Classe", "Frais dus", "Payé", "Solde", "Statut"]


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
                "id": e.id,
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
            if col == 0: return str(row["id"])
            if col == 1: return row["nom"]
            if col == 2: return row["prenom"]
            if col == 3: return row["classe"]
            if col == 4: return f"{row['frais']:,.0f}".replace(",", " ")
            if col == 5: return f"{row['paye']:,.0f}".replace(",", " ")
            if col == 6: return f"{row['solde']:,.0f}".replace(",", " ")
            if col == 7: return row["statut"]

        if role == Qt.UserRole:
            if col == 0: return row["id"]              # int
            if col == 1: return row["nom"].lower()
            if col == 2: return row["prenom"].lower()
            if col == 3: return row["classe"].lower()
            if col == 4: return row["frais"]
            if col == 5: return row["paye"]
            if col == 6: return row["solde"]
            if col == 7: return row["statut"]

        if role == Qt.TextAlignmentRole:
            if col == 0:
                return int(Qt.AlignCenter)
            if col in (4, 5, 6):
                return int(Qt.AlignRight | Qt.AlignVCenter)
            if col == 7:
                return int(Qt.AlignCenter)

        if role == Qt.ForegroundRole and col == 7:
            statut = row["statut"]
            if statut == "Soldé":
                return QColor(0, 130, 0)
            if statut == "Partiellement payé":
                return QColor(200, 100, 0)
            if statut == "Non payé":
                return QColor(180, 0, 0)

        return None

    
    def sort(self, column, order=Qt.AscendingOrder):
        """Trie les lignes selon une colonne."""
        if column == 0:  # ID (numérique)
            key = lambda r: r["id"]
        elif column == 1:  # Nom
            key = lambda r: r["nom"].lower()
        elif column == 2:  # Prénom
            key = lambda r: r["prenom"].lower()
        elif column == 3:  # Classe
            key = lambda r: r["classe"].lower()
        elif column == 4:  # Frais
            key = lambda r: r["frais"]
        elif column == 5:  # Payé
            key = lambda r: r["paye"]
        elif column == 6:  # Solde
            key = lambda r: r["solde"]
        elif column == 7:  # Statut
            key = lambda r: r["statut"]
        else:
            return

        self.beginResetModel()
        self._rows.sort(key=key, reverse=(order == Qt.DescendingOrder))
        self.endResetModel()

    def eleve_at(self, row_index: int):
        """Retourne l'objet Eleve à une ligne donnée."""
        if 0 <= row_index < len(self._rows):
            return self._rows[row_index]["eleve"]
        return None