DELETE FROM Hood;
ALTER TABLE `projectdb`.`Hood` 
AUTO_INCREMENT = 1 ;
INSERT INTO Hood(hname, sw_lat, sw_lng, ne_lat, ne_lng, hpopulation) VALUES
('East Village', 0, 0, 0, 0, 500),
('West Village', 0, 0, 0, 0, 400),
('Financial District', 0, 0, 0, 0, 300),
('Two Bridges', 0, 0, 0, 0, 100),
('SoHo', 0, 0, 0, 0, 400),
('Bowery', 0, 0, 0, 0, 2),
('Brooklyn Heights', 0, 0, 0, 0, 1000),
('Grove Street', 0, 0, 0, 0, 300),
('Newport', 0, 0, 0, 0, 1),
('Downtown Newark', 0, 0, 0, 0, 500);
SELECT * FROM Hood;