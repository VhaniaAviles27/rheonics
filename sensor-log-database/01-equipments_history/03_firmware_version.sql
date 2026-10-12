USE rheonics_logs;

CREATE TABLE
  firmware_versions (
    firmware_version_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    version VARCHAR(100) NOT NULL,
    PRIMARY KEY (firmware_version_id),
    UNIQUE KEY uq_firmware_version (version)
  )