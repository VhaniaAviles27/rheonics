USE rheonics_logs;

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