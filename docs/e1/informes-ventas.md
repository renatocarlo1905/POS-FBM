# Informes de ventas — 26/09/2026

Acceso: icono Reportes → Ventas por artículo, categoría, empleado o tipo de pago. Se mantienen Recibos y Resumen de ventas.

Filtros compartidos entre los cuatro informes: fechas (Ciudad de México), sucursal, origen manual/simulado y empleado participante. Búsqueda, paginación de 20 filas, totales del filtro completo y descarga CSV. El botón Este año selecciona enero hasta la fecha actual. Artículos incluye los cinco mayores importes netos, gráfica de líneas/barras y agrupación diaria/mensual.

Las ventas confirmadas incorporan correcciones vigentes; se excluyen anuladas. Categoría corresponde al tipo de pieza actual. Costos y beneficios son estimados con el catálogo actual, sin costo histórico congelado. No se presentan cifras inventadas de reembolsos, propinas o altas de clientes.

En ventas compartidas, los importes y descuentos se reparten por igual entre vendedores; el residuo en centavos se asigna por identificador ordenado. Los recibos cuentan participaciones. El filtro de empleado selecciona operaciones donde participó, incluyendo los otros participantes de esas operaciones. En pagos mixtos cada medio cuenta una transacción; el efectivo corresponde al aplicado, sin cambio.

## Descuentos

El rol Personal de venta tenía límite de 40 % pero permiso discount desactivado. Se activó manteniendo el límite existente y registrando el cambio mediante el servicio de roles. Respaldo previo: lab/e1/data/backups/pre-report-discount-fix.dump. El formulario explica que permiso y límite deben configurarse juntos. El POS valida permiso, número finito y rango antes de continuar; el servicio mantiene su validación independiente. Es necesario iniciar sesión en línea de nuevo para descargar los permisos. Sin conexión se conserva la última autorización descargada.

## Verificación

- 21 pruebas de integración y 3 de cajas aprobadas.
- test_sales_reports.cjs verifica pagos mixtos, reparto exacto de centavos, anulaciones y correcciones.
- Los cuatro informes concilian 2,991 ventas simuladas: $5,684,629.00 netos. Verificado en modelo y totales visibles del navegador.
- Exportación CSV descargada desde el navegador.
- POS Melissa: $1,000 con 10 % muestra $900 en pago; 41 % bloqueado. Venta cancelada antes de registro, carrito limpiado.
- Cajas sin filtro ni etiquetas de turno; solo apertura y cierre. No se modifica la distribución histórica de las cajas simuladas.
- Presentación de artículos revisada en navegador; sin errores de consola observados.
