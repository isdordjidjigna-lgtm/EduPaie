"""Peuplement de la base edupaie.db avec 15 eleves et un historique varie."""
from datetime import datetime, timedelta

from database.database import Database
from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from repositories.recu_repository import RecuRepository


ELEVES = [
    ("Kossi",    "Afi",     "3eme A", 200_000, [(200_000, 90, "espèces")]),
    ("Mensah",   "Kodjo",   "3eme A", 250_000, [(100_000, 120, "espèces"),
                                                (100_000,  80, "mobile_money"),
                                                ( 50_000,  40, "virement")]),
    ("Ama",      "Dodji",   "3eme B", 180_000, [(100_000, 100, "chèque"),
                                                ( 80_000,  60, "espèces")]),
    ("Sossou",   "Akoua",   "3eme B", 220_000, [(220_000,  75, "virement")]),
    ("Togo",     "Yawa",    "3eme C", 300_000, [(100_000, 130, "espèces"),
                                                (100_000, 100, "mobile_money"),
                                                ( 50_000,  70, "espèces"),
                                                ( 50_000,  35, "chèque")]),
    ("Adjovi",   "Sena",    "4eme A", 200_000, [(100_000,  95, "espèces"),
                                                ( 80_000,  50, "mobile_money")]),
    ("Kouassi",  "Yao",     "4eme A", 250_000, [(100_000, 110, "virement"),
                                                ( 75_000,  70, "espèces"),
                                                ( 50_000,  30, "chèque")]),
    ("Diop",     "Aminata", "4eme B", 180_000, [( 50_000, 100, "espèces"),
                                                ( 40_000,  60, "mobile_money")]),
    ("Nkrumah",  "Kwame",   "4eme B", 220_000, [(110_000,  85, "virement")]),
    ("Lawson",   "Ayaba",   "5eme A", 150_000, [( 30_000,  45, "espèces")]),
    ("Bodjona",  "Komi",    "5eme A", 200_000, [( 20_000,  70, "espèces"),
                                                ( 20_000,  35, "mobile_money")]),
    ("Zinsou",   "Sonia",   "5eme B", 250_000, []),
    ("Agbeko",   "Messan",  "5eme B", 180_000, []),
    ("Folly",    "Rita",    "6eme A", 150_000, []),
    ("Amegan",   "Kofi",    "6eme A", 150_000, []),
]

ANNEE_SCOLAIRE = "2025-2026"


def main():
    db = Database("edupaie.db")
    db.init_schema("database/schema.sql")

    eleve_repo = EleveRepository(db)
    paiement_repo = PaiementRepository(db)
    recu_repo = RecuRepository(db)

    aujourdhui = datetime.now()
    total_paiements = 0

    for nom, prenom, classe, total_du, paiements in ELEVES:
        eleve_id = eleve_repo.insert(
            nom=nom, prenom=prenom, classe=classe,
            annee_scolaire=ANNEE_SCOLAIRE, montant_total=total_du,
        )

        solde = total_du
        for montant, jours_avant, mode in paiements:
            date_paiement = (aujourdhui - timedelta(days=jours_avant)).strftime("%Y-%m-%d")

            paiement_id = paiement_repo.insert(
                eleve_id=eleve_id,
                montant=montant,
                date_paiement=date_paiement,
                mode_paiement=mode,
            )

            numero = recu_repo.prochain_numero()
            solde_avant = solde
            solde -= montant

            recu_repo.insert(
                numero=numero,
                paiement_id=paiement_id,
                date_emission=(aujourdhui - timedelta(days=jours_avant)).isoformat(timespec="seconds"),
                solde_avant=round(solde_avant, 2),
                solde_apres=round(solde, 2),
                eleve_nom_snapshot=nom,
                eleve_prenom_snapshot=prenom,
                eleve_classe_snapshot=classe,
                eleve_annee_snapshot=ANNEE_SCOLAIRE,
            )
            total_paiements += 1

    db.close()
    print(f"OK Base edupaie.db peuplee : {len(ELEVES)} eleves.")
    print(f"   -> {total_paiements} paiements enregistres.")
    print(f"   -> {total_paiements} recus emis.")


if __name__ == "__main__":
    main()