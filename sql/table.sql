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
CREATE TABLE locataire_box (
    idLocataire TEXT (255) ,
    idBox TEXT (255) ,
    CONSTRAINT PK__locataire_box PRIMARY KEY (idLocataire, idBox),
    CONSTRAINT FK_locataire FOREIGN KEY (idLocataire) REFERENCES locataire(idLocataire),
    CONSTRAINT FK_locataire_box FOREIGN KEY (idBox) REFERENCES box(idBox)
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
    CONSTRAINT FK_payement_box FOREIGN KEY (idBox) REFERENCES box(idBox),
    CONSTRAINT UC_payement UNIQUE (idBox, mois, annee) 
);

CREATE TABLE marcher_ra (
    idMarcher TEXT(255),
    raison TEXT(255),
    pourcentage CURRENCY,
    mois INTEGER,
    CONSTRAINT PK_marcher_ra PRIMARY KEY (idMarcher, mois),
    CONSTRAINT FK_marcher_ra FOREIGN KEY (idMarcher) REFERENCES marcher(idMarcher)
);

