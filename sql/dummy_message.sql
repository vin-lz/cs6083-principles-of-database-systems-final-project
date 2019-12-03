DELETE FROM Message;
ALTER TABLE `projectdb`.`Message` 
AUTO_INCREMENT = 1;
INSERT INTO Message(author, title, content, mtimestamp, visibility, receiver, lat, lng) VALUES 
(11, 'Bicycle accident', 'There is a bicycle accident on the third street. Anyone witness?', '2018-03-02 20:00:00', 'hood', NULL, 1.1, 1.1),
(10, 'New hot dog store', 'The new dog store is so hot, yay!', '2018-03-03 10:00:00', 'hood', NULL, 1.1, 1.1),
(10, 'Brain problem', 'My right brain has noting left.', '2018-03-02 20:00:00', 'block', NULL, 1.2, 1.2),
(10, 'Brain problem', 'My left brain has nothing right', '2018-03-03 20:00:00', 'block', NULL, 1.1, 1.1),
(11, 'Pokemon go fans', 'Anyone found a pikachu near the new Xmas tree?', '2019-11-29 16:00:01', 'friend', NULL, 1.1, 1.1),
(11, 'Hitchhicker for Woodbury shopping', 'Hi Cami! One spare spot to Woodbury on Friday night. Are you coming?', '2019-11-20 01:40:49', 'direct', 5, 1.1, 1.1),
(1, 'FFVII Remake is coming', 'Yo, bro! Final Fantasy VII Remake is coming next year! How exciting!', '2019-08-20 01:40:33', 'direct', 11, NULL, NULL),
(5, 'Street Food Festival', 'Chilli Daddy has the best noodle soup for you!', '2018-01-02 20:00:00', 'block', NULL, 1.1, 1.1),
(5, 'AD: Free cake', 'Free cake give away at the Plaza ', '2018-01-02 20:00:01', 'block', NULL, 1.1, 1.1)
(5, 'Street Food Festival Again', 'Chilli Daddy has the best noodle soup for you!', '2018-01-02 21:00:00', 'friend', NULL, 1.1, 1.1),
SELECT * FROM Message;
