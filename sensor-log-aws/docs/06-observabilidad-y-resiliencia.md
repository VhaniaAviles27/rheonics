# 6. Observabilidad, monitoreo y resiliencia

## Logs, métricas y trazas

- Centralizar logs de aplicación y servicios en **Amazon CloudWatch Logs**.
- Crear métricas para archivos recibidos, procesados, rechazados y fallidos; duración del procesamiento y profundidad/antigüedad de mensajes en SQS.
- Configurar CloudWatch Alarms para detectar fallos y retrasos.
- Como umbral inicial propuesto, alertar si la tasa de errores de procesamiento supera el **1 %**. Validar el umbral con el volumen real y los objetivos de servicio.
- Utilizar **AWS X-Ray** u otra solución compatible de trazabilidad distribuida para localizar cuellos de botella y seguir el recorrido de una solicitud.
- Enviar alertas mediante Amazon SNS a los canales operativos aprobados (por ejemplo, correo o integración con herramientas de ingeniería).

## Reintentos y mensajes fallidos

Se recomienda desacoplar los eventos de S3 mediante una cola Amazon SQS.

- Configurar una política de reintentos adecuada.
- Tras el número de intentos definido —tres es el valor inicial propuesto—, enviar el mensaje a una **Dead Letter Queue (DLQ)**.
- Alertar cuando haya mensajes en la DLQ.
- Investigar los archivos fallidos de forma aislada y permitir su reprocesamiento controlado.
- Implementar idempotencia para que los reintentos no dupliquen resultados.

## Copias de seguridad y recuperación

- **S3:** evaluar versionado y Cross-Region Replication (CRR) según los requisitos de recuperación y cumplimiento.
- **RDS:** configurar backups automáticos y retención. Los 35 días son una propuesta inicial que debe validarse con la política de la organización.
- **DynamoDB:** habilitar recuperación a un punto en el tiempo (PITR) cuando se utilice.
- Definir RPO (pérdida de datos tolerable) y RTO (tiempo objetivo de recuperación).
- Probar periódicamente restauraciones y procedimientos de recuperación; no basta con que los backups estén habilitados.

## Indicadores operativos sugeridos

- Porcentaje de archivos procesados correctamente.
- Tasa de errores y reintentos.
- Antigüedad y profundidad de la cola.
- Tiempo desde la carga hasta la disponibilidad de resultados.
- Número de mensajes en DLQ.
- Coste por archivo procesado.
