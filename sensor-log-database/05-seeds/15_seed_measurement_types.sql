USE rheonics_logs;

INSERT INTO
  measurement_types (
    log_type,
    measurement_key,
    documented_name,
    description
  )
VALUES
  ('A', 'T', 'temperature', 'Temperature'),
  (
    'A',
    'f',
    'resonant frequency',
    'Resonant frequency'
  ),
  ('A', 'df', 'damping', 'Damping'),
  ('A', 'Fv', 'VCO frequency', 'Unit not specified'),
  (
    'A',
    'ph',
    'resonator phase preset',
    'Unit not specified'
  ),
  (
    'A',
    'V',
    'viscosity estimate',
    'Median of 5 measurements; unit not specified'
  ),
  (
    'A',
    'D',
    'density estimate',
    'Unit not specified'
  ),
  ('A', 'P', 'pressure input', 'Unit not specified'),
  (
    'A',
    'fc',
    'compensated resonant frequency',
    'Unit not specified'
  ),
  (
    'A',
    'I-',
    'excitation current negative',
    'Unit not specified'
  ),
  (
    'A',
    'I+',
    'excitation current positive',
    'Unit not specified'
  ),
  ('A', 'Q', 'df ratio df-/df+', 'Ratio'),
  (
    'A',
    'fr',
    'reference frequency',
    'Unit not specified'
  ),
  (
    'A',
    'df-',
    'negative phase slope',
    'Unit not specified'
  ),
  (
    'A',
    'df+',
    'positive phase slope',
    'Unit not specified'
  ),
  (
    'A',
    'Tc',
    'coil temperature',
    'Unit not specified in tag table'
  ),
  (
    'A',
    'Tp',
    'PT1000 temperature',
    'Unit not specified in tag table'
  ),
  (
    'A',
    'Te',
    'estimated internal temperature',
    'Unit not specified in tag table'
  ),
  (
    'A',
    'A',
    'measurement string age',
    'Unit not specified'
  ),
  (
    'P',
    'P:0',
    'viscosity median / 5 measurements',
    NULL
  ),
  (
    'P',
    'P:1',
    'density median / 5 measurements',
    NULL
  ),
  (
    'P',
    'P:2',
    'temperature median / 5 measurements',
    NULL
  ),
  ('P', 'P:3', 'kinematic viscosity', NULL),
  (
    'P',
    'P:4',
    'density average / 5 measurements',
    NULL
  ),
  ('P', 'P:5', 'viscosity raw (V)', NULL),
  ('P', 'P:6', 'density raw (D)', NULL),
  ('P', 'P:7', 'temperature raw (T)', NULL),
  ('P', 'P:8', 'resonant frequency (f)', NULL),
  (
    'P',
    'P:9',
    'compensated resonant frequency (fc)',
    NULL
  ),
  ('P', 'P:10', 'damping (df)', NULL),
  ('P', 'P:11', 'coil temperature (Tc)', NULL),
  (
    'P',
    'P:12',
    'viscosity median and last good',
    NULL
  ),
  ('P', 'P:13', 'density median and last good', NULL),
  ('P', 'P:14', 'mapped Modbus register 512', NULL),
  ('P', 'P:15', 'mapped Modbus register 514', NULL),
  ('P', 'P:16', 'mapped Modbus register 516', NULL),
  ('P', 'P:17', 'estimated temperature (Te)', NULL),
  ('P', 'P:18', 'PT1000 temperature (Tp)', NULL),
  (
    'P',
    'P:19',
    'calculated viscosity model parameter',
    NULL
  ),
  (
    'P',
    'P:20',
    'calculated density model parameter',
    NULL
  ),
  (
    'P',
    'P:21',
    'calculated concentration model parameter',
    NULL
  ),
  ('P', 'P:22', 'sensor cleanliness ratio', NULL),
  (
    'P',
    'P:pressure',
    'pressure',
    'Final pressure field; unit not specified'
  ) ON DUPLICATE KEY
UPDATE documented_name =
VALUES
  (documented_name),
  description =
VALUES
  (description);