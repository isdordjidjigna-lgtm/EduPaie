"""Fiche élève : infos, solde, historique des paiements, actions."""
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from ui.decorators import safe_slot
from ui.paiement_dialog import PaiementDialog


class FicheEleveDialog(QDialog):
    def __init__(self, eleve, eleve_service, paiement_service,
                 recu_service, pdf_generator, parent=None):
        super().__init__(parent)
        self.eleve = eleve
        self.eleve_service = eleve_service
        self.paiement_service = paiement_service
        self.recu_service = recu_service
        self.pdf_generator = pdf_generator

        self.setWindowTitle(f"Fiche élève — {eleve.nom} {eleve.prenom}")
        self.setMinimumSize(750, 550)

        self.info_label = QLabel()
        self.info_label.setTextFormat(Qt.RichText)
        self._maj_infos()

        self.btn_payer = QPushButton("➕ Enregistrer un paiement")
        self.btn_payer.clicked.connect(self._on_payer)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["N° reçu", "Date", "Montant", "Mode", "Solde après", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.btn_fermer = QPushButton("Fermer")
        self.btn_fermer.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label)
        layout.addWidget(self.btn_payer)
        layout.addWidget(QLabel("<b>Historique des paiements</b>"))
        layout.addWidget(self.table)

        bas = QHBoxLayout()
        bas.addStretch()
        bas.addWidget(self.btn_fermer)
        layout.addLayout(bas)

        self._charger_historique()

    def _maj_infos(self):
        eleve = self.eleve
        solde = self.eleve_service.calculer_solde(eleve.id)
        paye = eleve.montant_total - solde
        statut = self.eleve_service.statut(eleve.id)

        couleur = {
            "Soldé": "green",
            "Partiellement payé": "orange",
            "Non payé": "red",
        }.get(statut, "black")

        self.info_label.setText(f"""
        <h2>{eleve.nom} {eleve.prenom}</h2>
        <table>
            <tr><td><b>Classe :</b></td><td>{eleve.classe}</td></tr>
            <tr><td><b>Annee scolaire :</b></td><td>{eleve.annee_scolaire}</td></tr>
            <tr><td><b>Frais totaux :</b></td><td>{eleve.montant_total:,.0f} FCFA</td></tr>
            <tr><td><b>Total paye :</b></td><td>{paye:,.0f} FCFA</td></tr>
            <tr><td><b>Solde restant :</b></td><td><b>{solde:,.0f} FCFA</b></td></tr>
            <tr><td><b>Statut :</b></td>
                <td><span style='color:{couleur}'><b>{statut}</b></span></td></tr>
        </table>
        """.replace(",", " "))

    def _charger_historique(self):
        self.table.setRowCount(0)
        recus = self.recu_service.lister_par_eleve(self.eleve.id)
        self.table.setRowCount(len(recus))

        for row, recu in enumerate(recus):
            paiement = self.paiement_service.paiement_repo.get(recu.paiement_id)
            if paiement is None:
                continue

            self.table.setItem(row, 0, QTableWidgetItem(recu.numero))
            self.table.setItem(row, 1, QTableWidgetItem(paiement.date_paiement))
            self.table.setItem(row, 2, QTableWidgetItem(
                f"{paiement.montant:,.0f}".replace(",", " ")
            ))
            self.table.setItem(row, 3, QTableWidgetItem(paiement.mode_paiement))
            self.table.setItem(row, 4, QTableWidgetItem(
                f"{recu.solde_apres:,.0f}".replace(",", " ")
            ))

            btn = QPushButton("Revoir")
            btn.clicked.connect(
                lambda _, rid=recu.id: self._reimprimer(rid)
            )
            self.table.setCellWidget(row, 5, btn)

    @safe_slot
    def _on_payer(self):
        dialog = PaiementDialog(
            self.eleve, self.paiement_service, self.eleve_service, self
        )
        if dialog.exec():
            self._maj_infos()
            self._charger_historique()

            if dialog.recu_id:
                data = self.recu_service.donnees_pour_pdf(dialog.recu_id)
                chemin = f"recus/{data['numero']}.pdf"
                self.pdf_generator.generer_recu(data, chemin)
                self.recu_service.marquer_imprime(dialog.recu_id)

    @safe_slot
    def _reimprimer(self, recu_id: int):
        data = self.recu_service.donnees_pour_pdf(recu_id)
        chemin = f"recus/{data['numero']}.pdf"

        self.pdf_generator.generer_recu(data, chemin)
        self.recu_service.marquer_imprime(recu_id)

        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(chemin)))

        self._charger_historique()