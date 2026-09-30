"""Repository : accès aux données de la table `eleve`."""
from typing import Optional

from database.database import Database
from models.eleve import Eleve


class EleveRepository:
    def __init__(self, db: Database):
        self.db = db

    def _row_to_eleve(self, row) -> Eleve:
        return Eleve(
            id=row["id"],
            nom=row["nom"],
            prenom=row["prenom"],
            classe=row["classe"],
            annee_scolaire=row["annee_scolaire"],
            montant_total=row["montant_total"],
            date_creation=row["date_creation"],
        )

    def get(self, eleve_id: int) -> Optional[Eleve]:
        row = self.db.conn.execute(
            "SELECT * FROM eleve WHERE id = ?", (eleve_id,)
        ).fetchone()
        return self._row_to_eleve(row) if row else None

    def lister_tous(self) -> list[Eleve]:
        rows = self.db.conn.execute(
            "SELECT * FROM eleve ORDER BY classe, nom, prenom"
        ).fetchall()
        return [self._row_to_eleve(r) for r in rows]

    def lister_classes(self) -> list[str]:
        rows = self.db.conn.execute(
            "SELECT DISTINCT classe FROM eleve ORDER BY classe"
        ).fetchall()
        return [r["classe"] for r in rows]

    def insert(self, nom: str, prenom: str, classe: str,
               annee_scolaire: str, montant_total: float) -> int:
        with self.db.transaction() as c:
            cur = c.execute(
                "INSERT INTO eleve(nom, prenom, classe, annee_scolaire, montant_total) "
                "VALUES(?, ?, ?, ?, ?)",
                (nom, prenom, classe, annee_scolaire, montant_total),
            )
            return cur.lastrowid

    def update(self, eleve_id: int, nom: str, prenom: str, classe: str,
               annee_scolaire: str, montant_total: float) -> None:
        with self.db.transaction() as c:
            c.execute(
                "UPDATE eleve SET nom = ?, prenom = ?, classe = ?, "
                "annee_scolaire = ?, montant_total = ? WHERE id = ?",
                (nom, prenom, classe, annee_scolaire, montant_total, eleve_id),
            )

    def delete(self, eleve_id: int) -> None:
        with self.db.transaction() as c:
            c.execute("DELETE FROM eleve WHERE id = ?", (eleve_id,))

    def a_des_paiements(self, eleve_id: int) -> bool:
        row = self.db.conn.execute(
            "SELECT COUNT(*) AS n FROM paiement WHERE eleve_id = ?",
            (eleve_id,),
        ).fetchone()
        return row["n"] > 0