# Cambios comerciales de mercancía · ampliación E1

## Uso

En POS → Correcciones de operaciones → Cambio de mercancía, buscar el folio, fecha o vendedor de una venta confirmada. La búsqueda incluye ambas sucursales y folios de cambios anteriores. Seleccionar las unidades recibidas, confirmar origen y buen estado, buscar las piezas nuevas, indicar descuento autorizado y cobrar solo la diferencia. Comparar y confirmar. El comprobante se abre en vista previa con impresión y se conserva para reimpresión.

El rol requiere el derecho **Realizar cambios comerciales de mercancía**, inicialmente exclusivo del administrador. La operación exige conexión, caja abierta y permiso de venta; los descuentos respetan los límites del rol. La vista/impresión del comprobante conserva sus derechos independientes. El dashboard consulta los movimientos y avisos; la entrega física se confirma únicamente desde POS.

## Reglas y persistencia

- Plazo hasta el final del día natural 15 en America/Mexico_City. Cada mercancía nueva toma la fecha del cambio; las piezas originales restantes conservan su fecha de compra.
- Valor reconocido: neto pagado por las unidades recibidas, con descuento original. Las devoluciones parciales distribuyen los centavos usando el avance acumulado de unidades, conservando el total.
- Total nuevo después de descuentos igual o mayor al valor reconocido. No hay devolución de dinero ni creación automática de saldo a favor. Diferencia pagable en efectivo, tarjeta y transferencia; se conserva el cambio de efectivo recibido en exceso.
- Se conserva la venta y el cierre originales. La diferencia se asigna a la caja actual; los movimientos de existencias llevan fecha actual. Todo el cambio se confirma en una transacción PostgreSQL con bloqueo, control de idempotencia y revalidación de unidades/existencias. La comparación lleva huella para detectar cambios antes de confirmar.
- Las piezas normales recibidas regresan a Coyoacán; las nuevas salen de ese almacén. Las partidas **99** recibidas nunca generan ingreso a existencias y dejan un aviso persistente en el resumen del dashboard, con folio, fecha, sucursal, origen y descripción. No se crean productos para ellas.
- El valor original conserva vendedores y la diferencia se atribuye a quienes atienden. Las nuevas partidas guardan la atribución para cambios parciales posteriores. Se bloquean anulación/reemplazo por error y corrección de vendedores de la venta que ya tiene cambios vinculados.
- Dos movimientos de reporte, recepción negativa y entrega positiva, se registran en la fecha del cambio. Los cobros contienen solo la diferencia; se identifican los cambios en el listado. Las gráficas con valores negativos usan ejes con signo; el pastel de categorías se sustituye por barras cuando no puede representar esos valores.

## Archivos

`lab/e1/exchanges.py` mantiene el dominio, la tabla inmutable `merchandise_exchanges`, avisos y comprobantes. `static/exchanges.js` implementa las pantallas y reutiliza el buscador de productos y selector de vendedores. El servicio local sincroniza importes de cambios para caja, incluso después de reconectar; realizar un cambio sigue requiriendo conexión.

## Verificación

Pruebas de cambio con venta original cerrada, sucursal distinta, dos días de diferencia, pago mixto, cierre de caja actual, devolución parcial 99, aviso administrativo, plazo vencido, permiso, estado de piezas, sesión incorrecta, importe menor, cambios encadenados, reintentos, competencia por las mismas unidades y comparación obsoleta. Reportes verifican conservación de centavos, atribución y compensación de importes negativos.

Revisión en navegador con base desechable: compra 99 por $500 en sucursal 1 ya cerrada; cambio en sucursal 2 por artículo de $1,000; diferencia $500, comprobante, alerta 99 y caja con fondo $500/teórico $1,000. No se utilizaron ventas de la base de uso habitual para confirmar cambios.

Alcance: ventas ordinarias confirmadas y sus reemplazos/cambios; no aplica al historial SIM ni a la operación de órdenes de apartados/reparaciones, que conserva sus módulos. La aplicación de saldo a favor en ventas generales sigue pendiente en su módulo. Los avisos 99 son informativos y permanecen consultables; no alteran el inventario al revisarlos.

## Códigos visibles de comprobantes

Las ventas ordinarias usan `V1-000123` / `V2-000123`, calculados con la sucursal y la secuencia durable de operaciones del POS. Se conservan sin conexión, al sincronizar y al reimprimir, incluso para ventas anteriores. La secuencia incluye otras operaciones: puede haber saltos entre ventas. No se trunca un UUID para generar este código.

La restricción existente `UNIQUE(branch,seq)` y una sola cola SQLite por sucursal garantizan la unicidad en esta arquitectura. No se debe clonar/reiniciar la cola como si fuera otra terminal: antes de habilitar varias terminales por sucursal se requiere una asignación de rangos o identidad de terminal.

Los reemplazos por corrección usan `R1-000123`; los cambios comerciales, `C1-000123`. Su asignación central se guarda en `receipt_codes`, con identificador único, secuencia PostgreSQL única e inmutabilidad. La migración asigna códigos a los documentos anteriores sin alterar hechos económicos, UUID, firmas ni hashes.

Comprobantes, detalle, ticket y búsqueda de cambios muestran el mismo código; buscarlo completo prioriza la coincidencia exacta. Se mantiene la búsqueda por UUID antiguo, fecha o persona que registró la venta. Los códigos SIM/SV corresponden al historial ficticio; en el laboratorio también admiten cambios comerciales. No se generan códigos de barras.

Los datos ficticios tienen alias persistentes independientes: `SV1-000001` (venta), `SC1-000002` (caja), `SA1-000003` (apartado) y `SR1-000004` (reparación). La S evita colisiones con los códigos operativos. Se guardan en `simulated_receipt_codes` sin cambiar claves ni importes; cada comprobante de una orden agrega `-01`, `-02`, etc. Se conserva la marca de procedencia. Por decisión del usuario, las ventas del historial ficticio admiten cambios comerciales con el mismo flujo operativo. Cada cambio modifica inventario y cobra únicamente la diferencia en la caja actual; el lote original no se vuelve a cobrar ni se reconstruyen sus cajas. Las correcciones por errores de captura siguen separadas de este flujo.
