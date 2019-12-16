DELETE FROM Users;
ALTER TABLE `projectdb`.`Users` 
AUTO_INCREMENT = 1;
INSERT INTO Users(email, pword, fname, lname, street_addr, cid) VALUES 
('ewaters@me.com', 'pword1', 'Shaneka', 'Franck', '110 Pikachu Rd', 1),
('okroeger@yahoo.com', 'pword1', 'Kathry', 'Grimsley', '607 Shady Court', 1),
('lstaf@comcast.net', 'pword1', 'Rochell', 'Brigance', '7477 Pearl St', 1),
('auronen@live.com', 'pword1', 'Cami', 'Silk', '56 Marvon St', 1),
('grdschl@icloud.com', 'pword1', 'Ryan', 'Dilks', '9700 Armstrong St', 3),
('inico@sbcglobal.net', 'pword1', 'Helen', 'Uresti', '3 Wentworth Dr', 3),
('harpes@outlook.com', 'pword1', 'Kylee', 'Deskins', '33 Hill St', 3),
('mrdvt@gmail.com', 'pword1', 'Cristie', 'Bonnell', '37 Holly Road', 1),
('dodong@yahoo.com', 'pword1', 'Alden', 'Mee', '7569 Grant Ave', 3),
('killmenow@optonline.net', 'pword1', 'Todd', 'Carl', '68 Oakwood Drive', 3),
('vin_lz@outlook.com', 'pword1', 'Vin', 'Liu', '110 1st St', 3);
SELECT * FROM Users;
UPDATE Users SET last_logout_timestamp = '2017-01-01 00:00:00' WHERE uid = 11;