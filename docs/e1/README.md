> Guía inicial de E1. Para el estado vigente consultar el README raíz y los documentos específicos de órdenes, categorías, informes y comprobantes. Algunas descripciones inferiores corresponden al primer corte del laboratorio.

# Laboratorio E1 · Frida Blancas México

25/09/2026. Laboratorio funcional local con **PostgreSQL central y SQLite por POS**, tres páginas independientes y datos ficticios persistentes. Incluye las ampliaciones solicitadas durante el desarrollo: identidad de marca, alta manual de productos y correcciones de ventas. No sustituye todavía al sistema del negocio.

## Abrir y entrar

- Dashboard: http://127.0.0.1:8870/dashboard.html
- Sucursal 1: http://127.0.0.1:8871/sucursal-1.html
- Sucursal 2: http://127.0.0.1:8872/sucursal-2.html

Los HTML están en `lab/e1/static`. Deben abrirse mediante esos servicios, no con doble clic: necesitan el backend para autenticación y persistencia.

Usuarios iniciales: `carlo`, `melissa`, `ximena`, `citlali`, `jessica`, `himelda`, `zicaru`. Contraseña inicial de laboratorio: nombre con mayúscula inicial seguido de `-E1-2026!`, por ejemplo `Carlo-E1-2026!`. Son exclusivamente credenciales ficticias locales, editables por Carlo. Los demás empiezan con el rol Personal de venta y descuento deshabilitado (0%); Carlo decide el porcentaje.

En Empleados se editan nombre, correo, teléfono, rol, sucursales, estado y nueva contraseña. El sistema guarda verificadores derivados, no contraseñas en texto. En Derechos de acceso se crean/editan roles; los permisos y su límite de descuento afectan a todos los integrantes. Para una excepción individual, crear otro rol y asignarlo. El rol administrador mantiene todos los derechos y Carlo no puede perderlo accidentalmente.

## Recorrido de prueba

1. Entrar como Carlo en dashboard; revisar Empleados, Derechos de acceso y Configuración de tickets.
2. En cada POS, entrar con un empleado y abrir su caja. El acceso inicial requiere central disponible para descargar autorización y catálogo.
3. Vender una pieza ficticia en S1; actualizar S2 y dashboard. Ambos POS utilizan Coyoacán sin cupos de dispositivo.
4. En Conexión y respaldos, desconectar S1. Registrar venta, recargar y comprobar que queda guardada. Reconectar: se confirma una sola vez.
5. Abrir la vista previa desde un comprobante y pulsar Imprimir. La primera generación en POS es original; siguientes generaciones son copias. Generar/imprimir no crea otro cobro. Una descarga tiene URL temporal de un solo uso.
6. En Inventario, crear proveedor si hace falta y Agregar producto. Revisar y confirmar; se genera código numérico de 15 dígitos y entrada al almacén elegido. Ingresar unidades reutiliza el código. No hay carga Excel todavía.
7. En Correcciones, buscar una venta confirmada; consultar original; escoger acción; escribir motivo; comparar y confirmar. Revisar después stock, acumulados, caja e historial. El administrador también puede hacerlo desde dashboard.

El laboratorio conserva una apertura y venta ficticias en S1, una corrección de pago desde dashboard y el producto «Dije espiral · prueba» creados durante la verificación visual. No son datos del negocio. No se borraron para disimular las pruebas.

## Qué está implementado

- Servicio central Python, PostgreSQL 18 aislado, dos servicios POS y dos archivos SQLite.
- Autenticación individual; roles y permisos verificados por servicios; límite de descuento porcentual.
- Última autorización descargada para trabajar offline; revocaciones se conocen al reconectar, sin caducidad automática impuesta en esta prueba. Los hechos offline previamente autorizados no se pierden al cambiar un rol.
- Ventas con pagos mixtos; centavos exactos; cambio separado; uno o varios vendedores; apertura, movimientos autorizados y cierre ciego por sucursal.
- Cola durable, UUID estable, secuencia, validación del contenido repetido, acuse y actualización del snapshot local en una transacción.
- Venta online con consumo central serializado. Si dos ventas ya cobradas offline revelan negativo, se conservan y se señala la incidencia.
- Segunda copia SQLite por POS independiente del otro POS, y respaldos PostgreSQL con pg_dump. Restauración probada en bases/archivos desechables.
- Tickets configurables por sucursal: logo, cabecera, pie y ancho 58/80 mm; plantilla histórica conservada; PDF con tipografía incrustada.
- Alta manual con descripción corta/larga, material, tipo, subcategorías de captura, proveedor registrado, precio/costo, peso opcional (máximo 999 g/tres decimales), PNG opcional, almacén/cantidad. Códigos generados, cantidades del mismo artículo comparten código. Ingreso recurrente sin alterar precio/costo histórico.
- Correcciones de ventas: reparto de pago manteniendo total; vendedores; anulación por error; anulación y nueva venta correcta vinculada, incluidos reemplazos encadenados. Comparación, motivo, operador/autorizador, autorización puntual desde POS, concurrencia controlada e idempotencia. Originales y movimientos de stock conservados; nuevas entradas/salidas fechadas. Cierres originales y vista ajustada separados. Dashboard no crea impresión pendiente en POS.

## Límites de esta entrega

**No declarar E1 integral ni salida operativa aprobadas solo por este laboratorio.** Las pruebas de equipos reales, dos computadoras independientes, pérdida total de disco, copias en soporte independiente, recuperación de identidad/contadores tras reinstalación y duración de cortes reales siguen pendientes. Las tres interfaces están aisladas por servicio/puerto, pero comparten el mismo proceso anfitrión y computadora en este ensayo.

Las correcciones implementadas abarcan ventas de mostrador existentes en el laboratorio. Los pagos de apartados/reparaciones, anulación de pagos pendientes, restitución de saldo, COR-17 ligado al estado real de órdenes y revisión de cálculos de comisión guardados requieren integrar E4/E5/E7. No se ofrece una falsa edición de esas entidades ausentes. El bloqueo de venta con cambio comercial relacionado se prueba mediante vínculo de ensayo; el flujo de cambio comercial aún pertenece a E6.

Inventario aún no incluye edición completa del catálogo/códigos históricos, administración jerárquica de catálogos, traspasos, reversión de ingreso, precios/costos variables, impresión de etiquetas ni importación Excel. Los nombres de subcategorías son captura inicial, no catálogo administrable definitivo. Los seis artículos iniciales son fixtures; el resto se guarda en PostgreSQL.

E0 queda conservada como maqueta histórica. Apartados, reparaciones, saldo, cambios, importación/migración y reportes completos mantienen su lugar obligatorio antes de la primera sustitución operativa. Su ausencia en E1 no reduce ese alcance.

## Arranque en este equipo Linux

Desde `/home/renatocarlo19/Documentos/POS-nuevo`:

```bash
python3 lab/e1/setup_postgres.py
lab/e1/run.sh
```

`setup_postgres.py` crea/reutiliza exclusivamente `pos-frida-e1-postgres`, volumen `pos-frida-e1-pgdata`, base `pos_e1` y rol no superusuario `pos_e1_app`. Publica PostgreSQL solo en `127.0.0.1:55432`. Las bases anteriores `pos_desarrollo` y SQL Server no se modifican. No mostrar ni versionar `lab/e1/data/postgres.json` o `postgres.env`.

Para instalar en otro Linux: Python 3.12, Docker, crear un entorno virtual `.venv`, instalar `lab/e1/requirements.txt` y ejecutar el mismo arranque. Las fuentes Montserrat se incluyen localmente con licencia OFL; no se consulta un CDN al utilizar el POS. `fonttools` solo se utilizó al preparar esas fuentes.

```bash
lab/e1/.venv/bin/python lab/e1/tests/test_e1.py
```

La suite crea y elimina bases PostgreSQL cuyo nombre empieza por `e1_test_`/`e1_restore_`; no reinicia la base de la demostración. Resultado y límites: [verificación](verificacion.md).

- [Arquitectura y decisiones](arquitectura.md)
- [Aplicación de identidad](identidad.md)
- [Pruebas ejecutadas](resultado-pruebas.txt)

## Reporte de cajas

Disponible en **Reportes → Cajas**. Consulta [la guía del reporte y sus datos ficticios](reporte-cajas.md): filtros, panel lateral, CSV y 1,070 turnos simulados de mañana/tarde conciliados con el historial de ventas.
