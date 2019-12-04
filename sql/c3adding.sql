-- User 1 add User 10 as a friend
INSERT INTO Friendship VALUE
(1, 10, CURRENT_TIMESTAMP, 'pending');

-- User 1 add User 10 as a neighbor
INSERT INTO Neighboring VALUE
(1, 10, CURRENT_TIMESTAMP);

-- User 10 accepts User 1's friend request
UPDATE Friendship SET fstatus = 'accepted'
WHERE followee = 10 AND follower = 1;

(SELECT follower FROM Friendship
WHERE followee = 3)
UNION
(SELECT followee FROM Friendship
WHERE follower = 3);

SELECT acceptor FROM Neighboring
WHERE initiator = 3;