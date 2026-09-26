# Apartados y reparaciones: operación local adelantada

26/09/2026. Sustituye la limitación de consulta acordada inicialmente: el usuario pidió operación completa desde POS, vinculada al dashboard, y edición exclusiva del administrador.

## Uso

En el dashboard, el módulo lateral conserva «Apartados y reparaciones» y su primera opción ahora se llama «Resumen». Cada orden abre su detalle y el botón Editar orden para administradores. Se pueden corregir cliente, teléfono, notas y, en reparaciones no liquidadas, trabajo, entrega prevista y presupuesto. Se exige motivo y se conserva el historial. Las piezas/precios del apartado se conservan desde el registro. No se pueden alterar importes después de liquidar.

En ambas sucursales aparecen Apartados de mercancía y Reparaciones. Nuevas órdenes se crean desde el POS con caja abierta y conexión. Las tablas consultan el mismo PostgreSQL y se actualizan al guardar, al pulsar Actualizar órdenes y periódicamente mientras el listado esté abierto. El detalle abierto conserva su revisión; un cambio desde otra sesión obliga a actualizar antes de guardar.

El permiso Gestionar apartados y reparaciones habilita consulta, registro, cobros y entrega. Se inicializa para los roles que ya podían vender y queda editable desde Derechos de acceso. Editar, cambiar estados, autorizar cobros vencidos, liberar o cancelar requiere rol administrador, comprobado también en servidor. Los permisos de comprobantes/reimpresión se conservan para descargar PDFs.

## Flujos

- Apartado: elegir artículos/cantidades y vendedores, cliente/teléfono, anticipo mínimo 40 %, sin descuentos. Reserva existencias centrales una sola vez. Abonos positivos hasta el saldo desde cualquiera de las sucursales. Liquidación registra venta una sola vez, conserva vendedores originales y atribuye la venta a la sucursal que liquida. Entrega completa es otro acto, exclusivamente POS.
- Reparación: piezas del cliente fuera de inventario, trabajo, presupuesto, fecha prevista y acuerdo; anticipo mínimo 50 %. No admite abonos intermedios. Administrador actualiza estados; liquidación final al estar lista y entrega completa desde POS. No genera comisión comercial (Matanga - sin asignación).
- Presupuesto: reducción por debajo de lo pagado genera saldo a favor por la diferencia y liquida; aumento mantiene lo pagado y deja diferencia pendiente. Se conserva acuerdo/motivo y presupuesto histórico. El saldo se identifica por teléfono y puede aplicarse a pagos de órdenes; su integración con el módulo general de clientes/ventas sigue siendo parte del trabajo pendiente de ese módulo.
- Plazos: valores iniciales 45 días naturales, configurables para nuevas órdenes desde Reglas y alcance. Cada orden conserva su plazo. Avisos no liberan ni entregan automáticamente. Reparación que vuelve a proceso suspende recogida, y volver a lista reinicia su plazo conservado. El antecedente de haber iniciado trabajo bloquea cancelar aun después de corregir a recibida.
- Liberación: administrador, apartado vencido sin liquidar; devuelve reserva al disponible, conserva pagos e historial, sin reembolso.
- Cancelación por mercancía: administrador desde POS con caja abierta. Apartado hasta fin del día 7, reparación recibida/nunca iniciada/no liquidada. Mercancía igual o superior a lo pagado; cobra solo diferencia, libera originales cuando corresponda, no entrega efectivo. Atribución anterior y de diferencia separadas. Conserva comprobante interno de reparación y copias de apartado.

## Persistencia y conciliación

Tablas PostgreSQL service_orders, order_requests y order_credit. Transacción única para documento, reserva/liberación, pagos, crédito, reconocimiento de venta, auditoría y deduplicación. Petición UUID se conserva ante una respuesta incierta; repetir no vuelve a cobrar ni reservar. Revisión optimista impide sobrescribir cambios de otra sesión.

Cobros se asignan a la caja receptora y participan en su esperado/cierre, con medios separados. Los anticipos no son ventas: informes reconocen ingreso comercial al liquidar; informe por medios y indicador de cobros incluyen los movimientos cuando ocurren. Costos/categorías de las partidas se conservan. Cancelación atribuye el importe previo a vendedores originales (o Matanga) y la diferencia a vendedores actuales.

Los 14 folios SIM- siguen aislados, permiten correcciones administrativas de consulta pero no operación de caja, cobro ni reservas. Para probar el flujo, usar Nuevo apartado o Recibir reparación. No se convirtieron retroactivamente los ejemplos en transacciones.

## PDFs

Descarga desde cada movimiento, con logo, folio, importes y copias correspondientes. Dos copias en apartados; tres al recibir reparación; dos en liquidación/entrega; interna firmada para cancelación de reparación. La copia de negocio en entrega incluye firma manuscrita. Los documentos de nuevas órdenes conservan instantánea al emitirse: editar posteriormente no cambia el PDF original.

## Validación

Pruebas PostgreSQL y HTTP en bases aisladas: reservas y rollback, mínimo de anticipo, abonos y liquidación entre sucursales, cierre con anticipos, edición administrativa, revisión concurrente, idempotencia, corrección de presupuesto y saldo, estados/cancelación y bloqueo sin conexión, PDF con sus tres copias. Suite de regresión del laboratorio aprobada. Prueba de interfaz aislada: recibir reparación, anticipo, lista, liquidación, entrega y descarga PDF; revisión visual del PDF de entrega.

Los cobros de verificación no se insertaron en las dos cajas del usuario. Permanecen abiertas una caja por sucursal. La puesta en producción y las dependencias completas de E2/E3/E4 siguen requiriendo la validación prevista en el plan general; este adelanto es para operación local de pruebas.
