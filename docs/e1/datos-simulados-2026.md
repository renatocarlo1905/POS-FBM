# Historial ficticio de 2026

Generado el 25/09/2026 a las 12:20, hora de Ciudad de México. Periodo: 01/01/2026 a 25/09/2026, sin registros posteriores al momento de generación.

- 2,991 ventas simuladas: 1,646 de Sucursal 1 y 1,345 de Sucursal 2.
- Siete empleados, con rotación de operador y algunas ventas compartidas por dos vendedores.
- 24 productos ficticios adicionales (anillos, aretes, dijes, pulseras y collares); 80 unidades actuales de cada producto en Coyoacán, compartidas entre ambas sucursales.
- Variación por día/mes, fines de semana y campañas ficticias de febrero y mayo. Días sin operaciones, descuentos de 0–20%, efectivo con cambio, tarjeta, transferencia y pagos mixtos.
- Importe bruto $5,883,140.00, descuentos $198,511.00, neto $5,684,629.00 MXN. Son cifras sintéticas para explorar el software, no estimaciones del negocio.

## Cómo probar

En Resumen de ventas selecciona **Datos → Solo historial simulado**, abre fechas y elige **Este año → Aplicar periodo**. Usa **Meses** para ver el año completo o **Días** para explorar un mes. Cambia sucursal/vendedor, selecciona las tarjetas y abre la tabla de valores. **Solo ventas manuales** conserva la vista de las operaciones anteriores y las que registres después.

Los productos llevan «Ficticio» en el nombre y están disponibles en Inventario y en ambos POS al sincronizar/iniciar sesión. Sus existencias actuales sirven para nuevas pruebas de venta.

## Separación de operaciones

El histórico se almacena en la tabla PostgreSQL `simulated_sales`. No entra en la secuencia de eventos de los POS, no abre/cierra cajas ni descuenta existencias actuales. Sirve para reportes, atribución a vendedores, consulta y descarga de comprobantes explícitamente simulados. No se ofrece para correcciones operativas; para probarlas registra una venta manual con los productos ficticios.

Las operaciones anteriores permanecen intactas. Las autorizaciones, contraseñas y límites actuales no se cambiaron. Los descuentos del histórico describen un escenario sintético y no alteran la autorización actual de cada empleado. Los PDF del lote conservan una plantilla propia con leyenda de simulación.

## Reproducibilidad y comprobación

Generador: `lab/e1/seed_simulation.py`. Semilla aleatoria fija; identificadores deterministas por lote. Reejecutarlo detecta el lote y no duplica ventas ni productos. El manifiesto completo está en `datos-simulados-2026.json`.

Se guardaron respaldos PostgreSQL antes y después en `lab/e1/data/backups/pre-simulation-2026.dump` y `post-simulation-2026.dump`.

Validaciones: fechas/UUID únicos, suma de partidas, descuentos y pagos de todas las ventas; huellas de los eventos anteriores sin cambios; segunda ejecución sin duplicados; 21 pruebas de regresión aprobadas (40.172 s). Navegador: 2,991 ventas y neto anual coincidente, cuatro ventas manuales originales conservadas en su filtro, filtro Ximena con ventas propias/compartidas, descarga de PDF simulado correcta y consola sin errores. Se reutilizó el formato de producto del alta manual.
