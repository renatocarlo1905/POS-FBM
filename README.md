# POS FBM · Frida Blancas México

Sistema de punto de venta para dos sucursales y un almacén compartido. **Laboratorio local en desarrollo; no aprobado todavía para sustituir el sistema del negocio.**

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
