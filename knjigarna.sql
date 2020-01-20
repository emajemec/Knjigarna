--
-- File generated with SQLiteStudio v3.2.1 on pon. jan. 20 10:30:15 2020
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: avtorji
DROP TABLE IF EXISTS avtorji;

CREATE TABLE avtorji (
    id          INTEGER PRIMARY KEY,
    ime         TEXT,
    srednje_ime TEXT,
    priimek     TEXT
);


-- Table: knjiga
DROP TABLE IF EXISTS knjiga;

CREATE TABLE knjiga (
    id        INTEGER PRIMARY KEY,
    naslov    TEXT,
    st_strani INTEGER,
    ocena     FLOAT,
    isbn      INTEGER,
    datum     DATE,
    zalozba   INTEGER REFERENCES zalozba (id) 
);


-- Table: pripada
DROP TABLE IF EXISTS pripada;

CREATE TABLE pripada (
    knjiga INTEGER REFERENCES knjiga (id),
    avtor  INTEGER REFERENCES avtorji (id) 
);


-- Table: pripada_zanr
DROP TABLE IF EXISTS pripada_zanr;

CREATE TABLE pripada_zanr (
    knjiga INTEGER REFERENCES knjiga (id),
    zanr   INTEGER REFERENCES zanr (id) 
);


-- Table: uporabnik
DROP TABLE IF EXISTS uporabnik;

CREATE TABLE uporabnik (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ime       TEXT    NOT NULL
                      UNIQUE,
    zgostitev TEXT    NOT NULL,
    sol       TEXT    NOT NULL
);


-- Table: zalozba
DROP TABLE IF EXISTS zalozba;

CREATE TABLE zalozba (
    id  INTEGER PRIMARY KEY,
    ime TEXT
);


-- Table: zanr
DROP TABLE IF EXISTS zanr;

CREATE TABLE zanr (
    id      INTEGER PRIMARY KEY,
    ime     TEXT,
    nadzanr INTEGER REFERENCES zanr (id) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
