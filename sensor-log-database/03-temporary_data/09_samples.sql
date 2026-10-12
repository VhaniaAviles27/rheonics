USE rheonics_logs;

CREATE TABLE
  samples (
    sample_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    import_id BIGINT UNSIGNED NOT NULL,
    line_number INT UNSIGNED NOT NULL,
    timestamp_unix BIGINT NULL,
    timestamp_utc DATETIME (6) NULL,
    validation ENUM ('VALID', 'PARTIAL', 'INVALID') NOT NULL,
    description_error TEXT NULL,
    raw_record TEXT NOT NULL,
    hash_record BINARY(32) NOT NULL,
    PRIMARY KEY (sample_id),
    CONSTRAINT fk_samples_import FOREIGN KEY (import_id) REFERENCES import_logs (import_id),
    UNIQUE KEY uq_samples_import_line (import_id, line_number),
    KEY ix_samples_timestamp (timestamp_utc),
    KEY ix_samples_import_timestamp (import_id, timestamp_utc),
    KEY ix_samples_hash (hash_record)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;