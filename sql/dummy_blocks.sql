DELETE FROM Blocks;
ALTER TABLE `projectdb`.`Blocks` 
AUTO_INCREMENT = 1 ;
INSERT INTO Blocks(bname, sw_lat, sw_lng, ne_lat, ne_lng, bpopulation) VALUES 
('The A Building', 0, 0, 0, 0, 10),
('250 East Houston Street', 0, 0, 0, 0, 12),
('45 Christopher Street', 0, 0, 0, 0, 25),
('49 Delancy Street', 0 ,0 ,0 ,0, 2),
('Newport Center', 0, 0, 0, 0, 3),
('Cadman Plaza', 0, 0, 0, 0, 60),
('Prince Street', 0, 0, 0, 0, 110),
('Provost Square', 0, 0, 0, 0, 70),
('First Street', 0, 0, 0, 0, 80),
('Newark Avenue', 0, 0, 0, 0, 100),
('Warren Street', 0, 0, 0, 0, 10);
SELECT * FROM Blocks;