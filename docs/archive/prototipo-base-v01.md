> **Actualización 25/09/2026:** laboratorio vigente con PostgreSQL central, dos POS y tres páginas: [E1](docs/e1/README.md). El documento inferior describe el prototipo histórico v0.1; no gobierna las reglas nuevas de inventario compartido.

# POS de joyería — base PostgreSQL v0.1

Primera implementación de desarrollo, 14 de septiembre de 2026. No está lista para operar las cajas del negocio.

## Qué está construido

PostgreSQL 18, instalado mediante imagen oficial fijada por digest. Base `pos_desarrollo`, esquema `pos`, 18 tablas y dos vistas de existencias. Tres migraciones SQL versionadas. Contenedor `pos-postgres-desarrollo`, volumen persistente `pos-postgres-desarrollo-data`. Sin puertos publicados en la red. Límite del contenedor: 768 MB. SQL Server de análisis permanece independiente.

- Dos sucursales, tres almacenes y cuatro ubicaciones: Coyoacán/Local 1, Coyoacán/Local 2, oficina y Santa Rosa.
- Productos con códigos de barras como texto, peso y precios decimales; categorías y personal.
- Terminales y sesiones de caja con apertura y campos de cierre. No se ha implementado todavía el cálculo completo del cierre, gastos, permisos ni autenticación.
- Ventas de mostrador con partidas y datos históricos de producto/precio/costo, pagos aplicados y vendedores participantes.
- Fecha/hora de operación con zona y recepción central por separado. El cliente debe enviar una fecha con desplazamiento explícito, por ejemplo `2026-09-14T09:43:21-06:00`.
- Libro de movimientos de inventario y vistas calculadas por ubicación y almacén. El total de Coyoacán suma ambos locales, sin repetir existencias.
- Recepción atómica e idempotente de ventas mediante `pos.receive_sale`: las operaciones repetidas con el mismo identificador y contenido devuelven el registro existente; cambiar contenido con ese mismo identificador produce error.
- Si llega una venta ya cobrada cuyo stock no concuerda, se conserva y crea una incidencia. Esta función recibe hechos ya ocurridos; no autoriza vender sin existencias.
- Correspondencias para futura migración; no se han importado los registros antiguos.

## Estado de los datos

Solo están cargadas las sucursales, almacenes, ubicaciones y medios efectivo/tarjeta. No hay productos, empleados, terminales ni ventas reales. No se repartieron automáticamente las existencias antiguas: se requiere conteo físico por local. Los tests usan bases desechables y registros ficticios.

Los nombres Local 1/Local 2 son provisionales. La ubicación de venta se obtiene de la terminal, no de un campo de almacén enviado libremente por el cliente. V1 admite una terminal por ubicación de venta. Si se agregan otras, será necesario un protocolo de asignación adicional o coordinación local.

## Uso local

Desde esta carpeta, con Python 3 y Docker:

```bash
python3 database/manage.py start
python3 database/manage.py status
python3 database/manage.py migrate
python3 database/tests/test_database.py
python3 database/manage.py backup
python3 database/tests/test_backup.py
python3 database/manage.py stop
```

`start` crea el contenedor si falta; en arranques posteriores conserva los datos. `migrate` solo aplica versiones pendientes. Detener el contenedor no borra el volumen. No ejecutar scripts SQL ya aplicados manualmente.

La contraseña de administración de este laboratorio está en `.postgres.env`, con permisos 0600 y excluida del control de versiones. No compartir ese archivo ni utilizar el superusuario desde una aplicación de usuarios. La imagen fijada requerirá actualizaciones planificadas para recibir correcciones.

Los respaldos de desarrollo se guardan en `backups/`. Se verificó la restauración en otra base. No son todavía una política de respaldo de producción ni tienen programación automática.

## Límites importantes antes de conectar el POS

1. **La cola local y la sincronización de dispositivos no están construidas.** Esta base implementa solo la recepción central de ventas. La computadora deberá guardar de forma durable el ticket completo y su identificador antes de imprimir, descontar su asignación local, reenviar hasta recibir confirmación y persistir el acuse.
2. **Asignación y transferencias:** las ubicaciones representan cantidades físicamente separadas. No hay aún una función aprobada para mover cupos entre dispositivos, traspasar mercancía, cargar conteos o ajustar negativos. Esas operaciones deben coordinar sincronización previa, origen/destino, recepción y auditoría. No insertar transferencias manualmente para operar el negocio; las columnas están reservadas para esa implementación.
3. **Seguridad:** el esquema no concede acceso público a tablas ni funciones. La aplicación necesitará un rol de privilegios mínimos, identidad de terminal autenticada, permisos de usuario y validación de descuentos. Nunca enviar credenciales PostgreSQL al navegador. La función no verifica todavía políticas comerciales de precio, descuento, terminal activa o vendedor autorizado; puede recibir operaciones antiguas de terminales desactivadas, cuya revisión corresponde al backend.
4. **Cajas:** faltan flujo de cierre, gastos, retiros, devoluciones y conciliación. Se permite recibir sesiones históricas con cierres aún pendientes de envío; el backend/local debe garantizar una sola sesión operativa por terminal.
5. **Cancelaciones:** ventas y movimientos confirmados no se editan ni borran mediante el flujo ordinario. Se requiere implementar operaciones compensatorias y sus reglas. Un administrador de base sigue teniendo privilegios de mantenimiento; los triggers no constituyen auditoría inviolable.
6. **Apartados y reparaciones:** deliberadamente fuera de esta versión, pendientes de especificación de anticipos, abonos, liquidación, entrega, vencimientos y comisiones. La tabla actual de pagos solo corresponde a ventas de mostrador.
7. **Migración histórica:** los registros sin hora real no deben insertarse como si tuvieran precisión horaria. Se definirá un archivo histórico o modelo con precisión explícita antes de importarlos. No se ha trasladado ninguna contraseña antigua.
8. **Catálogo:** faltan reglas de generación de códigos, cotizaciones de metales, proveedores, jerarquías completas y cambios autorizados. La categoría evita autorreferencia directa, pero aún no un ciclo de varios niveles; el catálogo no tiene API de escritura en esta fase.

## Archivos

- `database/migrations/001_core.sql`: estructura y recepción inicial.
- `database/migrations/002_locations.sql`: locales, almacenes y ubicaciones acordados.
- `database/migrations/003_validation.sql`: validación de cierre y secuencia local.
- `database/tests/`: pruebas reales en PostgreSQL, incluida concurrencia y restauración.
- `docs/modelo.md`: mapa y ejemplo del contrato de recepción.
- `docs/validacion.txt`: resultados de las pruebas realizadas.

Base de las decisiones: `../PV-laboratorio/analisis/Analisis_PV.md`.

Documentación técnica consultada: https://www.postgresql.org/docs/18/datatype-datetime.html, https://www.postgresql.org/docs/18/ddl-constraints.html y https://hub.docker.com/_/postgres.
