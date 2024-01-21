use smart_garden;

create table devices (
  id integer NOT NULL AUTO_INCREMENT,
  serial text,
  model text,
  description text,
  PRIMARY KEY(id)
);

create table configs (
  id integer NOT NULL AUTO_INCREMENT,
  dev_id integer NOT NULL,
  dev_group text,
  dev_interval text,
  PRIMARY KEY(id)
);
