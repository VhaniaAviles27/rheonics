# Deliverables

This repository contains four components covering data processing, desktop visualization, database design, and cloud deployment.

---

## 2. Python Data Processing — `sensor-log-processor`

Python engine for processing raw Rheonics equipment logs (`A-LOG` and `P-LOG`).

**Source code:** [Browse `sensor-log-processor`](sensor-log-processor/)

### Output Datasets

| File | Description |
|---|---|
| [SAMPLE-A.CSV](https://github.com/user-attachments/files/33363788/SAMPLE-A.CSV) | Processed A-LOG sample data |
| [SAMPLE-P.CSV](https://github.com/user-attachments/files/33363791/SAMPLE-P.CSV) | Processed P-LOG sample data |

### Setup and Dependencies

See the [Setup and Installation Guide](sensor-log-processor/README.md) for prerequisites, dependency installation, execution instructions, and testing.

---

## 3. Desktop Application — `sensor-log-visualizer`

Tauri desktop application for visualizing and analyzing processed sensor log data.

**Source code:** [Browse `sensor-log-visualizer`](sensor-log-visualizer/)

### Demo

[▶ Watch the Application Demo](https://github.com/user-attachments/assets/a39fcd19-31d7-40a1-8d74-f2ba51820a3b)

---

## 4. Database Design — `sensor-log-database`

Relational database design and SQL implementation for the sensor log processing system.

- **Documentation:** [Browse `sensor-log-database`](sensor-log-database/)
- **DDL Script:** [View `DDL.sql`](sensor-log-database/DDL.sql)

### Entity-Relationship Diagram

<details>
<summary>View ER Diagram</summary>

![Sensor Log Database ER Diagram](https://github.com/user-attachments/assets/1185ce77-4d8e-4772-9ccb-5f6203220933)

</details>

**Editable diagram:** [Open the ER Diagram in Lucidchart](https://lucid.app/lucidchart/3d6e077d-c263-4975-84fd-42c6b860d02d/edit?page=0_0&invitationId=inv_3f1bc463-86cd-4a2b-9691-7e9aa2fb706b#)

---

## 5. Cloud Architecture & Security — `sensor-log-aws`

AWS cloud deployment approach and application security architecture.

**Documentation:** [Browse `sensor-log-aws`](sensor-log-aws/)

---
