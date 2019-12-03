# Schemas

1. Users (*uid*, email, pword, fname, lname, street_addr, cid, uprofile, photo, last_login_timestamp)
2. Hood (*hid*, hname, sw_lat, sw_lng, ne_lat, ne_long, hpopulation)
3. Blocks (*bid*, bname, sw_lat, sw_lng, ne_lat, ne_lng, bpopulation)
4. Location (*bid*, *hid*, *cid*)
5. Membership (*uid*, *bid*, approval_count)
6. Friendship (*follower*, *followee*, *ftimestamp*, fstatus)
7. Neighboring (*initiator*, *acceptor*, *ntimestamp*)
8. Message (*mid*, author, title, content, mtimestamp, visibility, receiver, lat, lng)
9. Reply (*rid*, *mid*, author, content, rtimestamp)
10. Thread (*uid*, *mid*, tstatus, ttimestamp)
11. City (*cid*, cname, state)

User:

* `uid` is auto-generated and is a primary key.
* `email` serves as username.
* `password` should be hashed properly. Or we can try Google Oauth.

Neighborhood:

* `nid` is auto-generated and is a primary key.
* `sw_lat, sw_lng, ne_lat, ne_lng` stores the "axis-aligned" rectangles mentioned in the `pro1.pdf`.
* `population` is the number of users in that particular `Neighborhood`.

Block:

* Similar to `Neighborhood`.

Location:

* `nid` and `bid` are primary key specifying that the block is in the neighborhood.

Membership:

* `uid` and `bid` are the primary key specifying a user is a member of that particular block.
* `uid` is a foreign key referencing `uid` in `User`. `bid` is a foreign key referencing `bid` in `Block`.
* `nid` is a foreign key referencing `nid` in `Neighborhood`.
* `approval_count` is the number of approval the user get from other users within the block. It is set to "0" when the user registers into the block. If `approval_count` >= 3, the user is in the block.

Friendship:

* `follower`, `followee` `timestamp` are the primary key specifying the symmetric friendship. `follower` sends the request, `followee` accepts the request. The request can be resend if `followee` rejects.
`follower` is a foreign key referencing `uid` in `User`. `followee` ris a foreign key referencing `uid` in `User`.

Neighboring:

* `initiator` and `acceptor` are the primary key specifying a unilaterally neighbor relationship.
* `initiator` is a foreign key referencing `uid` in `User`. `acceptor` is a foreign key referencing `uid` in `User`.
* `initiator` add `acceptor` into his/her neighbor list.

Message:

* `mid` is the primary key.
* `author` is a foreign key referencing `uid` in `User`.
* If `level` is set to direct message, a `receiver`, which is a foreign key referencing a `uid` in `User`, must be provided to be the receiver of this message.

Reply:

* `rid` and `mid` are the primary key specifying a `Reply` to a `Message`.
* `mid` is a foreign key referencing `mid` in `Message`.

Thread:

* `uid` and `mid` are the primary key specifying a user should see a message in his/her newsfeed timeline.
* `uid` is a foreign key referencing `uid` in `User`. `mid` is a foreign key referencing `mid` in `Message`.
* when a new reply is added into the database, a trigger sets `read` to "unread" for the corresponding message.
