# 7. Estrategia de entornos y CI/CD

## Separación de ambientes

Se propone separar Desarrollo (Dev), Pruebas (Staging/QA) y Producción (Prod). Para un aislamiento más fuerte, evaluar una arquitectura multicuenta con **AWS Organizations**.

Cada ambiente debe contar con permisos, secretos, datos y recursos propios. Evitar utilizar datos reales de producción en ambientes inferiores salvo autorización y controles de anonimización.

## Infraestructura como código (IaC)

Definir la infraestructura mediante **AWS CDK** o **Terraform** para facilitar la revisión, repetibilidad y trazabilidad de los cambios.

- Revisar cambios de infraestructura mediante pull requests.
- Ejecutar validaciones estáticas y análisis de seguridad.
- Evitar cambios manuales no registrados en el código de infraestructura.
- Separar estado, variables y secretos por ambiente.

## Pipeline propuesto

Puede implementarse con AWS CodePipeline o GitHub Actions.

1. Al integrar cambios en `main`, ejecutar pruebas unitarias y análisis estático.
2. Construir y verificar el artefacto del backend.
3. Validar y sintetizar la infraestructura como código.
4. Desplegar automáticamente en Staging.
5. Ejecutar pruebas de integración y controles de seguridad.
6. Requerir aprobación para promover a Producción.
7. Desplegar con una estrategia progresiva, como Canary o Blue/Green, cuando el servicio y la infraestructura lo permitan.
8. Verificar métricas y permitir rollback ante una degradación.

## Seguridad del pipeline

- Utilizar credenciales de corta duración y roles con permisos mínimos.
- Proteger ramas y exigir revisión de cambios.
- Escanear dependencias e imágenes de contenedor.
- No exponer secretos en logs.
- Mantener trazabilidad entre commit, artefacto y despliegue.
- Proteger el pipeline de producción con aprobaciones y permisos separados.
