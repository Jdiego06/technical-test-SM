CREATE DATABASE recipes_and_interactions;

USE recipes_and_interactions;

CREATE TABLE users (
    id INT NOT NULL,
    techniques TEXT,
    items TEXT,
    ratings TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE recipes (
	id INT NOT NULL,    
	name VARCHAR(512),
    minutes INT,
    contributor_id INT,
	submitted DATE,
	tags TEXT,
	nutrition TEXT,
	steps TEXT,
	description TEXT,
	ingredients TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE interactions (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    date DATE,
    rating TINYINT,
    review TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(recipe_id) REFERENCES recipes(id)
);

