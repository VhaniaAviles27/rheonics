# 3. Gestión de secretos y credenciales

## Objetivo

Evitar que credenciales de bases de datos, tokens de APIs externas y claves privadas queden expuestos en el código fuente, archivos de configuración o registros de ejecución.

## Propuesta

- Almacenar los secretos en **AWS Secrets Manager**.
- Asignar al servicio de procesamiento un rol IAM que permita leer únicamente los secretos que necesita.
- Recuperar los secretos en tiempo de ejecución mediante el SDK de AWS, o utilizar un mecanismo de caché seguro cuando sea apropiado.
- Habilitar rotación automática cuando el tipo de secreto y el sistema dependiente la soporten.
- Cifrar los secretos con AWS KMS y limitar quién puede administrar las claves.
- Evitar imprimir secretos, tokens o cadenas de conexión en logs y mensajes de error.

## Flujo

1. El servicio se ejecuta con un rol IAM, sin credenciales AWS estáticas embebidas.
2. El rol solicita acceso al secreto específico.
3. Secrets Manager devuelve el valor autorizado.
4. El servicio usa el secreto para conectarse al recurso.
5. La rotación y la renovación de conexiones se prueban para evitar interrupciones.

## Lista de verificación

- [ ] No hay secretos en el repositorio ni en imágenes de contenedor.
- [ ] Los permisos IAM siguen el principio de mínimo privilegio.
- [ ] Los secretos están separados por ambiente.
- [ ] La rotación está habilitada o documentada como no aplicable.
- [ ] Los logs ocultan credenciales y datos sensibles.
- [ ] Existe un procedimiento de revocación y respuesta ante exposición.
