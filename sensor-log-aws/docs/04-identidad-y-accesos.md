# 4. Autenticación, autorización y control de accesos

## Autenticación (AuthN)

Se propone **Amazon Cognito User Pools** para gestionar el inicio de sesión, recuperación de contraseñas y autenticación multifactor (MFA), según el nivel de riesgo y las necesidades de los usuarios.

## Autorización (AuthZ)

Tras la autenticación, el cliente obtiene tokens. La API debe validar firma, emisor, audiencia, expiración y demás atributos relevantes del JWT antes de aceptar la solicitud.

La autenticación confirma quién es el usuario; la autorización determina qué recursos puede consultar o modificar.

## Aislamiento entre clientes

Para evitar que un cliente acceda a datos de otro:

1. Obtener `tenant_id` o `customer_id` de una identidad o atributo validado por el backend.
2. No confiar en el identificador de cliente enviado libremente en el cuerpo o query string.
3. Aplicar el filtro de tenant en todas las consultas y operaciones.
4. En PostgreSQL, considerar Row-Level Security (RLS) como defensa adicional.
5. En DynamoDB, diseñar claves y políticas de acceso que reflejen el aislamiento requerido.
6. Probar explícitamente escenarios de acceso cruzado entre tenants.

## Controles complementarios

- Aplicar permisos IAM de mínimo privilegio a servicios y recursos.
- Usar MFA para usuarios y controles reforzados para administradores.
- Separar roles de usuario, operador, soporte y administrador.
- Registrar eventos de autenticación y accesos relevantes, sin incluir tokens completos.
- Definir expiración, renovación y revocación de sesiones según el riesgo.
