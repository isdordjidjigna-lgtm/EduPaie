"""Fenêtre principale : sidebar + navigation + titre de page."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget, QPushButton, QButtonGroup, QFrame
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
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)

        # Logo / titre sidebar
        self.logo = QLabel("EduPaie")
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet(
            "color: white; font-size: 20pt; font-weight: bold; "
            "padding: 20px; background-color: #1a2327;"
        )

        # Boutons de navigation
        self.btn_dashboard = self._creer_bouton_sidebar("📊  Tableau de bord")
        self.btn_eleves    = self._creer_bouton_sidebar("👥  Élèves")

        # Groupe exclusif : un seul bouton coché à la fois
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.nav_group.addButton(self.btn_dashboard, 0)
        self.nav_group.addButton(self.btn_eleves, 1)

        # Layout de la sidebar
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar_layout.addWidget(self.logo)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_eleves)
        sidebar_layout.addStretch()

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
        layout.addWidget(self.sidebar)
        layout.addWidget(conteneur_droite, stretch=1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ============================
        # SIGNAUX
        # ============================
        self.nav_group.idClicked.connect(self._on_sidebar_change)
        self.btn_dashboard.setChecked(True)   # page par défaut

        self.statusBar().showMessage("Prêt")

    def _creer_bouton_sidebar(self, texte):
        """Crée un bouton de sidebar coché/non coché."""
        btn = QPushButton(texte)
        btn.setObjectName("sidebarBtn")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def _on_sidebar_change(self, row):
        """Change la page affichée et met à jour le titre."""
        self.stack.setCurrentIndex(row)

        titres = {
            0: "Tableau de bord",
            1: "Gestion des élèves",
        }
        self.titre_page.setText(titres.get(row, "EduPaie"))

        if row == 0:
            self.dashboard_view.refresh()
        elif row == 1:
            self.eleves_view.refresh()