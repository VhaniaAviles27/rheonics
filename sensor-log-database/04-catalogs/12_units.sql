USE rheonics_logs;

CREATE TABLE
  units (
    unit_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    unit_symbol VARCHAR(30) NOT NULL,
    unit_name VARCHAR(100) NULL,
    PRIMARY KEY (unit_id),
    UNIQUE KEY uq_unit_symbol (unit_symbol)
  )