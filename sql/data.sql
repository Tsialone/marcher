INSERT INTO marcher (idMarcher, nomMarcher, prixLocation ,x , y , longueur , largeur) VALUES ('M1', 'Marché Central', 150.00 , 10 , 15 , 100 , 120);
INSERT INTO marcher (idMarcher, nomMarcher, prixLocation, x ,y , longueur , largeur) VALUES ('M2', 'Marché Nord', 120.00 , 480 , 10 , 100 , 200);
INSERT INTO marcher (idMarcher, nomMarcher, prixLocation, x ,y , longueur , largeur) VALUES ('M3', 'Marché Sud', 100.00 , 20 , 200 , 70 , 500);

INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B1', 'Box A', 20, 29);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B2', 'Box B', 10, 40);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B3', 'Box C', 35, 40);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B4', 'Box D', 34, 44);
INSERT INTO box (idBox, nomBox, longueur, largeur) VALUES ('B5', 'Box E', 30, 50);



INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B1', 'M1');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B2', 'M1');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B3', 'M2');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B4', 'M1');
INSERT INTO marcher_box (idBox, idMarcher) VALUES ('B5', 'M3');



INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M1', 10.00, 1, 2023);
INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M1', 15.00, 2, 2023);
INSERT INTO marcher_reduction (idMarcher, reduction, mois, annee) VALUES ('M2', 20.00, 1, 2023);

