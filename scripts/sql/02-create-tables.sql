use smart_garden;

CREATE TABLE devices (
    id INTEGER NOT NULL AUTO_INCREMENT,
    serial text,
    model text,
    description text,
    PRIMARY KEY(id)
);

CREATE TABLE configs (
    id INTEGER NOT NULL AUTO_INCREMENT,
    dev_id INTEGER NOT NULL,
    dev_group text,
    dev_interval text,
    PRIMARY KEY(id)
);

CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT,
    username text,
    passwd text,
    PRIMARY KEY(id)
);

INSERT INTO users(username, passwd) values(
    "admin",
    "910158f3631d8263272b121ef90fe71907deab41ff4ad504fb224900bce7e6ab"
);
