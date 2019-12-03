-- List all threads that have new messages cince last time access
SET @query_user = 11;
SET @llt = (SELECT last_login_timestamp FROM Users AS u
WHERE u.uid = @query_user);

SELECT mid FROM Thread 
	WHERE ttimestamp > @llt AND uid = @query_user;

SELECT * FROM Message
WHERE mid IN (SELECT mid FROM Thread 
	WHERE ttimestamp > @llt AND uid = @query_user);

SELECT * FROM Reply
WHERE mid IN (SELECT mid FROM Message
WHERE mid IN (SELECT mid FROM Thread 
	WHERE ttimestamp > @llt AND uid = @query_user));

-- List all unread messages in friend feed
SET @query_user = 11;

SELECT * FROM Message AS w, 
(SELECT mid FROM Message 
WHERE author IN
	(SELECT follower FROM Friendship
		WHERE followee = @query_user AND fstatus = 'accepted'
	UNION
	SELECT followee FROM Friendship
		WHERE follower = @query_user AND fstatus = 'accepted')
AND visibility = 'friend') AS m
WHERE w.mid IN
(SELECT mid FROM Thread
WHERE uid = @query_user AND tstatus = 'unread') AND m.mid = w.mid;

-- List all "bicycle accident" message the user can access
SELECT * FROM Thread
WHERE uid = @query_user AND mid IN
(SELECT mid FROM Message
WHERE title LIKE '%bicycle accident%' OR content LIKE '%bicycle accident%');





