USE rheonics_logs;

CREATE TABLE
  sensors (
    sensor_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    serial_sensor VARCHAR(100) NULL,
    model VARCHAR(100) NULL,
    created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (sensor_id),
    UNIQUE KEY uq_sensor_serial (serial_sensor)
  )