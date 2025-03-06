INSERT INTO marcher (idMarcher, nomMarcher, prixLocation ,x , y , longueur , largeur) VALUES ('Behoririka', 'Marché Central', 20000 , 0 , 0 ,340, 500 );
INSERT INTO marcher (idMarcher, nomMarcher, prixLocation ,x , y , longueur , largeur) VALUES ('Analakely', 'Marché Central', 13000 , 10 , 350 ,250 , 200);

INSERT INTO locataire  (idLocataire , nomLocataire) VALUES ('Loc1', 'RABARIJAONA');
INSERT INTO locataire  (idLocataire , nomLocataire) VALUES ('Loc2', 'ROMANIA');

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B1', 'Box A', 100, 100);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B2', 'Box B', 300, 200);

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B3', 'Box C', 220, 40);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B4', 'Box D', 30, 400);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B5', 'Box E', 30, 50);

INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B1', 'Behoririka');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B2', 'Behoririka');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B3', 'Analakely');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B4', 'Behoririka');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B5', 'Analakely');





INSERT INTO marcher_ra (idMarcher, annee, mois, valeur) VALUES ('Behoririka', 2024, 1, 500000);
INSERT INTO marcher_ra (idMarcher, annee, mois, valeur) VALUES ('Behoririka', 2024, 9, 450000);
INSERT INTO marcher_ra (idMarcher, annee, mois, valeur) VALUES ('Analakely', 2024, 7, 300000);
INSERT INTO marcher_ra (idMarcher, annee, mois, valeur) VALUES ('Analakely', 2024, 4, 280000);












