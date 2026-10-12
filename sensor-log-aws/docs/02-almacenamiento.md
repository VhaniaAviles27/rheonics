# 2. Estrategias de almacenamiento

## Archivos brutos

Los archivos originales se almacenan en un bucket dedicado de Amazon S3, inicialmente en la clase **S3 Standard** cuando se necesita acceso frecuente y baja latencia.

Controles y operación:

- Bloquear el acceso público.
- Habilitar cifrado predeterminado y políticas que rechacen solicitudes sin TLS.
- Aplicar permisos mínimos por rol y prefijo.
- Considerar versionado para recuperación frente a sobrescrituras o borrados accidentales.
- Definir reglas de ciclo de vida. Como punto de partida, evaluar la transición a **S3 Glacier Flexible Retrieval después de 30 días**, siempre que la frecuencia de recuperación y los objetivos de recuperación lo permitan.
- Definir la retención y eliminación de acuerdo con los requisitos del negocio.

S3 ofrece una durabilidad de diseño de 99,999999999 % (11 nueves); esto no reemplaza la necesidad de configurar controles de acceso, versionado y recuperación apropiados.

## Datos estructurados

La elección entre Amazon DynamoDB y Amazon RDS for PostgreSQL depende de las consultas esperadas.

| Opción | Elegir cuando | Aspectos por evaluar |
|---|---|---|
| **Amazon DynamoDB** | Las consultas se resuelven principalmente por claves conocidas, como dispositivo y timestamp, con patrones de acceso previsibles. | Diseño de claves y GSIs, consultas ad hoc, consistencia y costos por capacidad/solicitud. |
| **Amazon RDS for PostgreSQL** | Se necesitan relaciones, joins, consultas SQL complejas, integridad relacional o integración con herramientas BI. | Índices, conexiones, escalado, alta disponibilidad y costos de operación. |

No es necesario utilizar ambas bases de datos de forma simultánea salvo que existan requisitos claros para ello.

## Reportes generados

Guardar los reportes en un bucket de S3 separado del bucket de entrada, con políticas de acceso restrictivas. Esto reduce el riesgo de que los archivos no confiables y los artefactos publicados compartan permisos o ciclos de vida.

## Convenciones sugeridas

- Separar por ambiente y, cuando corresponda, por cliente mediante prefijos o cuentas.
- No utilizar información sensible en nombres de objetos.
- Definir reglas de retención, versionado, recuperación y eliminación.
- Registrar el identificador del objeto y del procesamiento en la base de datos, evitando duplicar innecesariamente el archivo binario.
