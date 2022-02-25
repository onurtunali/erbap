
-- We need to drop tables with foreign keys first to prevent error.

DROP TABLE IF EXISTS likes;

DROP TABLE IF EXISTS reviews;

DROP TABLE IF EXISTS books;

DROP TABLE IF EXISTS users;

CREATE TABLE books (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  book_title VARCHAR(200),
  author_name VARCHAR(200),
  edition_language CHAR(8),
  rating_score FLOAT,
  rating_votes INTEGER,
  review_number INTEGER,
  book_description LONGTEXT,
  year_published INTEGER,
  genres TEXT,
  url VARCHAR(200),
  cover VARCHAR(200)
);

CREATE TABLE reviews (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  book_id INTEGER NOT NULL,
  date DATE,
  rating FLOAT,
  hash VARCHAR(50) NOT NULL UNIQUE,
  review_text MEDIUMTEXT,
  capture_date DATE,
  FOREIGN KEY (book_id) REFERENCES books (id)
);

CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL
);

CREATE TABLE likes (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  book_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (book_id) REFERENCES books (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);