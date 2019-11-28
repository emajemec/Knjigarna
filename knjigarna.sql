--
-- File generated with SQLiteStudio v3.2.1 on cet. nov. 28 09:26:46 2019
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: izdaja
CREATE TABLE izdaja (
    id INTEGER PRIMARY KEY, 
    knjiga INTEGER REFERENCES knjiga(id), 
    zalo�ba INTEGER REFERENCES zalo�ba(id), 
    �t_strani INTEGER, 
    leto INTEGER, 
    cena REAL,
    vezava CHARACTER CHECK (vezava IN ('T', 'M', 'S')),
    jezik INTEGER REFERENCES jezik(id)
);

-- Table: je_ocenil
CREATE TABLE je_ocenil (
    id_knjige INTEGER REFERENCES knjiga(id),
    ocena INTEGER,
    komentar TEXT,
    cas DATE,
    uporabnik INTEGER REFERENCES uporabnik(id) 
);

-- Table: jezik
CREATE TABLE jezik (
    id INTEGER,
    jezik TEXT
);

-- Table: vezava
CREATE TABLE vezava (
    id  INTEGER PRIMARY KEY,
    ime TEXT
);

-- Table: knjiga
CREATE TABLE knjiga (
    id INTEGER PRIMARY KEY,
    naslov TEXT,
    �anr INTEGER REFERENCES �anr(id),
    opis TEXT
);

-- Table: oseba
CREATE TABLE oseba (
    id INTEGER PRIMARY KEY,
    ime TEXT,
    �ivljenjepis TEXT
);

-- Table: pripada
CREATE TABLE pripada (
    knjiga INTEGER REFERENCES izvod(id),
    oseba INTEGER REFERENCES oseba(id),
    tip CHARACTER CHECK (tip IN ('O', 'P'))
);

-- Table: uporabnik
CREATE TABLE uporabnik (
    id INTEGER,
    ime TEXT,
    email TEXT 
);


-- Table: zalo�ba
CREATE TABLE zalo�ba (
    id INTEGER,
    ime TEXT
);

-- Table: �anr
CREATE TABLE �anr (
    id INTEGER REFERENCES knjiga(id),
    ime TEXT
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
