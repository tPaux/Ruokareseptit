CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ingredients TEXT,
    instructions TEXT,
    image BLOB,
    sent_at TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);
