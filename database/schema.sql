PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS eleve (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT    NOT NULL,
    prenom          TEXT    NOT NULL,
    classe          TEXT    NOT NULL,
    annee_scolaire  TEXT    NOT NULL,
    montant_total   REAL    NOT NULL CHECK (montant_total >= 0),
    date_creation   TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(nom, prenom, classe, annee_scolaire)
);

CREATE TABLE IF NOT EXISTS paiement (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eleve_id        INTEGER NOT NULL,
    montant         REAL    NOT NULL CHECK (montant > 0),
    date_paiement   TEXT    NOT NULL,
    mode_paiement   TEXT    NOT NULL
                    CHECK (mode_paiement IN ('espèces','chèque','virement','mobile_money')),
    FOREIGN KEY (eleve_id) REFERENCES eleve(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recu (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    numero                 TEXT    NOT NULL UNIQUE,
    paiement_id            INTEGER NOT NULL UNIQUE,
    date_emission          TEXT    NOT NULL,
    solde_avant            REAL    NOT NULL,
    solde_apres            REAL    NOT NULL,
    eleve_nom_snapshot     TEXT    NOT NULL,
    eleve_prenom_snapshot  TEXT    NOT NULL,
    eleve_classe_snapshot  TEXT    NOT NULL,
    eleve_annee_snapshot   TEXT    NOT NULL,
    nb_impressions         INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (paiement_id) REFERENCES paiement(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_paiement_eleve ON paiement(eleve_id);
CREATE INDEX IF NOT EXISTS idx_eleve_classe    ON eleve(classe);
CREATE INDEX IF NOT EXISTS idx_recu_numero     ON recu(numero);