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
  core.py                Exportaciones de compatibilidad para consumidores anteriores
  central.py             Coordinación del servicio central y recepción de eventos
  store.py               Operación local del POS
  identity.py            Usuarios, autenticación, roles y permisos
  sales.py               Validación y cálculo de ventas
  cash.py                Estado y resumen de la caja abierta
  synchronization.py     Envío y recepción de cambios del POS
  local_storage.py       Persistencia SQLite y respaldos locales
  domain.py              Validaciones y conversiones comunes
  defaults.py            Permisos y datos iniciales
  receipts.py            Plantilla y generación de tickets
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

La separación de `core.py` está implementada. El archivo conserva las exportaciones anteriores para no romper scripts ni pruebas; los módulos de producción importan directamente el dominio que utilizan. `central.py` y `store.py` coordinan los servicios, mientras identidad, cálculos, persistencia, comprobantes y sincronización tienen archivos propios. Continúa pendiente reducir las responsabilidades de `extensions.py` conforme evolucione el catálogo y las correcciones.

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

## Ajustes de E1 del 28 de septiembre de 2026

- Categoría y material son atributos independientes del artículo: por ejemplo, Anillos → Colección y material Plata. Categorías muestra los materiales presentes en sus artículos y descendientes; no impone un único metal a toda una categoría.
- Los reportes de artículos y categorías permiten combinar ambos filtros. Tabla, gráfica y exportación usan las mismas partidas filtradas. En ventas sin clasificación histórica registrada se consulta el catálogo actual; un cambio posterior del material puede modificar ese desglose histórico.
- El permiso `cash_summary` permite consultar cantidades de ventas e importes aplicados por efectivo, tarjeta y transferencia, además del efectivo teórico de la caja abierta. Se habilita inicialmente solo para admin y puede editarse por rol. El servicio omite ese resumen para usuarios sin permiso. Sin conexión se conserva la última autorización descargada.
- Una venta mixta cuenta en cada método que utiliza, pero una sola vez en el total de ventas. Los anticipos y abonos de órdenes se muestran aparte; las correcciones actualizan el resumen. El cierre ciego se conserva para quienes no pueden consultar el resumen.
- La corrección de vendedores reutiliza el selector de cobro: menú, fichas removibles y captura del código del empleado. La selección se aplica al confirmar la corrección con su motivo y permisos correspondientes.

Validación: 39 pruebas Python de integración/regresión y suites JavaScript de reportes y órdenes; revisión de interfaz en navegador. Las pruebas de integración usan bases desechables.

### Corrección de piezas desde el POS y dashboard

El reemplazo vinculado muestra únicamente las partidas de la venta y permite buscar una pieza nueva por nombre o código. Cada fila conserva la pieza anterior y presenta la seleccionada con cantidad editable. También permite agregar, quitar y restaurar partidas; las cantidades del mismo producto se agrupan antes de solicitar la validación al servidor. La comparación incluye la lista anterior y la nueva; no modifica datos hasta confirmar. El selector de vendedores comparte componente con el cobro. Se versionaron los recursos de estas pantallas para renovar los archivos al recargarlas.

Verificación: búsqueda y sustitución con cantidad distinta, comparación validada por el servidor y cancelación desde el POS sin alterar la venta consultada; prueba de integración de reemplazos, inventario y atomicidad.

### Venta fuera de inventario: código 99

En Nueva venta, escribir `99` y pulsar Enter (o elegir el botón del resultado) abre la captura de categoría/subcategoría, descripción, precio unitario y cantidad. Requiere el permiso normal de vender. La partida tiene un identificador único y código visible 99; conserva la clasificación y descripción en la venta. Admite carrito mixto, descuentos existentes, pagos y vendedores. No crea productos ni movimientos de existencias, tampoco al anularla o reemplazarla. El costo y material no se inventan: los reportes indican costo no disponible y permiten encontrarla bajo material sin registrar. Funciona con las categorías previamente descargadas cuando se trabaja sin conexión.

Verificación específica: venta mixta sin conexión, sincronización, ticket PDF, reemplazo y anulación sin movimientos de inventario para el 99, rechazo de descripción vacía/precio cero/categoría inexistente y reportes por categoría/artículo. Revisión del formulario y el cobro en navegador sin confirmar ventas de prueba en la base de uso habitual.

### Cambios comerciales

Se incorpora `lab/e1/exchanges.py` y `static/exchanges.js` para cambios online desde el POS, con diferencias cobradas en la caja actual, trazabilidad y avisos administrativos por piezas 99 sin ingreso a inventario. Véanse las reglas y evidencias en [Cambios de mercancía](e1/cambios-mercancia.md). Esta ampliación adelanta parte de E6; no completa automáticamente las demás dependencias y requisitos de esa etapa.

Los identificadores públicos de ventas y cambios se resuelven en `lab/e1/folios.py`. Su contrato offline, migración y límites se documentan en `docs/e1/cambios-mercancia.md`. Los UUID siguen siendo las claves internas.
