## Basic Reporting Tool (BARETO)

## Setup
* Install required packets (**sudo apt-get install libpq-dev postgresql postgresql-contrib**).
* Enter to postgres user (**su postgres**).
* Start a postgres session (**psql**).
* Creta a database (**CREATE DATABASE bareto;**).
* Create a new user for the database and CHANGE THE PASSWORD! (**CREATE USER baretouser WITH PASSWORD 'ChangeThisPassword!';**).
* Change the encoding (**ALTER ROLE baretouser SET client_encoding TO 'utf8';**).
* Change the transaction isolation (**ALTER ROLE baretouser SET default_transaction_isolation TO 'read committed';**).
* Change the time zone (**ALTER ROLE baretouser SET timezone TO 'UTC';**).
* Add privileges to the new user (**GRANT ALL PRIVILEGES ON DATABASE bareto TO baretouser;**).
* Exit form the postgres session (**\q**).
* Exit from the postgres user(**exit**).