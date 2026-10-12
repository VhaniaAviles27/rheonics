# 5. Protección de datos: en tránsito y en reposo

## Cifrado en tránsito

- Exigir HTTPS con TLS 1.2 o superior para tráfico hacia APIs y servicios de AWS.
- Configurar políticas de bucket de S3 que rechacen solicitudes sin transporte seguro (`aws:SecureTransport`).
- Evitar endpoints públicos innecesarios y evaluar VPC endpoints cuando aporten aislamiento y control.
- No incluir secretos o datos sensibles en URLs, parámetros de consulta ni mensajes de error.

## Cifrado en reposo

Habilitar cifrado para los buckets de S3, tablas de DynamoDB y recursos de RDS. La propuesta contempla AWS Key Management Service (AWS KMS) para administrar claves cuando se requiera control adicional.

Definir por ambiente:

- Tipo de clave y responsables de administración.
- Permisos para usar, administrar y auditar las claves.
- Política de rotación y respuesta ante compromiso.
- Requisitos de auditoría y retención.

La rotación anual de claves indicada en el diseño inicial debe confirmarse según el tipo de clave y la política corporativa; no todos los mecanismos de rotación se configuran del mismo modo.

## Minimización y exposición

- Guardar solo los datos necesarios para el propósito de procesamiento.
- Limitar el acceso a archivos brutos y reportes.
- Enmascarar información sensible en logs y métricas.
- Definir reglas de retención y eliminación verificable.
- Considerar clasificación de datos y requisitos legales o contractuales aplicables.
