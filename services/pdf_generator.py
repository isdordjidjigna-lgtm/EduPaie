"""Génération du reçu PDF avec ReportLab."""
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def fmt_montant(montant: float) -> str:
    """Formate un montant en FCFA avec séparateur d'espace."""
    return f"{montant:,.0f} FCFA".replace(",", " ")


class PDFGenerator:
    def __init__(self, nom_etablissement: str = "ÉCOLE LES CHAMPIONS",
                 telephone: str = "+228 90 00 00 00",
                 adresse: str = "Lomé, Togo"):
        self.nom = nom_etablissement
        self.telephone = telephone
        self.adresse = adresse

    def generer_recu(self, data: dict, chemin: str) -> str:
        """Génère un PDF de reçu.

        data doit contenir :
            numero, date_emission, nom, prenom, classe, annee,
            montant, mode, date_paiement, solde_avant, solde_apres,
            nb_impressions
        """
        Path(chemin).parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(chemin, pagesize=A4)
        W, H = A4

        # --- En-tête établissement ---
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(W / 2, H - 20 * mm, self.nom)

        c.setFont("Helvetica", 9)
        c.drawCentredString(W / 2, H - 26 * mm, f"Tél : {self.telephone}")
        c.drawCentredString(W / 2, H - 31 * mm, f"Adresse : {self.adresse}")

        # Ligne de séparation
        c.line(20 * mm, H - 35 * mm, W - 20 * mm, H - 35 * mm)

        # --- Titre ---
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(W / 2, H - 45 * mm, "REÇU DE PAIEMENT")

        # --- Numéro + date d'émission ---
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20 * mm, H - 58 * mm, f"N° reçu : {data['numero']}")

        c.setFont("Helvetica", 9)
        date_em = data.get("date_emission", "")
        if date_em:
            date_em = date_em.replace("T", " à ")[:19]
        c.drawString(20 * mm, H - 64 * mm, f"Émis le : {date_em}")

        # Mention réimpression
        if data.get("nb_impressions", 0) > 0:
            c.setFillColorRGB(0.8, 0, 0)
            c.setFont("Helvetica-Bold", 9)
            c.drawRightString(
                W - 20 * mm, H - 58 * mm,
                f"⚠ Réimprimé le {datetime.now().strftime('%d/%m/%Y')}"
            )
            c.setFillColorRGB(0, 0, 0)

        # --- Infos élève ---
        y = H - 80 * mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20 * mm, y, "Élève :")
        c.setFont("Helvetica", 11)
        c.drawString(50 * mm, y, f"{data['nom']} {data['prenom']}")

        y -= 7 * mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20 * mm, y, "Classe :")
        c.setFont("Helvetica", 11)
        c.drawString(50 * mm, y, f"{data['classe']} — {data['annee']}")

        # --- Détail du paiement ---
        y -= 15 * mm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, "Détail du versement")
        c.line(20 * mm, y - 2 * mm, W - 20 * mm, y - 2 * mm)

        y -= 12 * mm
        c.setFont("Helvetica", 11)
        c.drawString(20 * mm, y, "Montant payé :")
        c.drawRightString(W - 20 * mm, y, fmt_montant(data["montant"]))

        y -= 7 * mm
        c.drawString(20 * mm, y, "Mode de paiement :")
        c.drawRightString(W - 20 * mm, y, str(data["mode"]).capitalize())

        y -= 7 * mm
        c.drawString(20 * mm, y, "Date du paiement :")
        c.drawRightString(W - 20 * mm, y, str(data.get("date_paiement", "")))

        # --- Soldes ---
        y -= 15 * mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20 * mm, y, "Solde avant ce paiement :")
        c.drawRightString(W - 20 * mm, y, fmt_montant(data["solde_avant"]))

        y -= 8 * mm
        c.drawString(20 * mm, y, "Solde restant après ce paiement :")
        c.drawRightString(W - 20 * mm, y, fmt_montant(data["solde_apres"]))

        # --- Mention SOLDÉ ---
        if abs(data["solde_apres"]) < 0.01:
            y -= 15 * mm
            c.setFillColorRGB(0, 0.5, 0)
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(W / 2, y, "★ SOLDÉ ★")
            c.setFillColorRGB(0, 0, 0)

        # --- Pied de page ---
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(
            20 * mm, 25 * mm,
            "Ce reçu ne vaut que revêtu du cachet et de la signature de l'établissement."
        )
        c.drawString(
            20 * mm, 20 * mm,
            "Document généré électroniquement — peut être réimprimé à l'identique."
        )

        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(W - 20 * mm, 25 * mm, "Signature / Cachet")

        c.showPage()
        c.save()
        return chemin