"""Point d'entrée de l'application EduPaie."""
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from database.database import Database
from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from repositories.recu_repository import RecuRepository
from services.eleve_service import EleveService
from services.paiement_service import PaiementService
from services.recu_service import RecuService
from services.pdf_generator import PDFGenerator
from ui.main_window import MainWindow


def excepthook(exc_type, exc_value, exc_tb):
    """Filet de sécurité global : aucune exception ne doit faire planter l'app."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return

    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    with open("edupaie_errors.log", "a", encoding="utf-8") as f:
        f.write(tb + "\n" + "-" * 60 + "\n")

    QMessageBox.critical(
        None,
        "Erreur inattendue",
        f"Une erreur est survenue :\n{exc_value}\n\n"
        "Le détail a été écrit dans edupaie_errors.log."
    )


def main():
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    app.setApplicationName("EduPaie")

    # QSS global — styles des boutons et de la sidebar
    app.setStyleSheet("""
        QFrame#sidebar {
            background-color: #263238;
        }
        QPushButton#sidebarBtn {
            background-color: #263238;
            color: white;
            text-align: left;
            padding: 15px 20px;
            border: none;
            border-bottom: 1px solid #37474F;
            font-size: 12pt;
        }
        QPushButton#sidebarBtn:hover {
            background-color: #37474F;
        }
        QPushButton#sidebarBtn:checked {
            background-color: #1976D2;
            border-left: 4px solid #0D47A1;
            font-weight: bold;
        }
        QPushButton#sidebarBtn:focus {
            outline: none;
            border: none;
        }

        QPushButton.actionBtn {
            background-color: #1976D2;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton.actionBtn:hover {
            background-color: #2196F3;
        }
        QPushButton.actionBtn:pressed {
            background-color: #0D47A1;
        }

        QPushButton.dangerBtn {
            background-color: #D32F2F;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton.dangerBtn:hover {
            background-color: #E53935;
        }
        QPushButton.dangerBtn:pressed {
            background-color: #B71C1C;
        }

        QPushButton.secondaryBtn {
            background-color: #607D8B;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
        }
        QPushButton.secondaryBtn:hover {
            background-color: #78909C;
        }

        QPushButton.payBtn {
            background-color: #388E3C;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton.payBtn:hover {
            background-color: #43A047;
        }
        QPushButton.payBtn:pressed {
            background-color: #2E7D32;
        }
    """)

    # 1. Base de données
    db = Database("edupaie.db")
    try:
        db.init_schema("database/schema.sql")
    except Exception:
        pass  # les tables existent déjà

    # 2. Repositories
    eleve_repo = EleveRepository(db)
    paiement_repo = PaiementRepository(db)
    recu_repo = RecuRepository(db)

    # 3. Services
    eleve_service = EleveService(eleve_repo, paiement_repo)
    paiement_service = PaiementService(
        db, eleve_repo, paiement_repo, recu_repo
    )
    recu_service = RecuService(recu_repo, paiement_repo)
    pdf_generator = PDFGenerator()

    # 4. Fenêtre principale
    window = MainWindow(
        eleve_service, paiement_service,
        recu_service, pdf_generator
    )
    window.show()

    exit_code = app.exec()
    db.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()