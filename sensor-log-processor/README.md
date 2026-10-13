# Setup y dependencias — `sensor-log-processor`

Motor Python para procesar archivos Rheonics `A-LOG` y `P-LOG`, validar registros, exportar CSV y generar figuras/análisis para el visualizador de escritorio.

## 1. Requisitos previos

- **Python 3.10 o posterior**.
- `pip` y `venv` (incluidos normalmente con Python).
- Una terminal **Bash** (Git Bash o WSL en Windows; Bash en Linux/macOS).
- Si se integrará con `sensor-log-visualizer`, tener también instalado el entorno de compilación de Tauri 2/Rust en el proyecto del visualizador. Es una dependencia de la aplicación de escritorio, no de este motor Python.

Comprueba las versiones:

```bash
python --version
python -m pip --version
```

Si `python` no está disponible en tu terminal, prueba `python3`.

## 2. Crear y activar el entorno virtual

Desde la carpeta raíz del repositorio:

```bash
cd sensor-log-processor
python -m venv .venv
source .venv/Scripts/activate
```

En Linux/macOS/WSL, usa en su lugar:

```bash
source .venv/bin/activate
```

Actualiza `pip`:

```bash
python -m pip install --upgrade pip
```

> En Windows, ejecuta los comandos de activación de `Scripts` desde Git Bash. Si el entorno se creó desde WSL, activa el entorno con `source .venv/bin/activate`.

## 3. Instalar dependencias

Dependencias de ejecución declaradas en `requirements.txt`:

- `pandas>=2.0`: lectura, transformación y exportación de datos tabulares.
- `plotly>=5.20`: generación de figuras serializables para el visualizador.
- `numpy`: usado directamente por los módulos de análisis y visualización; actualmente suele instalarse como dependencia de `pandas`, pero conviene declararlo explícitamente en `requirements.txt`.

Instalación:

```bash
python -m pip install -r requirements.txt
```

Para instalar también las dependencias de pruebas (`pytest`, `pytest-cov` y `pytest-mock`):

```bash
python -m pip install -r requirements-dev.txt
```

Si se desea declarar explícitamente NumPy, añade esta línea a `requirements.txt`:

```text
numpy>=1.24
```

## 4. Estructura relevante

```text
sensor-log-processor/
├── data/
│   ├── input/                 # Archivos LOG de entrada
│   └── output/                # CSV generados
├── src/
│   ├── constants/             # Constantes de A-LOG y P-LOG
│   ├── parsers/               # Parsers de cada formato
│   ├── validation/            # Validación y resumen de registros
│   ├── service/
│   │   └── log_processing.py  # API de procesamiento: process_log()
│   ├── plotting/              # Catálogo y generación de figuras Plotly
│   ├── analytics/             # Tendencias y detección de anomalías
│   └── main.py                # Ejecución de muestras de ejemplo
├── tests/                     # Pruebas automatizadas
├── requirements.txt
├── requirements-dev.txt
└── pytest.ini
```

## 5. Ejecutar el procesamiento de ejemplo

El programa principal procesa estos archivos:

- `data/input/SAMPLE-A.LOG`
- `data/input/SAMPLE-P.LOG`

Genera los CSV correspondientes en `data/output/`.

Desde la raíz del proyecto, con el entorno virtual activo:

```bash
python -m src.main
```

El programa muestra el resumen de validación, el número de registros y la ruta del CSV generado. Para procesar otros archivos desde una integración o un script, la función pública está en `src.service.log_processing`:

```python
from src.service.log_processing import process_log

result = process_log("ruta/al/archivo.LOG", "A-LOG")
# Para archivos P-LOG, usa "P-LOG".
```

El resultado incluye el tipo y nombre del archivo, el total de registros, los conteos de registros válidos e inválidos, las columnas y los registros serializables.

## 6. Ejecutar las pruebas

Instala las dependencias de desarrollo y ejecuta:

```bash
python -m pytest
```

Para generar un reporte de cobertura en la terminal:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## 7. Integración con `sensor-log-visualizer` (Tauri)

El visualizador y el procesador son proyectos separados. El código Rust/Tauri debe invocar Python apuntando a esta carpeta.

En la integración existente, configura `SENSOR_LOG_PROCESSOR_DIR` con la **ruta absoluta** a la raíz de `sensor-log-processor`. Por ejemplo, desde Bash:

```bash
export SENSOR_LOG_PROCESSOR_DIR="/ruta/absoluta/sensor-log-processor"
```

La integración puede priorizar el intérprete del entorno virtual:

- Windows: `.venv/Scripts/python.exe`
- Linux/macOS: `.venv/bin/python`

Si la integración ejecuta `desktop_runner.py`, verifica que ese archivo exista en la versión del proyecto que estás usando; no aparece en la estructura incluida en este paquete. No asumas que el comando de integración funciona hasta confirmar que el runner está presente y que el código Tauri apunta a la ruta correcta.

Mantén los CSV procesados en `desktop-output` cuando así lo requiera el visualizador; esa ubicación corresponde al flujo de integración de escritorio y es distinta de `data/output`, usada por el procesamiento de ejemplo.

## 8. Solución de problemas

### `ModuleNotFoundError`

Comprueba que el entorno virtual está activo y vuelve a instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

### No se encuentra el archivo LOG

Verifica la ruta y el nombre exacto del archivo. El programa de ejemplo espera `SAMPLE-A.LOG` y `SAMPLE-P.LOG` dentro de `data/input/`.

### No se genera el CSV

Ejecuta `python -m src.main` desde la raíz del repositorio y revisa los mensajes de error. Comprueba que `data/input/` contiene los archivos de ejemplo y que `data/output/` tiene permisos de escritura.

### Las pruebas no encuentran módulos

Ejecuta `python -m pytest` desde la raíz del repositorio. El archivo `pytest.ini` configura `pythonpath = .`.

## 9. Dependencias resumidas

| Paquete | Uso | Tipo |
|---|---|---|
| `pandas>=2.0` | DataFrames, importación/exportación CSV | Ejecución |
| `plotly>=5.20` | Figuras interactivas serializadas a JSON | Ejecución |
| `numpy` | Cálculos numéricos y análisis de series | Ejecución directa recomendada |
| `pytest>=8.0` | Pruebas automatizadas | Desarrollo |
| `pytest-cov>=5.0` | Cobertura de pruebas | Desarrollo |
| `pytest-mock>=3.12` | Utilidades de mocking para pruebas | Desarrollo |
