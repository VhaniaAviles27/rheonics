USE rheonics_logs;

CREATE TABLE
  log_files (
    file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    log_type ENUM ('A', 'P', 'UNKNOWN') NOT NULL,
    sha256 CHAR(64) NOT NULL,
    file_size_bytes BIGINT UNSIGNED NOT NULL,
    original_content LONGBLOB NULL,
    PRIMARY KEY (file_id),
    UNIQUE KEY uq_log_files_sha256 (sha256),
    CONSTRAINT ck_log_files_sha256_format CHECK (sha256 REGEXP '^[0-9a-f]{64}$')
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;