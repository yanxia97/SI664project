--
-- Create database
--

CREATE DATABASE IF NOT EXISTS art;
USE art;

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS place, gender, artist, artist_role,
  artwork, `subject`, artwork_subject;
SET FOREIGN_KEY_CHECKS=1;

-- --
-- -- UNSD M49 Regions
-- --

-- CREATE TABLE IF NOT EXISTS region
--   (
--     region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     region_name VARCHAR(100) NOT NULL UNIQUE,
--     PRIMARY KEY (region_id)
--   )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- INSERT IGNORE INTO region (region_name) VALUES
--   ('Africa'), ('Americas'), ('Asia'), ('Europe'), ('Oceania');

-- --
-- -- UNSD M49 sub-regions.
-- --

-- CREATE TABLE IF NOT EXISTS sub_region
--   (
--     sub_region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     sub_region_name VARCHAR(100) NOT NULL UNIQUE,
--     region_id INTEGER NOT NULL,
--     PRIMARY KEY (sub_region_id),
--     FOREIGN KEY (region_id) REFERENCES region(region_id) ON DELETE CASCADE ON UPDATE CASCADE
--   )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- -- Set FK variables and populate the sub_region table.
-- SET @fk_africa =
--   (
--     SELECT region_id
--     FROM region
--     WHERE region_name = 'Africa'
--   );
-- SET @fk_americas =
--   (
--     SELECT region_id
--     FROM region
--     WHERE region_name = 'Americas'
--   );
-- SET @fk_asia =
--   (
--     SELECT region_id
--     FROM region
--     WHERE region_name = 'Asia'
--   );
-- SET @fk_europe =
--   (
--     SELECT region_id
--     FROM region
--     WHERE region_name = 'Europe'
--   );
-- SET @fk_oceania =
--   (
--     SELECT region_id
--     FROM region
--     WHERE region_name = 'Oceania'
--   );

-- INSERT IGNORE INTO sub_region (sub_region_name, region_id) VALUES
--   ('Australia and New Zealand', @fk_oceania),
--   ('Central Asia', @fk_asia),
--   ('Eastern Asia', @fk_asia),
--   ('Eastern Europe', @fk_europe),
--   ('Latin America and the Caribbean', @fk_americas),
--   ('Melanesia', @fk_oceania),
--   ('Micronesia', @fk_oceania),
--   ('Northern Africa', @fk_africa),
--   ('Northern America', @fk_americas),
--   ('Northern Europe', @fk_europe),
--   ('Polynesia', @fk_oceania),
--   ('South-eastern Asia', @fk_asia),
--   ('Southern Asia', @fk_asia),
--   ('Southern Europe', @fk_europe),
--   ('Sub-Saharan Africa', @fk_africa),
--   ('Western Asia', @fk_asia),
--   ('Western Europe', @fk_europe);

-- --
-- -- UNSD M49 intermediate regions.
-- --

-- CREATE TABLE IF NOT EXISTS intermediate_region
--   (
--     intermediate_region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     intermediate_region_name VARCHAR(100) NOT NULL UNIQUE,
--     sub_region_id INTEGER NOT NULL,
--     PRIMARY KEY (intermediate_region_id),
--     FOREIGN KEY (sub_region_id) REFERENCES sub_region(sub_region_id) ON DELETE CASCADE
--     ON UPDATE CASCADE
--   )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- -- Set FK variables and populate the intermediate_region table.
-- SET @fk_latin_am_carrib =
--   (
--     SELECT sub_region_id
--     FROM sub_region
--     WHERE sub_region_name = 'Latin America and the Caribbean'
--   );
-- SET @fk_north_europe =
--   (
--     SELECT sub_region_id
--     FROM sub_region
--     WHERE sub_region_name = 'Northern Europe'
--   );
-- SET @fk_sub_saharan =
--   (
--     SELECT sub_region_id
--     FROM sub_region
--     WHERE sub_region_name = 'Sub-Saharan Africa'
--   );

-- INSERT IGNORE INTO intermediate_region (intermediate_region_name, sub_region_id) VALUES
--   ('Caribbean', @fk_latin_am_carrib),
--   ('Central America', @fk_latin_am_carrib),
--   ('Channel Islands', @fk_north_europe),
--   ('Eastern Africa', @fk_sub_saharan),
--   ('Middle Africa', @fk_sub_saharan),
--   ('South America', @fk_latin_am_carrib),
--   ('Southern Africa', @fk_sub_saharan),
--   ('Western Africa', @fk_sub_saharan);

-- --
-- -- UNSD M49 country or areas.
-- --

-- -- Temporary target table for UNSD data import
-- CREATE TEMPORARY TABLE temp_country_area
--   (
--     id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     region_name VARCHAR(100) NULL,
--     sub_region_name VARCHAR(100) NULL,
--     intermediate_region_name VARCHAR(100) NULL,
--     country_area_name VARCHAR(100) NOT NULL,
--     country_area_m49_code SMALLINT(4) NOT NULL,
--     country_area_iso_alpha3_code CHAR(3) NULL,
--     PRIMARY KEY (id)
--   )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- -- Load data from external file.
-- -- Check for blank entries and set to NULL.
-- LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/un_area_country_codes-m49.csv'
-- INTO TABLE temp_country_area
--   CHARACTER SET utf8mb4
--   FIELDS TERMINATED BY '\t'
--   -- FIELDS TERMINATED BY ','
--   ENCLOSED BY '"'
--   LINES TERMINATED BY '\n'
--   -- LINES TERMINATED BY '\r\n'
--   IGNORE 1 LINES
--   (@dummy, region_name, sub_region_name, intermediate_region_name, country_area_name, country_area_m49_code,
--    country_area_iso_alpha3_code, @dummy, @dummy, @dummy, @dummy)

--   SET region_name = IF(region_name = '', NULL, region_name),
--   sub_region_name = IF(sub_region_name = '', NULL, sub_region_name),
--   intermediate_region_name = IF(intermediate_region_name = '', NULL, intermediate_region_name),
--   country_area_m49_code = IF(country_area_m49_code = '', NULL, country_area_m49_code),
--   country_area_iso_alpha3_code = IF(country_area_iso_alpha3_code = '', NULL, country_area_iso_alpha3_code);

-- --
-- -- UNSD M49 countries and areas
-- --

-- CREATE TABLE IF NOT EXISTS country_area
--   (
--     country_area_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     country_area_name VARCHAR(100) NOT NULL UNIQUE,
--     region_id INTEGER NULL,
--     sub_region_id INTEGER NULL,
--     intermediate_region_id INTEGER NULL,
--     m49_code SMALLINT(4) NOT NULL,
--     iso_alpha3_code CHAR(3) NOT NULL,s
--     PRIMARY KEY (country_area_id),
--     FOREIGN KEY (region_id) REFERENCES region(region_id)
--     ON DELETE CASCADE ON UPDATE CASCADE,
--     FOREIGN KEY (sub_region_id) REFERENCES sub_region(sub_region_id)
--     ON DELETE CASCADE ON UPDATE CASCADE,
--     FOREIGN KEY (intermediate_region_id) REFERENCES intermediate_region(intermediate_region_id)
--     ON DELETE CASCADE ON UPDATE CASCADE,
--    )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- -- Insert country_area attributes only (N=249) from temp table (no regions).
-- INSERT IGNORE INTO country_area
--   (
--     country_area_name,
--     region_id,
--     sub_region_id,
--     intermediate_region_id,
--     m49_code,
--     iso_alpha3_code
--   )
-- SELECT tc.country_area_name, r.region_id, sr.sub_region_id, ir.intermediate_region_id,
--        tc.country_area_m49_code, tc.country_area_iso_alpha3_code
--   FROM temp_country_area tc
--        LEFT JOIN region r
--               ON tc.region_name = r.region_name
--        LEFT JOIN sub_region sr
--               ON tc.sub_region_name = sr.sub_region_name
--        LEFT JOIN intermediate_region ir
--               ON tc.intermediate_region_name = ir.intermediate_region_name
--  WHERE IFNULL(tc.region_name, 0) = IFNULL(r.region_name, 0)
--    AND IFNULL(tc.sub_region_name, 0) = IFNULL(sr.sub_region_name, 0)
--    AND IFNULL(tc.intermediate_region_name, 0) = IFNULL(ir.intermediate_region_name, 0)
--  ORDER BY tc.country_area_name;

-- DROP TEMPORARY TABLE temp_country_area;

--
-- artist genders
--

CREATE TABLE IF NOT EXISTS gender
  (
    gender_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    gender_name VARCHAR(10) NOT NULL UNIQUE,
    PRIMARY KEY (gender_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO gender (gender_name) VALUES
  ('Male'), ('Female');

--
-- artist born and death places
--

-- Temporary target table for artist place import
CREATE TEMPORARY TABLE temp_place
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    place_name VARCHAR(100) NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/output/artist_place.csv'
INTO TABLE temp_place
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (place_name);

--   SET place_name = IF(place_name = '', NULL, place_name);

CREATE TABLE IF NOT EXISTS place
  (
    place_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    place_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (place_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert
INSERT IGNORE INTO place
  (
    place_name
  )
SELECT place_name
  FROM temp_place
 ORDER BY place_name;

DROP TEMPORARY TABLE temp_place;

--
-- artist
--

-- Temporary target table for artist data import
CREATE TEMPORARY TABLE temp_artist
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artist_name VARCHAR(100) NULL,
    gender_name VARCHAR(10) NULL,
    birth_place_name VARCHAR(100) NULL,
    death_place_name VARCHAR(100) NULL,
    artist_birth_year INT NULL,
    artist_death_year INT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.

LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/artist_data.csv'
INTO TABLE temp_artist
  CHARACTER SET utf8mb4
--   FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, artist_name, gender_name, @dummy, artist_birth_year, artist_death_year, birth_place_name,
   death_place_name, @dummy)

  SET gender_name = IF(gender_name = '', NULL, gender_name),
  artist_birth_year = IF(artist_birth_year = '', NULL, artist_birth_year),
  artist_death_year = IF(artist_death_year = '', NULL, artist_death_year),
  birth_place_name = IF(birth_place_name = '', NULL, birth_place_name),
  death_place_name = IF(death_place_name = '', NULL, death_place_name);

-- Insert
CREATE TABLE IF NOT EXISTS artist
  (
    artist_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artist_name VARCHAR(100) NOT NULL,
    gender_id INTEGER NULL,
    birth_place_id INTEGER NULL,
    death_place_id INTEGER NULL,
    birth_year INT NULL,
    death_year INT NULL,
    PRIMARY KEY (artist_id),
    FOREIGN KEY (gender_id) REFERENCES gender(gender_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (birth_place_id) REFERENCES place(place_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (death_place_id) REFERENCES place(place_id)
    ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO artist
  (
    artist_name,
    gender_id,
    birth_place_id,
    death_place_id,
    birth_year,
    death_year
  )
SELECT ta.artist_name, g.gender_id, bp.place_id, dp.place_id, ta.artist_birth_year, ta.artist_death_year
  FROM temp_artist ta
       LEFT JOIN gender g
              ON ta.gender_name = g.gender_name
       LEFT JOIN place bp
              ON ta.birth_place_name = bp.place_name
       LEFT JOIN place dp
              ON ta.death_place_name = dp.place_name
 WHERE IFNULL(ta.gender_name, 0) = IFNULL(g.gender_name, 0)
   AND IFNULL(ta.birth_place_name, 0) = IFNULL(bp.place_name, 0)
   AND IFNULL(ta.death_place_name, 0) = IFNULL(dp.place_name, 0)
 ORDER BY ta.artist_name;

DROP TEMPORARY TABLE temp_artist;

--
-- artist role
--

-- Temporary target table for artist role data import
CREATE TEMPORARY TABLE temp_artist_role
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artist_role_name VARCHAR(45) NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/output/artist_role.csv'
INTO TABLE temp_artist_role
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (artist_role_name);

CREATE TABLE IF NOT EXISTS artist_role
  (
    artist_role_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artist_role_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (artist_role_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert
INSERT IGNORE INTO artist_role
  (
    artist_role_name
  )
SELECT artist_role_name
  FROM temp_artist_role
 ORDER BY artist_role_name;

DROP TEMPORARY TABLE temp_artist_role;

--
-- artwork
--

-- Temporary target table for artwork data import
CREATE TEMPORARY TABLE temp_artwork
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    accession_number CHAR(6) NOT NULL,
    title VARCHAR(999) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    artistRole VARCHAR(45) NOT NULL,
    dateText VARCHAR(100) NOT NULL,
    medium VARCHAR(100) NOT NULL,
    creditLine VARCHAR(999) NOT NULL,    
    acquisitionYear INT NOT NULL,
    width INT NULL,
    height INT NULL,
    depth INT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.

LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/artwork_data.csv'
INTO TABLE temp_artwork
  CHARACTER SET utf8mb4
--   FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, accession_number, artist, artistRole, @dummy, title, dateText, medium,
   creditLine, @dummy, acquisitionYear, @dummy, width, height, depth, @dummy, @dummy, @dummy, @dummy, @dummy)

  SET width = IF(width = '', NULL, width),
  height = IF(height = '', NULL, height),
  depth = IF(depth = '', NULL, depth);

-- Insert
CREATE TABLE IF NOT EXISTS artwork
  (
    artwork_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artwork_name VARCHAR(999) NOT NULL,
    accession_number CHAR(6) NOT NULL UNIQUE,
    artist_id INTEGER NOT NULL,
    artist_role_id INTEGER NOT NULL,
    date_text VARCHAR(100) NOT NULL,
    medium VARCHAR(100) NOT NULL,
    credit_line VARCHAR(999) NOT NULL,    
    acquisition_year INT NOT NULL,
    width INT NULL,
    height INT NULL,
    depth INT NULL,
    PRIMARY KEY (artwork_id),
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artist_role_id) REFERENCES artist_role(artist_role_id)
    ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO artwork
  (
    artwork_name,
    accession_number,
    artist_id,
    artist_role_id,
    date_text,
    medium,
    credit_line,    
    acquisition_year,
    width,
    height,
    depth
  )
SELECT ta.title, ta.accession_number, a.artist_id, ar.artist_role_id, ta.dateText, ta.medium, ta.creditLine, ta.acquisitionYear, ta.width, ta.height, ta.depth
  FROM temp_artwork ta
       LEFT JOIN artist a
              ON ta.artist = a.artist_name
       LEFT JOIN artist_role ar
              ON ta.artistRole = ar.artist_role_name
 WHERE IFNULL(ta.artist, 0) = IFNULL(a.artist_name, 0)
   AND IFNULL(ta.artistRole, 0) = IFNULL(ar.artist_role_name, 0)
 ORDER BY ta.accession_number;

DROP TEMPORARY TABLE temp_artwork;

--
-- subject
--

-- Temporary target table for subject data import
CREATE TEMPORARY TABLE temp_subject
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    original_id INT NOT NULL,
    subject_name VARCHAR(45) NOT NULL,
    parent_original_id INT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/output/subject.csv'
INTO TABLE temp_subject
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (original_id, subject_name, parent_original_id)

  SET parent_original_id = IF(parent_original_id = '', NULL, parent_original_id);

CREATE TABLE IF NOT EXISTS `subject`
  (
    subject_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    original_id INT NOT NULL,
    subject_name VARCHAR (45) NOT NULL,
    PRIMARY KEY (subject_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert
INSERT IGNORE INTO `subject`
  (
    original_id,
    subject_name
  )
SELECT original_id, subject_name
  FROM temp_subject
 ORDER BY subject_name;

ALTER TABLE `subject`
        ADD COLUMN parent_subject_id INT NULL DEFAULT 1 AFTER subject_name,
        ADD CONSTRAINT subject_fk_parent_subject_id
            FOREIGN KEY (parent_subject_id) REFERENCES `subject`(subject_id)
            ON DELETE CASCADE ON UPDATE CASCADE;

-- update the parent_subject_id
UPDATE `subject` AS s
   SET s.parent_subject_id = (
     SELECT a.id FROM (
       SELECT parent.subject_id AS id, ts.original_id AS original_id
         FROM temp_subject AS ts
              LEFT JOIN `subject` parent
                     ON ts.parent_original_id = parent.original_id
      )a
      WHERE IFNULL(a.original_id, 0) = IFNULL(s.original_id, 0)
    );

DROP TEMPORARY TABLE temp_subject;

--
-- Link artworks to subjects
--

-- Junction table linking artworks to subjects (many-to-many).
-- WARN: Django 2.x ORM does not recognize compound keys. Add otherwise superfluous primary key
-- to accommodate a weak ORM.

-- Create temporary table to store the relationship
CREATE TEMPORARY TABLE temp_relationship
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    accession_number CHAR(6) NOT NULL,
    subject_original_id INT NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/a1/Desktop/2018_fall/SI664/final_project/github/collection/output/artwork_subject.csv'
INTO TABLE temp_relationship
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (accession_number, subject_original_id, @dummy);

CREATE TABLE IF NOT EXISTS artwork_subject
  (
    artwork_subject_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    artwork_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    PRIMARY KEY (artwork_subject_id),
    FOREIGN KEY (artwork_id) REFERENCES artwork(artwork_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES `subject`(subject_id)
    ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert
INSERT IGNORE INTO artwork_subject
  (
    artwork_id,
    subject_id
  )
SELECT a.artwork_id,
       s.subject_id
  FROM temp_relationship tr
       LEFT JOIN artwork a
              ON tr.accession_number = a.accession_number
       LEFT JOIN `subject` s
              ON tr.subject_original_id = s.original_id
 ORDER BY tr.id;

DROP TEMPORARY TABLE temp_relationship;