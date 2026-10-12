USE rheonics_logs;

CREATE TABLE
  import_logs (
    import_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    receipt_id BIGINT UNSIGNED NOT NULL,
    sensor_id BIGINT UNSIGNED NULL,
    electronic_id BIGINT UNSIGNED NULL,
    firmware_version_id INT UNSIGNED NULL,
    parser_version VARCHAR(80) NOT NULL,
    status ENUM (
      'RECEIVED',
      'VALIDATING',
      'PARSING',
      'LOADING',
      'COMPLETED',
      'COMPLETED_WITH_ERRORS',
      'FAILED'
    ) NOT NULL DEFAULT 'RECEIVED',
    started_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    finished_at DATETIME (6) NULL,
    total_lines INT UNSIGNED NOT NULL DEFAULT 0,
    valid_rows INT UNSIGNED NOT NULL DEFAULT 0,
    invalid_rows INT UNSIGNED NOT NULL DEFAULT 0,
    inserted_rows INT UNSIGNED NOT NULL DEFAULT 0,
    summary_message TEXT NULL,
    PRIMARY KEY (import_id),
    CONSTRAINT fk_import_receipt FOREIGN KEY (receipt_id) REFERENCES log_file_receipts (receipt_id),
    CONSTRAINT fk_import_sensor FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id),
    CONSTRAINT fk_import_electronic FOREIGN KEY (electronic_id) REFERENCES electronics (electronic_id),
    CONSTRAINT fk_import_firmware FOREIGN KEY (firmware_version_id) REFERENCES firmware_versions (firmware_version_id),
    CONSTRAINT ck_import_counts CHECK (valid_rows + invalid_rows <= total_lines),
    CONSTRAINT ck_import_finished_after_started CHECK (
      finished_at IS NULL
      OR finished_at >= started_at
    ),
    KEY ix_import_sensor_started (sensor_id, started_at),
    KEY ix_import_electronic_started (electronic_id, started_at),
    KEY ix_import_receipt_status (receipt_id, status)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;