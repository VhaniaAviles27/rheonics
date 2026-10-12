USE rheonics_logs;

CREATE TABLE
  measurement_types (
    measurement_type_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    log_type ENUM ('A', 'P') NOT NULL,
    measurement_key VARCHAR(80) NOT NULL,
    documented_name VARCHAR(150) NULL,
    unit_id SMALLINT UNSIGNED NULL,
    description TEXT NULL,
    PRIMARY KEY (measurement_type_id),
    UNIQUE KEY uq_measurement_types_key (log_type, measurement_key),
    CONSTRAINT fk_measurement_types_unit FOREIGN KEY (unit_id) REFERENCES units (unit_id)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;