"""Fenêtre principale : sidebar + navigation + page active."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QMessageBox,
    QListWidget, QListWidgetItem, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ui.dashboard import DashboardView
from ui.eleves import ElevesView
from ui.decorators import safe_slot


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

        # --- Sidebar ---
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #263238;
                color: white;
                border: none;
                font-size: 12pt;
                padding-top: 20px;
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
        titre_sidebar = QLabel("EDUPAIE")
        titre_sidebar.setAlignment(Qt.AlignCenter)
        titre_sidebar.setStyleSheet(
            "color: white; font-size: 20pt; font-weight: bold; "
            "background-color: #1A2327; padding: 20px;"
        )

        # --- Contenu empilé ---
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

        # --- Layout ---
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, stretch=1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Signaux ---
        self.sidebar.currentRowChanged.connect(self._on_sidebar_change)
        self.sidebar.setCurrentRow(0)

        # --- Barre de statut ---
        self.statusBar().showMessage("Prêt")

    def _on_sidebar_change(self, row):
        self.stack.setCurrentIndex(row)
        # Rafraîchir la vue affichée
        if row == 0:
            self.dashboard_view.refresh()
        elif row == 1:
            self.eleves_view.refresh()