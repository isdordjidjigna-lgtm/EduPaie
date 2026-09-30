"""Repository : accès aux données de la table `paiement`."""
from typing import Optional

from database.database import Database
from models.paiement import Paiement


class PaiementRepository:
    def __init__(self, db: Database):
        self.db = db

    def _row_to_paiement(self, row) -> Paiement:
        return Paiement(
            id=row["id"],
            eleve_id=row["eleve_id"],
            montant=row["montant"],
            date_paiement=row["date_paiement"],
            mode_paiement=row["mode_paiement"],
        )

    def get(self, paiement_id: int) -> Optional[Paiement]:
        row = self.db.conn.execute(
            "SELECT * FROM paiement WHERE id = ?", (paiement_id,)
        ).fetchone()
        return self._row_to_paiement(row) if row else None

    def lister_par_eleve(self, eleve_id: int) -> list[Paiement]:
        rows = self.db.conn.execute(
            "SELECT * FROM paiement WHERE eleve_id = ? "
            "ORDER BY date_paiement, id",
            (eleve_id,),
        ).fetchall()
        return [self._row_to_paiement(r) for r in rows]

    def somme_par_eleve(self, eleve_id: int) -> float:
        row = self.db.conn.execute(
            "SELECT COALESCE(SUM(montant), 0) AS s "
            "FROM paiement WHERE eleve_id = ?",
            (eleve_id,),
        ).fetchone()
        return float(row["s"])

    def insert(self, eleve_id: int, montant: float,
               date_paiement: str, mode_paiement: str) -> int:
        with self.db.transaction() as c:
            cur = c.execute(
                "INSERT INTO paiement(eleve_id, montant, date_paiement, mode_paiement) "
                "VALUES(?, ?, ?, ?)",
                (eleve_id, montant, date_paiement, mode_paiement),
            )
            return cur.lastrowid