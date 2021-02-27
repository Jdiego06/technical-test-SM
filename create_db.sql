CREATE DATABASE recipes_and_interactions;

USE recipes_and_interactions;

CREATE TABLE users (
    id INT NOT NULL,
    techniques VARCHAR(200),
    items VARCHAR(200),
    ratings VARCHAR(200),
    PRIMARY KEY (id)
);

CREATE TABLE recipes (
	id INT NOT NULL,    
	name VARCHAR(200),
    minutes INT,
    contributor_id INT,
	submitted DATE,
	tags VARCHAR(200),
	nutrition VARCHAR(200),
	steps	VARCHAR(200),
	description VARCHAR(200),
	ingredients VARCHAR(200),
    PRIMARY KEY (id)
);

CREATE TABLE interactions (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    date DATE,
    rating TINYINT,
    review VARCHAR(200),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(recipe_id) REFERENCES recipes(id)
);

