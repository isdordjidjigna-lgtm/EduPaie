"""Tableau de bord : KPI globaux + filtre par statut."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QComboBox, QTableView, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QFont

from ui.models import EleveTableModel


class KPICard(QFrame):
    """Carte d'un indicateur (nombre d'élèves, total encaissé, etc.)."""
    def __init__(self, titre, valeur, couleur="#1976D2"):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("kpiCard")
        self.setStyleSheet(
            f"QFrame#kpiCard {{ border-left: 5px solid {couleur}; "
            f"background-color: #f5f5f5; border-radius: 4px; }}"
        )

        self.titre_label = QLabel(titre)
        self.titre_label.setStyleSheet("color: #555; font-size: 11pt;")

        self.valeur_label = QLabel(valeur)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.valeur_label.setFont(font)
        self.valeur_label.setStyleSheet(f"color: {couleur};")

        layout = QVBoxLayout(self)
        layout.addWidget(self.titre_label)
        layout.addWidget(self.valeur_label)

    def set_valeur(self, texte):
        self.valeur_label.setText(texte)


class DashboardView(QWidget):
    def __init__(self, eleve_service, paiement_service, parent=None):
        super().__init__(parent)
        self.eleve_service = eleve_service
        self.paiement_service = paiement_service

        # --- Cartes KPI ---
        self.card_eleves = KPICard("Nombre d'élèves", "0", "#1976D2")
        self.card_encaisse = KPICard("Total encaissé", "0 FCFA", "#388E3C")
        self.card_restant = KPICard("Total restant dû", "0 FCFA", "#D32F2F")
        self.card_non_soldes = KPICard("Élèves non soldés", "0", "#F57C00")

        cards = QHBoxLayout()
        cards.addWidget(self.card_eleves)
        cards.addWidget(self.card_encaisse)
        cards.addWidget(self.card_restant)
        cards.addWidget(self.card_non_soldes)

        # --- Filtre statut ---
        self.statut_combo = QComboBox()
        self.statut_combo.addItem("Tous les statuts", userData=None)
        self.statut_combo.addItem("Soldé", userData="Soldé")
        self.statut_combo.addItem("Partiellement payé", userData="Partiellement payé")
        self.statut_combo.addItem("Non payé", userData="Non payé")
        self.statut_combo.currentIndexChanged.connect(self._apply_filter)

        filtre = QHBoxLayout()
        filtre.addWidget(QLabel("Filtrer par statut :"))
        filtre.addWidget(self.statut_combo)
        filtre.addStretch()

        # --- Tableau ---
        self.model = EleveTableModel(self.eleve_service)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setSortRole(Qt.UserRole)
        

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # --- Layout global ---
        layout = QVBoxLayout(self)
        layout.addLayout(cards)
        layout.addLayout(filtre)
        layout.addWidget(QLabel("<b>Liste des élèves</b>"))
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        # 1. Rafraîchir les données
        self.model.refresh()

        # 2. Mettre à jour les cartes KPI
        eleves = self.eleve_service.lister_tous()
        nb_eleves = len(eleves)

        total_du = 0.0
        total_encaisse = 0.0
        nb_non_soldes = 0

        for e in eleves:
            solde = self.eleve_service.calculer_solde(e.id)
            paye = e.montant_total - solde
            total_du += e.montant_total
            total_encaisse += paye
            if self.eleve_service.statut(e.id) != "Soldé":
                nb_non_soldes += 1

        restant = total_du - total_encaisse

        self.card_eleves.set_valeur(str(nb_eleves))
        self.card_encaisse.set_valeur(
            f"{total_encaisse:,.0f} FCFA".replace(",", " ")
        )
        self.card_restant.set_valeur(
            f"{restant:,.0f} FCFA".replace(",", " ")
        )
        self.card_non_soldes.set_valeur(str(nb_non_soldes))

        # 3. Ré-appliquer le filtre
        self._apply_filter()

    def _apply_filter(self):
        statut = self.statut_combo.currentData()
        if statut is None:
            self.proxy.setFilterKeyColumn(-1)
            self.proxy.setFilterFixedString("")
        else:
            # colonne 7 = Statut
            self.proxy.setFilterKeyColumn(7)
            self.proxy.setFilterFixedString(statut)