--
-- File generated with SQLiteStudio v3.2.1 on čet. jan. 16 09:54:07 2020
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
    št_strani INTEGER,
    ocena     FLOAT,
    isbn      INTEGER,
    datum     DATE,
    zalozba   INTEGER REFERENCES založba (id) 
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


-- Table: založba
DROP TABLE IF EXISTS založba;

CREATE TABLE založba (
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
