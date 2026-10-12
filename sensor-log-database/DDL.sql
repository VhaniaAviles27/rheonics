CREATE DATABASE IF NOT EXISTS rheonics_logs CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE rheonics_logs;

CREATE TABLE
    sensors (
        sensor_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        serial_sensor VARCHAR(100) NULL,
        model VARCHAR(100) NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        PRIMARY KEY (sensor_id),
        UNIQUE KEY uq_sensors_serial (serial_sensor)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    electronics (
        electronic_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        serial_electronic VARCHAR(100) NULL,
        model VARCHAR(100) NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        PRIMARY KEY (electronic_id),
        UNIQUE KEY uq_electronics_serial (serial_electronic)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    firmware_versions (
        firmware_version_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        version VARCHAR(100) NOT NULL,
        PRIMARY KEY (firmware_version_id),
        UNIQUE KEY uq_firmware_version (version)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    units (
        unit_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
        unit_symbol VARCHAR(30) NOT NULL,
        unit_name VARCHAR(100) NULL,
        PRIMARY KEY (unit_id),
        UNIQUE KEY uq_units_symbol (unit_symbol)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

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

CREATE TABLE
    catalog_codes (
        code_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        log_type ENUM ('A', 'P', 'BOTH') NOT NULL,
        component VARCHAR(100) NOT NULL,
        code VARCHAR(40) NOT NULL,
        code_class ENUM ('STATE', 'ERROR', 'QUALITY', 'UNKNOWN') NOT NULL DEFAULT 'UNKNOWN',
        documented_description VARCHAR(500) NULL,
        is_error TINYINT NOT NULL DEFAULT 0,
        PRIMARY KEY (code_id),
        UNIQUE KEY uq_catalog_codes (log_type, component, code),
        CONSTRAINT ck_catalog_codes_is_error CHECK (is_error IN (0, 1))
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

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

CREATE TABLE
    status_events (
        event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        sample_id BIGINT UNSIGNED NOT NULL,
        code_id BIGINT UNSIGNED NOT NULL,
        occurrence_no SMALLINT UNSIGNED NOT NULL DEFAULT 1,
        associated_value VARCHAR(80) NULL,
        PRIMARY KEY (event_id),
        CONSTRAINT fk_status_events_sample FOREIGN KEY (sample_id) REFERENCES samples (sample_id),
        CONSTRAINT fk_status_events_code FOREIGN KEY (code_id) REFERENCES catalog_codes (code_id),
        UNIQUE KEY uq_status_event_occurrence (sample_id, code_id, occurrence_no),
        KEY ix_status_events_code_sample (code_id, sample_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

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