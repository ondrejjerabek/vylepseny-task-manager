
CREATE DATABASE IF NOT EXISTS ukol_db;
USE ukol_db;

CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(100),
    popis TEXT,
    stav VARCHAR(50),
    termin DATE
);
