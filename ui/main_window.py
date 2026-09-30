"""Fenêtre principale : sidebar + navigation + titre de page."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt

from ui.dashboard import DashboardView
from ui.eleves import ElevesView


class MainWindow(QMainWindow):
    def __init__(self, eleve_service, paiement_service,
                 recu_service, pdf_generator, parent=None):
        super().__init__(parent)
        self.eleve_service = eleve_service
        self.paiement_service = paiement_service
        self.recu_service = recu_service
        self.pdf_generator = pdf_generator

        self.setWindowTitle("EduPaie — Gestion des paiements scolaires")
        self.setMinimumSize(1100, 700)

        # ============================
        # SIDEBAR
        # ============================
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #263238;
                color: white;
                border: none;
                font-size: 12pt;
                padding-top: 0px;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-bottom: 1px solid #37474F;
            }
            QListWidget::item:selected {
                background-color: #1976D2;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #37474F;
            }
        """)

        item_dashboard = QListWidgetItem("📊  Tableau de bord")
        item_eleves = QListWidgetItem("👥  Élèves")
        self.sidebar.addItem(item_dashboard)
        self.sidebar.addItem(item_eleves)

        # Titre de la sidebar
        titre_sidebar = QLabel("EduPaie")
        titre_sidebar.setAlignment(Qt.AlignCenter)
        titre_sidebar.setFixedHeight(80)
        titre_sidebar.setStyleSheet(
            "color: white; font-size: 22pt; font-weight: bold; "
            "background-color: #1A2327; padding: 20px;"
        )

        # Colonne sidebar (titre + liste)
        colonne_sidebar = QVBoxLayout()
        colonne_sidebar.setContentsMargins(0, 0, 0, 0)
        colonne_sidebar.setSpacing(0)
        colonne_sidebar.addWidget(titre_sidebar)
        colonne_sidebar.addWidget(self.sidebar, stretch=1)

        conteneur_sidebar = QWidget()
        conteneur_sidebar.setLayout(colonne_sidebar)
        conteneur_sidebar.setFixedWidth(220)

        # ============================
        # BARRE DE TITRE (en haut à droite)
        # ============================
        self.titre_page = QLabel("Tableau de bord")
        self.titre_page.setStyleSheet(
            "font-size: 24pt; font-weight: bold; color: #263238; "
            "padding: 20px; background-color: white; "
            "border-bottom: 2px solid #1976D2;"
        )

        # ============================
        # CONTENU EMPILÉ
        # ============================
        self.stack = QStackedWidget()
        self.dashboard_view = DashboardView(
            self.eleve_service, self.paiement_service
        )
        self.eleves_view = ElevesView(
            self.eleve_service, self.paiement_service,
            self.recu_service, self.pdf_generator
        )
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.eleves_view)

        # ============================
        # COLONNE DROITE (titre + contenu)
        # ============================
        colonne_droite = QVBoxLayout()
        colonne_droite.setContentsMargins(0, 0, 0, 0)
        colonne_droite.setSpacing(0)
        colonne_droite.addWidget(self.titre_page)
        colonne_droite.addWidget(self.stack, stretch=1)

        conteneur_droite = QWidget()
        conteneur_droite.setLayout(colonne_droite)

        # ============================
        # LAYOUT GLOBAL
        # ============================
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(conteneur_sidebar)
        layout.addWidget(conteneur_droite, stretch=1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ============================
        # SIGNAUX
        # ============================
        self.sidebar.currentRowChanged.connect(self._on_sidebar_change)
        self.sidebar.setCurrentRow(0)

        self.statusBar().showMessage("Prêt")

    def _on_sidebar_change(self, row):
        """Change la page affichée et met à jour le titre."""
        self.stack.setCurrentIndex(row)

        titres = {
            0: "Tableau de bord",
            1: "Gestion des élèves",
        }
        self.titre_page.setText(titres.get(row, "EduPaie"))

        # Rafraîchir la vue affichée
        if row == 0:
            self.dashboard_view.refresh()
        elif row == 1:
            self.eleves_view.refresh()