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
