--
-- File generated with SQLiteStudio v3.0.3 on pon. nov. 18 10:49:29 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: izvod
CREATE TABLE izvod (
    id INTEGER PRIMARY KEY, 
    knjiga INTEGER REFERENCES knjiga(id), 
    založba INTEGER REFERENCES založba(id), 
    št_strani INTEGER, 
    leto INTEGER, 
    cena REAL,
    vezava TEXT REFERENCES vezava(oznaka),
    jezik INTEGER REFERENCES jezik(id)
);

-- Table: pripada
CREATE TABLE pripada (
    knjiga INTEGER REFERENCES izvod(id),
    oseba INTEGER REFERENCES oseba(id),
    tip CHARACTER CHECK (tip IN ('O', 'P'))
);

-- Table: oseba
CREATE TABLE oseba (
    id INTEGER PRIMARY KEY,
    ime TEXT,
    življenjepis TEXT
);

-- Table: oseba
CREATE TABLE oseba (
    id  INTEGER PRIMARY KEY,
    ime TEXT
);

-- Table: knjiga
CREATE TABLE knjiga (
    id INTEGER PRIMARY KEY,
    naslov TEXT,
    žanr INTEGER REFERENCES žanr(id),
    opis TEXT
);

-- Table: jezik
CREATE TABLE jezik (
    id INTEGER,
    jezik TEXT
);

-- Table: založba
CREATE TABLE založba (
    id INTEGER,
    ime TEXT
);

-- Table: vezava
CREATE TABLE vezava (
    oznaka CHARACTER CHECK (tip IN ('T', 'M', 'S')),
    vezano TEXT
);

-- Table: uporabnik
CREATE TABLE uporabnik (
    id INTEGER,
    ime TEXT,
    email TEXT 
);

-- Table: je_ocenil
CREATE TABLE je_ocenil (
    id_knjige INTEGER REFERENCES knjiga(id),
    ocena INTEGER,
    komentar TEXT,
    čas DATE,
    uporabnik INTEGER REFERENCES uporabnik(id) 
);


COMMIT TRANSACTION;
