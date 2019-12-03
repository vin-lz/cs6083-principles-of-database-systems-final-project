DELETE FROM Reply;
ALTER TABLE `projectdb`.`Reply` 
AUTO_INCREMENT = 1;
INSERT INTO Reply(mid, author, content, rtimestamp) VALUES 
(1, 9, 'I didn\'t see it.', '2018-03-03 20:00:00'),
(1, 8, 'I didn\'t see it, either.', '2018-03-04 20:00:00'),
(1, 10, 'Sorry to hear that.', '2018-03-03 21:00:00'),
(7, 11, 'Gotta buy a PS4 for gaming!', '2019-08-20 10:41:33'),
(6, 6, 'I wish I could go but I\'m working on the database project.', '2019-11-21 00:00:49'),
(5, 5, 'I got it!','2019-11-29 16:00:05'),
(5, 3, 'I got it!','2019-11-29 16:00:07'),
(3, 2, 'I didn\'t get it.', '2018-03-02 20:20:04');
SELECT * FROM Reply;
