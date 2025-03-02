INSERT INTO marcher (idMarcher, nomMarcher, prixLocation ,x , y , longueur , largeur) VALUES ('ALLEAS', 'Marché Central', 200 , 0 , 0 , 800 , 800);



INSERT INTO locataire  (idLocataire , nomLocataire) VALUES ('Loc1', 'RABARIJAONA');

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B1', 'Box A', 100, 100);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B2', 'Box B', 300, 200);

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B3', 'Box C', 35, 40);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B4', 'Box D', 34, 44);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B5', 'Box E', 30, 50);

INSERT INTO locataire_box  (idLocataire , idBox) VALUES ('Loc1', 'B1');
INSERT INTO locataire_box  (idLocataire , idBox) VALUES ('Loc1', 'B2');
INSERT INTO locataire_box  (idLocataire , idBox) VALUES ('Loc1', 'B3');
INSERT INTO locataire_box  (idLocataire , idBox) VALUES ('Loc1', 'B4');
INSERT INTO locataire_box  (idLocataire , idBox) VALUES ('Loc1', 'B5');


INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B1', 'ALLEAS');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B2', 'ALLEAS');






