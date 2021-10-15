# labs/AnmolStuff
Anmol's ML/data experiments for Recommeddit Backend

## Notes:
 * In testing_db.py, I refer to "sample_statements.json". This JSON was downloaded using the following BASH command:
```bash
wget -O sample_statements.json "https://api.pushshift.io/reddit/comment/search/?link_id=pzeblx&fields=body&subreddit=MovieSuggestions"
```

## Tools Used
### PostgreSQL (locally):
#### SETUP:
 * Please follow the instructions on [this page](https://www.postgresqltutorial.com/postgresql-getting-started/ "Getting Started with PostgreSQL")
#### POPULATING DATABASE:
[BASH] -->
```BASH
psql -U postgres
# input the password you created when installing the server
```
[PSQL] -->
```SQL
CREATE DATABASE Recommeddit;
\CONNECT Recommeddit
\COPY Movies from '{INSERT BASE PATH HERE}\mvnt.tsv' DELIMITER E'\t'
CREATE TABLE Sample_statements ("body" TEXT NOT NULL);
ALTER TABLE movies DROP COLUMN "endYear", DROP COLUMN "startYear", DROP COLUMN "language", DROP COLUMN "region", DROP COLUMN
 "index";
```
To ensure that you have duplicated the initialization, please run the following SQL commands to test the output:

[PSQL] -->
```SQL
\CONNECT Recommeddit
SELECT COUNT (DISTINCT title) from Movies;
-- Expected Output:
--   count
-- ---------
--  2003213
-- (1 row)

SELECT title FROM Movies LIMIT 10;
-- Expected Output:
--                     title
-- ---------------------------------------------
--  Carmencita
--  Le clown et ses chiens
--  The Clown and His Dogs
--  Pauvre Pierrot
--  Un bon bock
--  Blacksmith Scene
--  Blacksmithing
--  Chinese Opium Den
--  Corbett and Courtney Before the Kinetograph
--  Edison Kinetoscopic Record of a Sneeze
-- (10 rows)
```
Next step: Create a `database.ini` file in the same directory as your execution directory. Fill it with the following text information:

[TEXT] -->
```
[postgresql]
host=localhost
database=recommeddit
user=postgres
password={INSERT YOUR PASSWORD HERE}
```
Make sure that this file is listed in your `.gitignore` file.

You can now populate the sample statements table by running the python file `testing_db.py`.

[BASH] -->
```BASH
python3 ./testing_db.py
```
