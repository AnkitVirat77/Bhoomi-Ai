use flaskdb

select *from users

alter table users add auth_provider VARCHAR(20)


CREATE TABLE user_details (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50),
    mobile VARCHAR(15),
    email VARCHAR(255) UNIQUE,
    location VARCHAR(100),
    crop_type VARCHAR(50),
    language VARCHAR(50)
);


select *from user_details