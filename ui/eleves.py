"""Vue liste des élèves : recherche + filtre par classe."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTableView, QAbstractItemView,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, QSortFilterProxyModel

from ui.decorators import safe_slot
from ui.models import EleveTableModel
from ui.eleve_form import EleveForm
from ui.fiche_eleve import FicheEleveDialog


class ElevesView(QWidget):
    def __init__(self, eleve_service, paiement_service,
                 recu_service, pdf_generator, parent=None):
        super().__init__(parent)
        self.eleve_service = eleve_service
        self.paiement_service = paiement_service
        self.recu_service = recu_service
        self.pdf_generator = pdf_generator

        # --- Barre de filtres ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher (nom, prenom)...")
        self.search_input.setClearButtonEnabled(True)

        self.classe_combo = QComboBox()
        self.classe_combo.addItem("Toutes les classes", userData=None)

        self.btn_reset = QPushButton("Réinitialiser")
        self.btn_reset.setProperty("class", "secondaryBtn")
        self.btn_ajouter = QPushButton("➕ Ajouter un élève")
        self.btn_ajouter.setProperty("class", "actionBtn")
        self.btn_ajouter.clicked.connect(self._on_ajouter)

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Recherche :"))
        bar.addWidget(self.search_input, stretch=2)
        bar.addWidget(QLabel("Classe :"))
        bar.addWidget(self.classe_combo, stretch=1)
        bar.addWidget(self.btn_reset)
        bar.addWidget(self.btn_ajouter)

        # --- Tableau ---
        self.model = EleveTableModel(self.eleve_service)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(-1)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.doubleClicked.connect(self._on_voir_fiche)

        # --- Boutons bas ---
        self.btn_modifier = QPushButton("✏️ Modifier")
        self.btn_modifier.setProperty("class", "actionBtn")
        self.btn_supprimer = QPushButton("🗑️ Supprimer")
        self.btn_supprimer.setProperty("class", "dangerBtn")
        self.btn_fiche = QPushButton("📄 Voir la fiche")
        self.btn_fiche.setProperty("class", "actionBtn")

        self.btn_modifier.clicked.connect(self._on_modifier)
        self.btn_supprimer.clicked.connect(self._on_supprimer)
        self.btn_fiche.clicked.connect(self._on_voir_fiche)

        bas = QHBoxLayout()
        bas.addWidget(self.btn_fiche)
        bas.addStretch()
        bas.addWidget(self.btn_modifier)
        bas.addWidget(self.btn_supprimer)

        # --- Layout global ---
        layout = QVBoxLayout(self)
        layout.addLayout(bar)
        layout.addWidget(self.table)
        layout.addLayout(bas)

        # --- Signaux ---
        self.search_input.textChanged.connect(self._apply_filters)
        self.classe_combo.currentIndexChanged.connect(self._apply_filters)
        self.btn_reset.clicked.connect(self._reset_filters)

        self.refresh()

    def refresh(self):
        eleves = self.eleve_service.lister_tous()
        classes = sorted({e.classe for e in eleves})

        current = self.classe_combo.currentData()
        self.classe_combo.blockSignals(True)
        self.classe_combo.clear()
        self.classe_combo.addItem("Toutes les classes", userData=None)
        for c in classes:
            self.classe_combo.addItem(c, userData=c)
        idx = self.classe_combo.findData(current)
        self.classe_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.classe_combo.blockSignals(False)

        self.model.refresh()
        self._apply_filters()

    def _apply_filters(self):
        self.proxy.setFilterFixedString(self.search_input.text().strip())
        classe = self.classe_combo.currentData()
        if classe:
            self.proxy.setFilterKeyColumn(2)
            self.proxy.setFilterFixedString(classe)
        else:
            self.proxy.setFilterKeyColumn(-1)
            self.proxy.setFilterFixedString(self.search_input.text().strip())

    def _reset_filters(self):
        self.search_input.clear()
        self.classe_combo.setCurrentIndex(0)

    def _get_selected_eleve(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return None
        source_idx = self.proxy.mapToSource(idx)
        return self.model.eleve_at(source_idx.row())

    @safe_slot
    def _on_ajouter(self):
        form = EleveForm(self.eleve_service, parent=self)
        if form.exec():
            self.refresh()

    @safe_slot
    def _on_modifier(self):
        eleve = self._get_selected_eleve()
        if eleve is None:
            QMessageBox.warning(self, "Aucune sélection",
                                "Sélectionnez un élève dans la liste.")
            return
        form = EleveForm(self.eleve_service, eleve=eleve, parent=self)
        if form.exec():
            self.refresh()

    @safe_slot
    def _on_supprimer(self):
        eleve = self._get_selected_eleve()
        if eleve is None:
            QMessageBox.warning(self, "Aucune sélection",
                                "Sélectionnez un élève dans la liste.")
            return
        rep = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer {eleve.nom} {eleve.prenom} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self.eleve_service.supprimer(eleve.id)
            self.refresh()

    @safe_slot
    def _on_voir_fiche(self):
        eleve = self._get_selected_eleve()
        if eleve is None:
            return
        dialog = FicheEleveDialog(
            eleve, self.eleve_service, self.paiement_service,
            self.recu_service, self.pdf_generator, self
        )
        dialog.exec()
        self.refresh()