# Rheonics Logs — Esquema SQL normalizado

Motor previsto: **MySQL 8.0.16+**.
Documentación funcional completa: [`database.md`](./database.md).

## Modelo

14 tablas normalizadas que separan identidad de equipos, archivos, ingestas,
muestras crudas, mediciones y errores.

| # | Tabla | Propósito |
|---:|---|---|
| 1 | `sensors` | Identidad del sensor. |
| 2 | `electronics` | Identidad de la electrónica/controlador. |
| 3 | `firmware_versions` | Catálogo de versiones de firmware. |
| 4 | `units` | Catálogo de unidades confirmadas. |
| 5 | `log_files` | Contenido por SHA-256 (deduplicación). |
| 6 | `log_file_receipts` | Cada recepción física de un archivo. |
| 7 | `catalog_codes` | Códigos de estado/error/calidad por formato y componente. |
| 8 | `electronic_sensor_history` | Historial temporal sensor–electrónica. |
| 9 | `measurement_types` | Catálogo de variables A-LOG y P-LOG. |
| 10 | `import_logs` | Cada intento de procesar una recepción. |
| 11 | `samples` | Una fila por línea del archivo. |
| 12 | `measurements` | Valores por muestra/tipo/canal. |
| 13 | `status_events` | Ocurrencias de códigos por muestra. |
| 14 | `ingestion_errors` | Errores por etapa del pipeline. |

## Orden de ejecución

Ejecutar en una base vacía, en este orden exacto (respeta dependencias FK):

1.  `00_create_database.sql`
2.  `01_sensors.sql`
3.  `02_electronics.sql`
4.  `03_firmware_versions.sql`
5.  `04_units.sql`
6.  `05_log_files.sql`
7.  `06_log_file_receipts.sql`
8.  `07_catalog_codes.sql`
9.  `08_electronic_sensor_history.sql`
10. `09_measurement_types.sql`
11. `10_import_logs.sql`
12. `11_samples.sql`
13. `12_measurements.sql`
14. `13_status_events.sql`
15. `14_ingestion_errors.sql`
16. `15_seed_measurement_types.sql`
17. `16_seed_catalog_codes.sql`

## Convenciones

- Tablas en plural, columnas en `snake_case`, PKs `*_id`.
- `ENGINE=InnoDB`, `CHARSET=utf8mb4`, `COLLATE=utf8mb4_0900_ai_ci`.
- ENUMs siempre en MAYÚSCULAS y con los mismos literales en SQL, documentación y código de ingesta.
- `DATETIME(6)` para timestamps de dominio; `TIMESTAMP(6)` para timestamps meta.
- Los códigos se guardan como `VARCHAR` para preservar ceros iniciales.
- Hash SHA-256 normalizado a minúsculas antes del `INSERT`.

## Ejecución rápida

```bash
mysql -u root -p < 00_create_database.sql
for f in 0*.sql 1*.sql; do
  echo "==> $f"
  mysql -u root -p rheonics_logs < "$f" || break
done

## Link E-R Diagram

[Ver diagrama E-R en Lucidchart](https://lucid.app/lucidchart/3d6e077d-c263-4975-84fd-42c6b860d02d/edit?viewport_loc=-391%2C-411%2C3611%2C1923%2C0_0&invitationId=inv_3f1bc463-86cd-4a2b-9691-7e9aa2fb706b)