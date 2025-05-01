# HouseofMarktech
This is a To-Do API built with Flask and MySQL. 

# Working

Run the following in your MySQL client

CREATE DATABASE To_do;

USE To_do;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    name VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(255),
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


Change this part in the app.py file
host='localhost'
user='root'
password='root'
database='To_do'
