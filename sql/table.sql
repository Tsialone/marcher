CREATE TABLE marcher (
    idMarcher TEXT(255) PRIMARY KEY,
    nomMarcher TEXT(255),
    prixLocation CURRENCY NOT NULL,
    x INTEGER   NOT NULL,
    y INTEGER NOT NULL , 
    longueur INTEGER NOT NULL,
    largeur INTEGER NOT NULL
);

CREATE TABLE box (
    idBox TEXT(255) PRIMARY KEY,
    nomBox TEXT(255),
    longueur CURRENCY,
    largeur CURRENCY
);
CREATE TABLE locataire (
    idLocataire TEXT(255) PRIMARY KEY,
    nomLocataire TEXT(255) NOT NULL 
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
    montant CURRENCY,
    datePayement DATE,
    CONSTRAINT FK_payement_box FOREIGN KEY (idBox) REFERENCES box(idBox)
);

CREATE TABLE marcher_ra (
    idMarcherRa AUTOINCREMENT PRIMARY KEY,
    idMarcher TEXT(255) NOT NULL,
    annee INTEGER NOT NULL,
    mois INTEGER NOT NULL,
    valeur CURRENCY,
    CONSTRAINT FK_marcher_ra FOREIGN KEY (idMarcher) REFERENCES marcher(idMarcher),
    CONSTRAINT UQ_marcher_ra UNIQUE (idMarcher, annee, mois)
);

CREATE TABLE contrat (
    idContrat AUTOINCREMENT PRIMARY KEY,
    idBox TEXT(255) NOT NULL,
    idLocataire TEXT(255) NOT NULL,
    moisDebut INTEGER NOT NULL,
    anneeDebut INTEGER NOT NULL,
    moisFin INTEGER NOT NULL,
    anneeFin INTEGER NOT NULL,
    dateSignature DATE,
    CONSTRAINT FK_contrat_box FOREIGN KEY (idBox) REFERENCES box(idBox),
    CONSTRAINT FK_contrat_locataire FOREIGN KEY (idLocataire) REFERENCES locataire(idLocataire)
);

