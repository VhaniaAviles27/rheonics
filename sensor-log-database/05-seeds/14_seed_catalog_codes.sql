USE rheonics_logs;

INSERT INTO
  catalog_codes (
    log_type,
    component,
    code,
    code_class,
    documented_description,
    is_error
  )
VALUES
  (
    'A',
    'A:E',
    'E',
    'ERROR',
    'A-LOG error code (semantics not documented)',
    1
  ),
  (
    'A',
    'A:A',
    'A',
    'STATE',
    'Measurement string age marker',
    0
  ),
  (
    'P',
    'P:overall_status',
    'overall',
    'STATE',
    'P-LOG overall status field',
    0
  ),
  (
    'P',
    'P:0:status1',
    'status1',
    'STATE',
    'Parameter 0 status1',
    0
  ),
  (
    'P',
    'P:0:status2',
    'status2',
    'STATE',
    'Parameter 0 status2',
    0
  ),
  (
    'BOTH',
    'UNKNOWN',
    'UNKNOWN',
    'UNKNOWN',
    'Placeholder for undocumented codes',
    0
  ) ON DUPLICATE KEY
UPDATE code_class =
VALUES
  (code_class),
  documented_description =
VALUES
  (documented_description),
  is_error =
VALUES
  (is_error);