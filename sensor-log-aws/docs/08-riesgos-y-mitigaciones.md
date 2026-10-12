# 8. Mitigación de riesgos críticos y fiabilidad

| Riesgo | Mitigación propuesta | Verificación |
|---|---|---|
| Archivos maliciosos o exploits embebidos en logs | Aislar el bucket de entrada y analizar archivos antes del procesamiento. Evaluar Amazon GuardDuty Malware Protection for S3 o un escáner dedicado, por ejemplo ClamAV ejecutado en un entorno aislado. | Probar archivos benignos, archivos de prueba de malware y fallos del escáner; confirmar que el procesador no lee archivos no aprobados. |
| Archivos corruptos o malformados (*poison pills*) | Desacoplar con SQS, limitar reintentos y enviar fallos persistentes a una DLQ. Validar esquema, tamaño y contenido antes de persistir. | Enviar archivos inválidos y comprobar aislamiento, alertas y reprocesamiento. |
| Denegación de servicio o agotamiento de recursos por cargas masivas | Limitar tamaño de archivo en la capa de API y durante la carga; aplicar cuotas, control de concurrencia y AWS WAF/limitación de tasa donde corresponda. | Pruebas de carga y verificación de límites y costos. |
| Pérdida de datos | Versionado y políticas de recuperación en S3; backups de base de datos; replicación regional si el RPO/RTO lo requiere. | Simulacros de restauración y medición de RPO/RTO. |
| Acceso cruzado entre clientes | Validar JWT, derivar el tenant desde la identidad validada y aplicar filtros obligatorios/RLS o claves de partición. | Pruebas negativas entre tenants para cada endpoint y operación. |
| Exposición de credenciales | AWS Secrets Manager, roles IAM de mínimo privilegio, rotación y redacción de logs. | Escaneo de repositorio y pruebas de permisos. |
| Caída del servicio y costos inesperados (*denial of wallet*) | Cuotas, límites de tamaño y concurrencia, alarmas de costo, presupuestos y límites de reintentos. | Pruebas de carga y revisión de alarmas de presupuesto y uso. |

## Aclaración sobre los servicios de inspección

AWS Storage Gateway no es, por sí mismo, un antivirus ni un servicio general de análisis de malware. Para inspeccionar objetos en S3, evaluar **GuardDuty Malware Protection for S3** o un flujo con un escáner dedicado. La selección depende de la región, los requisitos de detección, el costo y el flujo de cuarentena.

## Criterios de aceptación de seguridad

- [ ] Los objetos de entrada no son públicos.
- [ ] La API verifica tokens y autorización en cada solicitud.
- [ ] Los clientes no pueden acceder a datos de otros tenants.
- [ ] Los archivos se validan antes de ser procesados.
- [ ] Los fallos persistentes terminan en DLQ y generan alertas.
- [ ] Los secretos no están en el repositorio ni en los logs.
- [ ] Los datos se cifran en tránsito y en reposo.
- [ ] Existen backups y se han probado restauraciones.
- [ ] Hay límites de tamaño, concurrencia y costo.
- [ ] Los despliegues pueden verificarse y revertirse.
