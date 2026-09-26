# Organización del desarrollo

## Metodología acordada para continuar

Desarrollo incremental por etapas, con un tablero Kanban sencillo: Pendiente → Definido → En desarrollo → En pruebas → Revisión del negocio → Terminado. No estamos usando Scrum formal: no hay sprints, ceremonias ni cargos de Scrum establecidos.

Cada tarea debe describir el problema, el comportamiento esperado, el alcance, permisos afectados, criterios de aceptación y pruebas. Carlo valida las reglas del negocio y la experiencia; el asistente implementa, documenta y verifica. Los errores pequeños pueden resolverse directamente, pero las reglas comerciales nuevas deben quedar registradas.

Una etapa termina cuando sus entregables y criterios están revisados, no solo cuando sus pantallas existen. Las funciones adelantadas de E5 (apartados y reparaciones) permanecen registradas como ampliaciones de E1; no eliminan requisitos pendientes de la primera puesta en operación.

## Arquitectura real

Actualmente hay un proceso Python que sirve tres interfaces en puertos locales separados. PostgreSQL es la autoridad central y cada POS utiliza SQLite para su estado local y su cola. El navegador consume la API; nunca recibe credenciales PostgreSQL. Apartados y reparaciones operativos requieren conexión según su implementación actual.

Estructura vigente:

```text
lab/e1/
  server.py              Rutas HTTP y autorización de solicitudes
  core.py                Servicios centrales, POS y reglas fundamentales
  extensions.py          Catálogo y correcciones
  order_service.py       Apartados, reparaciones y sus movimientos
  cash_reports.py        Informes de cajas
  simulated.py           Historial ficticio
  pg.py                  Acceso PostgreSQL
  schema-postgresql.sql  Esquema del laboratorio
  branding.py            Identidad de los comprobantes
  orders_preview.py      Comprobantes de órdenes
  receipt_view.py        Conversión a vista imprimible
  static/                Dashboard, dos POS, estilos y recursos
  tests/                 Pruebas de integración y cálculos
  data/                  Estado privado, nunca versionado
docs/                    Requisitos, decisiones, etapas y verificación
scripts/maintenance/     Operaciones de mantenimiento explícitas
prototype/               Maqueta histórica E0
database/                Base experimental anterior a E1
```

Conservamos estas rutas en esta reorganización porque el servicio local, las pruebas y recursos dependen de ellas. Organización no significa mover archivos de golpe. En una tarea posterior separaremos gradualmente `core.py` y `extensions.py` por dominio con pruebas de regresión.

## Framework: qué usamos y qué proponemos

**No usamos React, Vue, Django, Flask ni FastAPI actualmente.** La interfaz usa JavaScript puro y el servidor usa `http.server` de Python. ReportLab y Psycopg son bibliotecas, no frameworks web. Docker ejecuta la base; no es un framework.

La decisión inmediata es conservar este stack para terminar de validar E1. Antes del despliegue operativo debe sustituirse el servidor de laboratorio por una solución de servicio apropiada. Propuesta para evaluar en E2: FastAPI para contratos y validación de API, manteniendo las reglas de negocio separadas del transporte HTTP. Esta migración no está implementada ni aprobada por el hecho de documentarla. No hace falta reescribir la interfaz en React para organizar el proyecto; se valorará solo si la complejidad lo justifica.

Objetivo: monolito modular, no microservicios. Módulos lógicos de identidad/permisos, catálogo/inventario, ventas/pagos, cajas, órdenes, informes, comprobantes y sincronización. Una función nueva debería tocar su módulo y usar contratos explícitos, evitando dependencias circulares y reglas repetidas en interfaz y servidor.

## Git y GitHub

Git guarda versiones locales; GitHub hospeda el repositorio y facilita revisión e incidencias. Proponemos `main` estable y ramas cortas `feat/...`, `fix/...` o `docs/...`. Cada cambio tiene un commit descriptivo y, cuando corresponda, una pull request que explica resultado, validación y límites. No hace falta una rama permanente `develop` para este equipo.

Un repositorio privado permite trabajar sin publicar el código comercial. Publicar código no despliega el POS ni publica la base de datos. El acceso a GitHub se hace con autenticación oficial del usuario; no guardar tokens en el proyecto ni compartir contraseñas por chat.

## Próximos trabajos organizativos

1. Revisar la puerta de salida de E1 contra los requisitos, incluyendo ampliaciones.
2. Registrar tareas E2 con aceptación verificable y decidir el framework del servicio.
3. Introducir migraciones versionadas para el esquema vigente y estrategia de reversión/respaldos.
4. Separar dominios progresivamente y añadir integración continua en un entorno desechable reproducible.
5. Definir despliegue, secretos, recuperación y pruebas en dos equipos antes de operar.
