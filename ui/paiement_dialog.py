"""Dialogue d'enregistrement d'un paiement avec feedback live."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel,
    QDoubleSpinBox, QDateEdit, QComboBox, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import QDate, Qt

from services.exceptions import ValidationError, SoldeInsuffisantError


class PaiementDialog(QDialog):
    def __init__(self, eleve, paiement_service, eleve_service, parent=None):
        super().__init__(parent)
        self.eleve = eleve
        self.paiement_service = paiement_service
        self.eleve_service = eleve_service

        self.setWindowTitle(f"Paiement — {eleve.nom} {eleve.prenom}")
        self.setMinimumWidth(420)

        # Solde actuel
        self.solde_actuel = self.eleve_service.calculer_solde(eleve.id)

        # --- Champs ---
        self.montant_spin = QDoubleSpinBox()
        self.montant_spin.setMaximum(10_000_000)
        self.montant_spin.setDecimals(0)
        self.montant_spin.setSuffix(" FCFA")
        self.montant_spin.setSingleStep(5_000)
        self.montant_spin.setValue(min(self.solde_actuel, 50_000))

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMaximumDate(QDate.currentDate())

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["espèces", "chèque", "virement", "mobile_money"])

        # --- Labels info ---
        self.solde_label = QLabel()
        self.solde_label.setTextFormat(Qt.RichText)
        self._rafraichir_solde()

        self.eleve_label = QLabel(
            f"<b>{eleve.nom} {eleve.prenom}</b> — {eleve.classe}"
        )

        # --- Layout ---
        form = QFormLayout()
        form.addRow("Élève :", self.eleve_label)
        form.addRow("Solde restant :", self.solde_label)
        form.addRow("Montant à payer :", self.montant_spin)
        form.addRow("Date :", self.date_edit)
        form.addRow("Mode de paiement :", self.mode_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_valider)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        # Feedback live
        self.montant_spin.valueChanged.connect(self._rafraichir_solde)
        self.montant_spin.setFocus()
        self.montant_spin.selectAll()

        # Mémorise le recu créé
        self.recu_id = None
        self.numero_recu = None

    def _rafraichir_solde(self):
        """Met à jour l'affichage du solde restant après le paiement."""
        montant = self.montant_spin.value()
        apres = self.solde_actuel - montant
        if apres < -0.01:
            self.solde_label.setText(
                f"<span style='color:red'><b>{self.solde_actuel:,.0f} FCFA</b> "
                f"→ après : <b>{apres:,.0f}</b> ❌</span>".replace(",", " ")
            )
        else:
            self.solde_label.setText(
                f"<span style='color:green'><b>{self.solde_actuel:,.0f} FCFA</b> "
                f"→ après : <b>{apres:,.0f}</b></span>".replace(",", " ")
            )

    def _on_valider(self):
        try:
            montant = self.montant_spin.value()
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            mode = self.mode_combo.currentText()

            paiement_id, recu_id, numero = self.paiement_service.enregistrer(
                eleve_id=self.eleve.id,
                montant=montant,
                date_str=date_str,
                mode=mode,
            )
            self.recu_id = recu_id
            self.numero_recu = numero

            QMessageBox.information(
                self, "Paiement enregistré",
                f"Paiement de {montant:,.0f} FCFA enregistré.\n"
                f"Reçu N° {numero} émis.".replace(",", " ")
            )
            self.accept()

        except SoldeInsuffisantError as e:
            QMessageBox.warning(self, "Paiement refusé", str(e))
        except ValidationError as e:
            QMessageBox.warning(self, "Erreur de saisie", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur inattendue :\n{e}")