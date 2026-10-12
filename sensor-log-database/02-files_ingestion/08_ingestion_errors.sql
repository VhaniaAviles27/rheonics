USE rheonics_logs;

CREATE TABLE
  ingestion_errors (
    ingestion_error_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    import_id BIGINT UNSIGNED NOT NULL,
    line_number INT UNSIGNED NULL,
    stage ENUM (
      'CHECKSUM',
      'VALIDATION',
      'PARSING',
      'STAGING',
      'LOADING',
      'POSTPROCESS'
    ) NOT NULL,
    error_code VARCHAR(80) NOT NULL,
    message TEXT NOT NULL,
    raw_fragment TEXT NULL,
    occurred_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (ingestion_error_id),
    CONSTRAINT fk_ingestion_errors_import FOREIGN KEY (import_id) REFERENCES import_logs (import_id),
    KEY ix_ingestion_errors_import_line (import_id, line_number),
    KEY ix_ingestion_errors_code_time (error_code, occurred_at)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;