-- db_init.sql
CREATE DATABASE IF NOT EXISTS vigilancia 
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE vigilancia;

CREATE TABLE IF NOT EXISTS plates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  object_id INT NOT NULL,
  label VARCHAR(20) NOT NULL,
  plate VARCHAR(20) NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_plate (object_id, plate)
) ENGINE=InnoDB;
