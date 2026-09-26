# Apartados y reparaciones · Consulta previa a E2

> Registro histórico. El alcance fue ampliado por el usuario el 26/09/2026. Ver [operación local adelantada](apartados-reparaciones-operacion.md).

Implementado el 26 de septiembre de 2026. El usuario eligió preparar pantallas de consulta; la operación completa permanece en E5.

## Alcance entregado

Módulo lateral «Apartados y reparaciones»: resumen con alertas, consulta de apartados, consulta de reparaciones y reglas del negocio. Filtros de sucursal de registro, estado, fechas y búsqueda de folio/cliente/teléfono. Cada folio abre un detalle con piezas, pagos, saldo, plazos, historial, presupuesto y comprobantes.

14 ejemplos aislados, con fecha de corte fija 26/09/2026: siete apartados y siete reparaciones. Contemplan próximos a vencer, vencidos, liquidados sin entregar, entregados, cancelados, liberados, reparación en proceso y una corrección a recibida que conserva el antecedente de trabajo iniciado. No se escriben órdenes, reservas, pagos ni movimientos en PostgreSQL.

Los comprobantes se previsualizan y descargan como PDF con logo, marca SIMULADO, folio, cliente ficticio, piezas, importes históricos y sucursal del movimiento. Un PDF reúne sus copias en páginas separadas: dos en apartados; tres en recepción de reparación; dos en liquidación y entrega de reparación; una interna para cancelación de reparación. La copia de negocio en entrega incluye espacio para firma manuscrita. El endpoint exige sesión administrativa y no genera operaciones.

## Trazabilidad del documento de requerimientos

Fuente: `output/pdf/Requerimientos_POS_Frida_Blancas_Mexico_v2.pdf`, páginas 11–14 y 24.

- APA-01–09: conexión, anticipo 40 %, piezas y precio/costo conservados, abonos, liquidación y entrega separadas, vendedores originales, comprobantes.
- APA-10–16: plazo 45 días, aviso previo, revisión y liberación manual, excepciones y cancelación hasta día 7 con mercancía equivalente, sin devolución de efectivo.
- REP-01–07: piezas del cliente, anticipo 50 %, presupuesto, cobro final, sin abonos intermedios ni comisión comercial y comprobantes.
- REP-08–15: estados, correcciones, recogida 45 días desde lista, vencimiento solo alerta y restricción de cancelación si alguna vez comenzó el trabajo.
- DAS-34–45: consultas, filtros, alertas y detalle; COR-17: bloqueo económico después de liquidar.

## Pendiente para E5

Persistencia de órdenes, reservas, cobros y sus efectos contables; permisos operativos, transiciones, entrega desde POS, correcciones, conversión a mercancía/saldo y resolución de alertas. Precisar D02 (sucursal de atribución), D05 (efectos de correcciones de anticipo/presupuesto), D03/D06 (beneficios y conversiones), D22 (validación final de formatos). Mantener íntegro el alcance de primera puesta en operación.

## Validación

`tests/test_orders.cjs`: 14 casos coherentes, límites inclusivos, apartado liquidado fuera de vencimiento, entregas pagadas y ausencia de abonos intermedios en reparaciones.

`tests/test_orders_pdf.py`: todas las copias PDF, identidad de fixtures de UI/servidor y rechazo de folios/índices inválidos. Revisión visual de PDFs de liquidación de apartado y entrega de reparación. Descarga real probada en navegador y filtro de reparaciones vencidas verificado sin errores de consola.
