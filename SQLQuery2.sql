use flaskdb
select *from users


ALTER TABLE users
ADD CONSTRAINT unique_email UNIQUE (email);

DELETE FROM users;



delete from users where id = 25