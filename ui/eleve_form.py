"""Formulaire d'ajout et de modification d'un élève."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QDoubleSpinBox, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt

from services.exceptions import ValidationError


class EleveForm(QDialog):
    """Dialogue modal pour créer ou modifier un élève.

    Utilisation :
        form = EleveForm(eleve_service)
        if form.exec() == QDialog.Accepted:
            # la création/modification a été faite
    """

    def __init__(self, eleve_service, eleve=None, parent=None):
        super().__init__(parent)
        self.eleve_service = eleve_service
        self.eleve = eleve  # None = création, sinon modification

        if eleve is None:
            self.setWindowTitle("Nouvel élève")
        else:
            self.setWindowTitle(f"Modifier — {eleve.nom} {eleve.prenom}")

        self.setMinimumWidth(400)

        # --- Champs ---
        self.nom_edit = QLineEdit()
        self.nom_edit.setPlaceholderText("Ex : Kossi")

        self.prenom_edit = QLineEdit()
        self.prenom_edit.setPlaceholderText("Ex : Afi")

        self.classe_edit = QLineEdit()
        self.classe_edit.setPlaceholderText("Ex : 3eme A")

        self.annee_edit = QLineEdit()
        self.annee_edit.setPlaceholderText("Ex : 2025-2026")
        self.annee_edit.setText("2025-2026")

        self.frais_spin = QDoubleSpinBox()
        self.frais_spin.setMaximum(10_000_000)
        self.frais_spin.setDecimals(0)
        self.frais_spin.setSuffix(" FCFA")
        self.frais_spin.setSingleStep(5_000)

        # --- Pré-remplir en modification ---
        if eleve is not None:
            self.nom_edit.setText(eleve.nom)
            self.prenom_edit.setText(eleve.prenom)
            self.classe_edit.setText(eleve.classe)
            self.annee_edit.setText(eleve.annee_scolaire)
            self.frais_spin.setValue(eleve.montant_total)

        # --- Layout ---
        form = QFormLayout()
        form.addRow("Nom :", self.nom_edit)
        form.addRow("Prénom :", self.prenom_edit)
        form.addRow("Classe :", self.classe_edit)
        form.addRow("Année scolaire :", self.annee_edit)
        form.addRow("Frais totaux :", self.frais_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_valider)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.nom_edit.setFocus()

    def _on_valider(self):
        """Valide et ferme le dialogue. Affiche un warning si erreur."""
        try:
            nom = self.nom_edit.text().strip()
            prenom = self.prenom_edit.text().strip()
            classe = self.classe_edit.text().strip()
            annee = self.annee_edit.text().strip()
            frais = self.frais_spin.value()

            if self.eleve is None:
                # Création
                self.eleve_service.creer(nom, prenom, classe, annee, frais)
            else:
                # Modification
                self.eleve_service.modifier(
                    self.eleve.id, nom, prenom, classe, annee, frais
                )

            self.accept()

        except ValidationError as e:
            QMessageBox.warning(self, "Erreur de saisie", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur inattendue :\n{e}")