
---

## 📄 Contenido del challenge (resumen)

### Question 1 — Mechanical Design Task: SRD Mounting Accessory

**Escenario:** Diseñar un accesorio de montaje que garantice instalación correcta y
posicionamiento repetible del sensor SRD en una línea de 2" NPT, respetando la
orientación fluid-end, el balance térmico del sensor y las constraints del datasheet.

**Requerimiento básico**
- Modelo 3D CAD del accesorio de montaje (entregable: STEP).
- Justificar la selección de variante del sensor y definir condiciones de operación.
- Planos 2D de fabricación.
- Documentar decisiones clave: alineación, sellado, consideraciones higiénicas.

**Bonus**
- Consideraciones DFM (justificar método de fabricación).
- Tolerancias y callouts adicionales en el plano 2D.
- Estrategia de revisión básica para el ciclo de vida PDM.

**Entregables:** STEP, planos 2D, notas de diseño concisas.

---

### Question 2 — Python Data Processing: Raw Equipment Logs

**Escenario:** Desarrollar un backend que transforme logs crudos (A-LOG y P-LOG)
en datos estructurados, siguiendo el documento `Sensor_Log_Parsing_Logic.PDF`.

**Requerimiento básico**
- Parsear logs crudos a un formato estructurado (p. ej. DataFrame de pandas).
- Limpiar entradas malformadas o incompletas.
- Extraer: timestamp, identificación sensor/electrónica, status/errores y valores
  de medición.
- Salida estructurada (CSV u otro formato serializado documentado).

**Bonus**
- Detección de anomalías o identificación de tendencias.
- Código modular y escalable (separación parsing / análisis).
- Ejemplos de unit tests o lógica de validación.

**Entregables:** código Python, instrucciones de setup/dependencias, dataset de salida.

---

### Question 3 — Tauri Application: Log Analysis Tool

**Escenario:** Herramienta de escritorio para ingenieros de soporte que reutilice
el backend de la Q2 y permita inspeccionar logs de equipos de forma repetible.

**Requerimiento básico**
- App Tauri que cargue archivos de log crudos.
- Use el backend de parsing de la Q2.
- Muestre resúmenes de log claros y comprensibles.

**Bonus**
- Separación modular UI / lógica de backend.
- Visualización (gráficos básicos) con selección de parámetros.
- Empaquetado o estructura de build/deployment definida.
- Mantenibilidad y extensibilidad a largo plazo.

**Entregables:** proyecto Tauri completo, instrucciones de build/run, video demo
(1–3 min), instalador/ejecutable (opcional).

---

### Question 4 — SQL & Systems Modeling: Sensor Log Database

**Escenario:** Diseñar un modelo relacional para almacenar y consultar los datos
parseados de la Q2, con foco en análisis futuro, reportes e integración con otras
aplicaciones Rheonics.

**Requerimiento básico**
- Esquema relacional con tablas, relaciones, PKs y FKs.
- Debe soportar: sensores, electrónicas, archivos/logs importados, mediciones,
  status/errores. Tablas adicionales permitidas.
- Consultas SQL para:
  1. Mediciones de un sensor en un rango de tiempo.
  2. Errores/status agrupados por serial de sensor o electrónica.
  3. Últimas mediciones y status por sensor.
- Explicar brevemente las decisiones de diseño y supuestos.

**Bonus**
- Método para almacenar grandes volúmenes de mediciones time-series.
- Flujo de ingesta automatizado desde archivo subido hasta BD.
- Índices u otras mejoras para performance y escalabilidad.

**Entregables:** DDL/SQL en archivo `.sql`, ER diagram o representación equivalente,
notas de diseño.

> Este repositorio implementa la Q4 en [`Q4_sql_database/`](./Q4_sql_database/).
> Ver `database.md` para la especificación completa, DDL canónico y consultas.

---

### Question 5 — Cloud & Application Security: Deployment Approach

**Escenario:** Aplicación Rheonics que recibe logs de clientes. Los archivos se
almacenan, procesan por un backend y se exponen solo a usuarios autorizados.
Se puede usar AWS u otra nube.

**Requerimiento básico (sin implementación, solo enfoque paso a paso)**
- Arquitectura de alto nivel y flujo desde upload hasta resultados/reportes.
- Dónde almacenar archivos crudos, datos estructurados y reportes, y por qué.
- Gestión y protección de API keys, passwords, credenciales y secretos.
- Autenticación de usuarios y restricción de acceso a datos de cliente/internos.
- Protección de datos en tránsito y en reposo.
- Medidas básicas de logging, monitoreo, backup y recuperación.

**Bonus**
- Mapear el enfoque a servicios AWS concretos.
- Estrategia CI/CD y de entornos (dev, testing, prod).
- 2–3 riesgos de seguridad o confiabilidad y cómo mitigarlos.

**Entregables:** PDF, DOCX o TXT con la respuesta paso a paso, incluyendo diagrama
de arquitectura si se elaboró.

---

## 📦 Entregables globales del challenge

| Q | Entregable | Formato |
|---|---|---|
| 1 | STEP + planos 2D + notas de diseño | `.step`, `.pdf`/`.dxf`, `.md` |
| 2 | Código Python + instrucciones + dataset de salida | `.py`, `.md`, `.csv`/`.parquet` |
| 3 | Proyecto Tauri + instrucciones + video demo + instalador (opcional) | `.zip`/repo, `.md`, `.mp4`, binario |
| 4 | DDL + queries + ER + notas de diseño | `.sql`, `.png`/`.md`, `.md` |
| 5 | Respuesta paso a paso + diagrama de arquitectura | `.pdf`/`.docx`/`.txt`, `.png` |

> Los links al repositorio son bienvenidos pero opcionales. Si se entrega un repo
> Git, los archivos de salida solicitados igual deben incluirse en el ZIP enviado
> a Rheonics, salvo acuerdo previo.

---

## 🤖 Supuestos y asistencia IA

Tal como pide el challenge, se documenta lo siguiente:

- **Supuestos generales:** ver el README de cada pregunta. Cada decisión técnica
  relevante está justificada en su sección de "Assumptions" / "Design decisions".
- **Asistencia IA utilizada:** ChatGPT/Claude/otros fueron usados como apoyo para
  revisión de sintaxis SQL, generación de documentación y validación de
  consistencia entre archivos. Todo el código fue revisado, ejecutado y validado
  manualmente antes de su inclusión.
- **Librerías y herramientas externas:** listadas por pregunta en el README
  correspondiente (por ejemplo: MySQL 8.0.16+, Python 3.11+, Tauri 2.x,
  pandas, pydantic, etc.).

---

