CREATE TABLE IF NOT EXISTS mainmenu(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS film_list(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    genre text NOT NULL,
    short_review text NOT NULL
);