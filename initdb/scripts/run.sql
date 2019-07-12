--
-- create database and schema. then change default search path
-- https://wiki.hackzine.org/sysadmin/postgresql-change-default-schema.html
--
CREATE DATABASE testdb;
\connect testdb;

CREATE SCHEMA testschema;
GRANT ALL ON SCHEMA testschema TO testuser;

-- change search_path on a connection-level
SET search_path TO testschema;

-- change search_path on a database-level
ALTER database "testdb" SET search_path TO testschema;

--
-- create table
--

CREATE TABLE testschema.records (
	id serial NOT NULL,
	record varchar(30) NOT NULL,
	source varchar(5) NOT NULL,
	created_on timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT records_pkey PRIMARY KEY (id)
);

INSERT INTO testschema.records (record) VALUES
('foo', 'web'),
('bar', 'web'),
('baz', 'web');
