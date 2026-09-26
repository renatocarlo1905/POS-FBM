# Reportes → Cajas

Implementado el 25/09/2026 siguiendo las capturas de Loyverse: listado paginado de sesiones de caja y panel lateral de cuadre de efectivo, con identidad gráfica Frida.

## Uso

Recarga el dashboard, abre el icono Reportes y selecciona Cajas. Filtra por fechas de apertura, origen (manual/simulado), sucursal y estado (abierta/cerrada/con descuadre). El listado muestra 20 registros por página. Pulsa el nombre de la caja para abrir el detalle. Exportar CSV descarga todos los registros del filtro, no solo la página visible.

El panel incluye responsables y horarios de apertura/cierre, fondo inicial, cobros en efectivo, entradas, gastos/retiros, esperado, contado, diferencia, fondo siguiente, sobre, ventas brutas, descuentos, ventas netas y medios de pago. Los reembolsos comerciales no se inventan: su módulo está pendiente.

## Datos ficticios

Se generaron 1,070 turnos entre 01/01/2026 y 25/09/2026 a las 14:20 de Ciudad de México: 1,068 cerrados y dos abiertos. Horario de simulación asumido: mañana 10:00–15:00, tarde 15:00–20:00, dos turnos por día y sucursal; no se generan aperturas/cierres futuros. La tarde del 25 aún no había comenzado.

Cada turno agrega las ventas del lote simulado por sucursal, día y horario, sin modificar esas ventas. En conjunto: 2,991 ventas y $5,684,629.00 netos. El lote de ventas llega al 25/09 a las 12:20; los turnos son una fotografía de esos datos, no se cierran solos al avanzar el reloj.

Fondo de ejemplo: $500. Entradas/salidas ficticias y diferencias reproducibles para probar tanto cuadros exactos como faltantes y sobrantes. Los turnos se almacenan aparte en `simulated_shifts` y no afectan las cajas operativas. Repetir `cash_reports.seed(c)` no duplica el lote. La metadata queda en `simulated-shifts-v1` de la base local.

## Cajas manuales y correcciones

Se usan únicamente eventos aceptados. Las cajas abiertas no tienen contado ni diferencia y no participan en los totales de cierre. Desde el 26/09/2026 no se clasifican las cajas por mañana/tarde: cada sesión conserva sus fechas de apertura y cierre, con duración libre. Los cierres conservan esperado, conteo y diferencia declarados; los ajustes posteriores se muestran aparte. Los resúmenes de ventas reflejan las correcciones vigentes y los reemplazos, sin duplicar la venta anulada.

Los filtros usan America/Mexico_City. La consulta se actualiza con el refresco periódico del dashboard; también existe Actualizar cajas. El reporte es de consulta: no abre ni cierra cajas desde administración.

## Verificación

- Cuadres de los 1,070 turnos: esperado = fondo + efectivo + entradas − salidas; contado = esperado + diferencia = fondo siguiente + sobre.
- Conciliación exacta contra las 2,991 ventas sintéticas, y segunda carga sin duplicados.
- 21 pruebas previas aprobadas, y tres nuevas en `lab/e1/tests/test_cash_reports.py`: caja abierta sin conteo inventado, cierre con corrección posterior y anulación/reemplazo sin duplicación.
- Navegador: listado anual de 1,070 simuladas, filtros de sucursal/descuadre, detalle manual y simulado, descarga CSV por HTTP con URL temporal de un uso. Sin errores de consola.
- Respaldos PostgreSQL en `lab/e1/data/backups/pre-cash-reports.dump` y `post-cash-reports.dump`.
