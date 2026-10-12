USE rheonics_logs;

CREATE TABLE
  electronic_sensor_history (
    history_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    sensor_id BIGINT UNSIGNED NOT NULL,
    electronic_id BIGINT UNSIGNED NOT NULL,
    valid_from DATETIME (6) NOT NULL,
    valid_to DATETIME (6) NULL,
    PRIMARY KEY (history_id),
    CONSTRAINT fk_history_sensor FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id),
    CONSTRAINT fk_history_electronic FOREIGN KEY (electronic_id) REFERENCES electronics (electronic_id),
    CONSTRAINT ck_history_interval CHECK (
      valid_to IS NULL
      OR valid_to > valid_from
    ),
    KEY ix_history_sensor_time (sensor_id, valid_from, valid_to),
    KEY ix_history_electronic_time (electronic_id, valid_from, valid_to)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;