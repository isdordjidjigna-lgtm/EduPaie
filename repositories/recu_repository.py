"""Repository : accès aux données de la table `recu`."""
from datetime import datetime
from typing import Optional

from database.database import Database
from models.recu import Recu


class RecuRepository:
    def __init__(self, db: Database):
        self.db = db

    def _row_to_recu(self, row) -> Recu:
        return Recu(
            id=row["id"],
            numero=row["numero"],
            paiement_id=row["paiement_id"],
            date_emission=row["date_emission"],
            solde_avant=row["solde_avant"],
            solde_apres=row["solde_apres"],
            eleve_nom_snapshot=row["eleve_nom_snapshot"],
            eleve_prenom_snapshot=row["eleve_prenom_snapshot"],
            eleve_classe_snapshot=row["eleve_classe_snapshot"],
            eleve_annee_snapshot=row["eleve_annee_snapshot"],
            nb_impressions=row["nb_impressions"],
        )

    def get(self, recu_id: int) -> Optional[Recu]:
        row = self.db.conn.execute(
            "SELECT * FROM recu WHERE id = ?", (recu_id,)
        ).fetchone()
        return self._row_to_recu(row) if row else None

    def get_par_paiement(self, paiement_id: int) -> Optional[Recu]:
        row = self.db.conn.execute(
            "SELECT * FROM recu WHERE paiement_id = ?", (paiement_id,)
        ).fetchone()
        return self._row_to_recu(row) if row else None

    def lister_par_eleve(self, eleve_id: int) -> list[Recu]:
        rows = self.db.conn.execute(
            "SELECT r.* FROM recu r "
            "JOIN paiement p ON p.id = r.paiement_id "
            "WHERE p.eleve_id = ? "
            "ORDER BY r.date_emission, r.id",
            (eleve_id,),
        ).fetchall()
        return [self._row_to_recu(r) for r in rows]

    def prochain_numero(self) -> str:
        """Génère un numéro au format REC-AAAA-NNNNNN."""
        annee = datetime.now().year
        row = self.db.conn.execute(
            "SELECT COUNT(*) AS n FROM recu WHERE numero LIKE ?",
            (f"REC-{annee}-%",),
        ).fetchone()
        seq = row["n"] + 1
        return f"REC-{annee}-{seq:06d}"

    def insert(self, numero: str, paiement_id: int, date_emission: str,
               solde_avant: float, solde_apres: float,
               eleve_nom_snapshot: str, eleve_prenom_snapshot: str,
               eleve_classe_snapshot: str, eleve_annee_snapshot: str) -> int:
        with self.db.transaction() as c:
            cur = c.execute(
                "INSERT INTO recu(numero, paiement_id, date_emission, "
                "solde_avant, solde_apres, "
                "eleve_nom_snapshot, eleve_prenom_snapshot, "
                "eleve_classe_snapshot, eleve_annee_snapshot) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (numero, paiement_id, date_emission,
                 solde_avant, solde_apres,
                 eleve_nom_snapshot, eleve_prenom_snapshot,
                 eleve_classe_snapshot, eleve_annee_snapshot),
            )
            return cur.lastrowid

    def incrementer_impressions(self, recu_id: int) -> None:
        with self.db.transaction() as c:
            c.execute(
                "UPDATE recu SET nb_impressions = nb_impressions + 1 WHERE id = ?",
                (recu_id,),
            )