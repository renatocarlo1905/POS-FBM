# POS FBM · Frida Blancas México

Sistema de punto de venta para dos sucursales y un almacén compartido. **Laboratorio local en desarrollo; no aprobado todavía para sustituir el sistema del negocio.**

## Última actualización · 5 de noviembre de 2026

Esta actualización amplía inventario, usuarios y gestión de apartados y reparaciones, y mejora los cobros y comprobantes del laboratorio.

### Inventario y usuarios

- Importación de **productos nuevos** mediante plantilla de Google Sheets descargada como Excel; también se admiten CSV y TSV. Incluye vista previa, validaciones de catálogo y detección de duplicados.
- **Mercancía recurrente**: búsqueda de artículos existentes por descripción corta, larga o código; lista de cantidades y borrador persistente en el navegador. Disponible en administración y sucursales con permisos; confirmar requiere conexión.
- Descripciones corta y larga, precios fijos o por fórmula de costo/peso con terminación elegida por producto, y opción de imprimir el precio en etiqueta. El detalle del cálculo se consulta desde administración.
- Catálogo de proveedores habilitados, fecha de carga y última actividad de los artículos.
- Creación de usuarios desde administración, con rol y acceso a sucursales.

Consulta los campos, límites y procedimientos en [Importación de productos y mercancía recurrente](docs/e1/importacion-productos.md).

### Apartados, reparaciones y cobros

- Datos del cliente identificados claramente, incluido el teléfono.
- Acciones administrativas desde el dashboard: editar, registrar pagos, entregar, cancelar por mercancía, liberar apartados vencidos y cambiar estados de reparación, según las reglas de cada orden.
- Pagos, cancelaciones y entregas desde el dashboard requieren elegir una sucursal autorizada. Los cobros se asignan a su caja abierta; la sucursal debe estar conectada y sincronizada.
- Se exige importe exacto en ventas, abonos, liquidaciones y diferencias de cambios. Los pagos incompletos o excedidos se rechazan; los tickets no muestran devolución de cambio.
- Los cambios de mercancía aparecen en Comprobantes de la sucursal y permiten reimpresión. La búsqueda de piezas muestra su precio junto con ambas descripciones.
- Mejoras de búsqueda de tickets, indicadores de carga y alineación de controles de categorías.

### Validación y datos locales

Se añadieron pruebas de importación, metadatos, ingresos recurrentes, creación de usuarios y escenarios de órdenes. Las verificaciones recientes incluyen 10 pruebas de órdenes, 2 de cambios de mercancía y una de pago exacto en ventas; también se comprobaron controles del dashboard en el navegador.

El laboratorio local se preparó, con respaldo previo, con 12 apartados adicionales, ventas y cajas hasta el **4 de noviembre de 2026** y ninguna caja abierta. Esta preparación de PostgreSQL/SQLite y sus respaldos **no se distribuye con el repositorio**: clonar GitHub no restaura ese estado local. El módulo `lab/e1/order_training.py` conserva los escenarios iniciales de órdenes, no una copia de la base local completa.

## Aplicación vigente

El código activo está en `lab/e1/`. Las carpetas `prototype/` y `database/` conservan prototipos anteriores; no deben confundirse con el servicio vigente ni aplicarse sus migraciones a E1.

| Capa | Tecnología actual |
| --- | --- |
| Interfaz | HTML, CSS y JavaScript sin framework; tres páginas |
| Servicios | Python 3.12 y servidor HTTP de la biblioteca estándar |
| Datos centrales | PostgreSQL 18 mediante Psycopg |
| Persistencia de cada POS | SQLite |
| Comprobantes | ReportLab, Pillow y Poppler para vista previa e impresión |
| Entorno local | Linux, Docker para PostgreSQL |
| Pruebas | unittest, pypdf y pruebas JavaScript con Node.js |

## Inicio en un Linux nuevo

Requiere Python 3.12 con venv, Docker operativo, Poppler (`poppler-utils`) y Node.js para las pruebas JavaScript.

```bash
python3 -m venv lab/e1/.venv
lab/e1/.venv/bin/python -m pip install -r lab/e1/requirements-dev.txt
python3 lab/e1/setup_postgres.py
lab/e1/run.sh
```

El instalador genera credenciales locales en `lab/e1/data/`, excluidas de Git. No copies credenciales de otra computadora. Solo expone los servicios en la interfaz local.

- Dashboard: http://127.0.0.1:8870/dashboard.html
- POS 1: http://127.0.0.1:8871/sucursal-1.html
- POS 2: http://127.0.0.1:8872/sucursal-2.html

No abrir los HTML con doble clic: necesitan los servicios. Las cuentas iniciales y contraseñas de demostración se describen en [la guía del laboratorio](docs/e1/README.md); deben cambiarse antes de cualquier despliegue operativo.

## Abrirlo en la computadora de Renato

Busca **POS FBM** en el menú de aplicaciones o abre el acceso **POS-FBM** del escritorio. El lanzador inicia PostgreSQL, espera que esté disponible, inicia el servicio local y abre el dashboard. Puede aparecer una terminal durante unos segundos.

Alternativa desde la terminal:

```bash
/home/renatocarlo19/Documentos/POS-nuevo/scripts/local/open-pos.sh
```

El servicio persistente está instalado en `~/.config/systemd/user/frida-pos-e1.service`. Se inicia al usar el acceso, no automáticamente al encender la computadora. Para consultar su estado: `systemctl --user status frida-pos-e1`. Para detener la aplicación: `systemctl --user stop frida-pos-e1` (no elimina datos).

Abrir únicamente el enlace del navegador no enciende el servidor. Si aparece `ERR_CONNECTION_REFUSED`, utiliza el lanzador. Si Linux lo pide la primera vez, haz clic derecho sobre el acceso del escritorio y elige **Permitir lanzar**. Esta instalación local utiliza rutas de esta computadora; para otra computadora sigue el procedimiento de instalación anterior.

## Organización y desarrollo

- [Metodología, arquitectura y decisiones de framework](docs/desarrollo.md).
- [Cómo contribuir y entregar cambios](CONTRIBUTING.md).
- [Plan de etapas y alcance completo](docs/Plan_desarrollo_POS_Frida_Blancas_v1.md).
- [Requisitos y aceptación](docs/e0/README.md).
- [Apartados y reparaciones operativos](docs/e1/apartados-reparaciones-operacion.md).
- [Vista previa e impresión](docs/e1/comprobantes-vista-previa.md).
- [Prototipo histórico v0.1](docs/archive/prototipo-base-v01.md).

## Verificación

Con PostgreSQL de laboratorio iniciado, ejecutar:

```bash
lab/e1/.venv/bin/python -m unittest discover -s lab/e1/tests -p 'test_*.py'
node lab/e1/tests/test_sales_reports.cjs
node lab/e1/tests/test_orders.cjs
```

Las pruebas de integración crean bases desechables. No ejecutarlas contra producción. La aprobación de una suite no equivale a aprobación de salida a operación: faltan validaciones de equipos físicos, recuperación y despliegue en sucursales independientes.

## Qué se versiona

Código, documentación, esquemas SQL, pruebas, datos ficticios definidos en código y recursos gráficos necesarios. Se excluyen contraseñas, bases locales, respaldos, entornos virtuales y salidas generadas. GitHub conserva el historial del código; no sustituye los respaldos de PostgreSQL y SQLite.

La marca y los recursos de Frida Blancas México no se conceden bajo una licencia abierta. Las fuentes Montserrat conservan su licencia OFL incluida.
