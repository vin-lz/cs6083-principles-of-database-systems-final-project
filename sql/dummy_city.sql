DELETE FROM City;
ALTER TABLE `projectdb`.`City` 
AUTO_INCREMENT = 1 ;
INSERT INTO City(cname, cstate) VALUES
('New York', 'New York'),
('White Plains', 'New York'),
('Jersey City', 'New Jersey'),
('Yonkers', 'New York'),
('Hoboken', 'New Jersey'),
('Harrison', 'New Jersey'),
('Weehawken', 'New Jersey'),
('West New York', 'New Jersey'),
('Newark', 'New Jersey'),
('Long Beach', 'New York');
SELECT * FROM City;