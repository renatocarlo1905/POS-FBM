# Verificación del laboratorio E1

25/09/2026. Datos ficticios; PostgreSQL real en Docker/Linux. Ver salida completa en [resultado-pruebas.txt](resultado-pruebas.txt).

Resultado final: **21 pruebas aprobadas**, ejecutadas en 39.011 segundos. Para instalar las dependencias de verificación se incluye `lab/e1/requirements-dev.txt`.

La suite verifica dinero/pagos, inventario compartido, dos ventas offline de última unidad, reintento tras acuse perdido, reinicio de cola, atomicidad acuse/snapshot, permisos y porcentaje, cambio de contraseña/rol, protección del administrador, cierre ciego, fallo de segunda copia sin bloqueo, restauración de cola y PostgreSQL, plantilla histórica/PDF, concurrencia online, límites HTTP, descargas temporales de un uso, redondeo, firma/contenido alterados, secuencia, alta manual, ingreso por almacén, corrección de pagos y cierres, cancelación única/cambio vinculado, vendedor/autorizador, reemplazos encadenados, hechos inmutables y correcciones de varias ventas de una sesión.

Las pruebas se ejecutan en bases `e1_test_*` y `e1_restore_*` y directorios temporales. No representan aprobación del conjunto A01-A30 de salida ni carga de producción.

## Recorridos en navegador

- Inicio de sesión de Carlo, Melissa y Ximena en las páginas correspondientes; formularios de empleados y roles revisados.
- Apertura S1 por $500; venta de $1,000 con $500 recibidos en efectivo y $600 tarjeta: efectivo aplicado $400, cambio $100; existencia de anillo pasa de 8 a 7.
- Recarga/reinicio del servicio conserva la operación; S2 recibe la existencia compartida.
- Alta manual de «Dije espiral · prueba» con costo $450, precio $1,200, peso 2.400 g y dos unidades en Coyoacán, previa comparación. Producto visible en S2 después de autenticar/sincronizar.
- Corrección de pago desde dashboard: efectivo $400/tarjeta $600 a efectivo $0/tarjeta $1,000, mismo total. Comparación y confirmación realizadas; historial conserva operador, autorizador y motivo; no se envió impresión pendiente al POS.
- Descarga de vista previa PDF confirmada mediante evento de descarga del navegador. La descarga inicial mediante URL blob no produjo evento fiable en el navegador integrado; se sustituyó por entrega HTTP de un archivo con URL temporal de un uso y se verificó.
- Inspección visual de dashboard con logo/paleta/Montserrat. PDFs de ticket y corrección renderizados con Poppler y revisados: acentos legibles, logo proporcionado, sin texto cortado.

## Pendientes de validación integral

Equipos físicos, impresoras, lectores, dos computadoras con fallas independientes, pérdida de disco, reinstalación con cola antigua, endurecimiento de despliegue, carga y duración offline. No se ejecutó una auditoría externa de seguridad ni accesibilidad completa. Los módulos de órdenes y saldo aún no existen en este backend; por tanto sus correcciones económicas no están certificadas. El estado final y el alcance pendiente están descritos sin reducir la primera puesta en operación en [README](README.md).
