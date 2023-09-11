-- migration_script.sql

-- Add the "images" column to the "properties" table
ALTER TABLE properties
ADD COLUMN images TEXT;
