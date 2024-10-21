-- Author: Gadoskey
-- File: 0-uniq_users.sql
-- A SQL script that creates a table users if it does not exist

CREATE TABLE IF NOT EXISTS users (
    id AUTOINCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
