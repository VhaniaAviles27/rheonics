USE rheonics_logs;

CREATE TABLE
  measurements (
    measurement_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    sample_id BIGINT UNSIGNED NOT NULL,
    measurement_type_id INT UNSIGNED NOT NULL,
    channel ENUM ('VALUE', 'PRIMARY', 'SECONDARY') NOT NULL DEFAULT 'VALUE',
    numeric_value DECIMAL(24, 10) NULL,
    original_value VARCHAR(80) NULL,
    quality ENUM ('OK', 'NAN', 'MISSING', 'NON_NUMERIC', 'INVALID') NOT NULL DEFAULT 'OK',
    PRIMARY KEY (measurement_id),
    CONSTRAINT fk_measurements_sample FOREIGN KEY (sample_id) REFERENCES samples (sample_id),
    CONSTRAINT fk_measurements_type FOREIGN KEY (measurement_type_id) REFERENCES measurement_types (measurement_type_id),
    UNIQUE KEY uq_measurements_sample_type_channel (sample_id, measurement_type_id, channel),
    KEY ix_measurements_type_sample (measurement_type_id, sample_id),
    CONSTRAINT ck_measurements_value_quality CHECK (
      (
        quality = 'OK'
        AND numeric_value IS NOT NULL
      )
      OR quality <> 'OK'
    )
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;