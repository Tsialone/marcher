INSERT INTO marcher (idMarcher, nomMarcher, prixLocation) VALUES ('M1', 'Marché Central', 150.00);
INSERT INTO marcher (idMarcher, nomMarcher, prixLocation) VALUES ('M2', 'Marché Nord', 120.00);
INSERT INTO marcher (idMarcher, nomMarcher, prixLocation) VALUES ('M3', 'Marché Sud', 100.00);

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B1', 'Box A', 5.00, 3.00);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B2', 'Box B', 4.00, 2.50);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B3', 'Box C', 6.00, 4.00);

INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B1', 'M1');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B2', 'M1');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B3', 'M2');

INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M1', 10.00, 1, 2023);
INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M1', 15.00, 2, 2023);
INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M2', 20.00, 1, 2023);
