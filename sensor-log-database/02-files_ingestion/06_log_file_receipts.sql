USE rheonics_logs;

CREATE TABLE
  log_file_receipts (
    receipt_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    file_id BIGINT UNSIGNED NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    path_or_uri VARCHAR(1024) NULL,
    received_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (receipt_id),
    CONSTRAINT fk_receipts_file FOREIGN KEY (file_id) REFERENCES log_files (file_id),
    KEY ix_receipts_file_received (file_id, received_at)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;