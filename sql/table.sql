CREATE TABLE marcher (
    idMarcher TEXT(255) PRIMARY KEY,
    nomMarcher TEXT(255),
    prixLocation CURRENCY NOT NULL
);

CREATE TABLE box (
    idBox TEXT(255) PRIMARY KEY,
    nomBox TEXT(255),
    longueur DOUBLE,
    largeur DOUBLE
);

CREATE TABLE marcher_box (
    idBox TEXT(255),
    idMarcher TEXT(255),
    CONSTRAINT PK_marcher_box PRIMARY KEY (idBox, idMarcher),
    CONSTRAINT FK_marcher FOREIGN KEY (idMarcher) REFERENCES marcher(idMarcher),
    CONSTRAINT FK_box FOREIGN KEY (idBox) REFERENCES box(idBox)
);
CREATE TABLE payement_box (
    idPayement AUTOINCREMENT PRIMARY KEY,  
    idBox TEXT(255),
    mois INTEGER,
    annee INTEGER,
    datePayement DATE,
    CONSTRAINT FK_payement_box FOREIGN KEY (idBox) REFERENCES box(idBox)
);

CREATE TABLE marcher_reduction (
    idMarcher TEXT(255),
    reduction CURRENCY,
    mois INTEGER,
    annee INTEGER,
    CONSTRAINT PK_marcher_reduction PRIMARY KEY (idMarcher, mois, annee),
    CONSTRAINT FK_marcher_reduction FOREIGN KEY (idMarcher) REFERENCES marcher(idMarcher)
);
