INSERT INTO City(cname, state) VALUE ('Jersey City', 'New Jersey');
INSERT INTO Users(email, pword, fname, lname, street_addr, cid, uprofile, photo) 
VALUE ('zl1477@outlook.com', 'pword', 'Vin', 'Liu', '110 1st st', 
	(SELECT cid FROM city WHERE cname = 'Jersey City' AND cstate='New Jersey'), 'Hi there!', NULL);