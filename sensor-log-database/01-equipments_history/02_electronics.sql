USE rheonics_logs;

CREATE TABLE
  electronics (
    electronic_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    serial_electronic VARCHAR(100) NULL,
    model VARCHAR(100) NULL,
    created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (electronic_id),
    UNIQUE KEY uq_electronic_serial (serial_electronic)
  )