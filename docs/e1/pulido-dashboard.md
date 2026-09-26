# Pulido visual del dashboard · 25/09/2026

Referencia: las dos grabaciones de Loyverse entregadas por el usuario (11:57:50 y 12:00:08). Se adaptan las interacciones a la identidad Frida; esta entrega permanece en E1 y no modifica datos, esquema o reglas de operaciones.

## Interacciones disponibles

- Barra lateral de símbolos con nombres accesibles y ayudas al pasar el cursor. Cada símbolo abre sus opciones; se cierra al seleccionar una opción, pulsar fuera o presionar Escape. Se mantienen todos los accesos existentes del dashboard.
- Tarjetas seleccionables de ventas brutas, descuentos, ventas netas y cobros registrados. La selección controla gráfica y tabla; comparación contra un periodo anterior de igual duración. Si la base anterior es cero se indica que no hay base para un porcentaje.
- Fechas inclusivas, accesos rápidos Hoy/Ayer/7 días/30 días/mes actual/mes anterior, calendario nativo del navegador, navegación entre periodos y validación de orden y duración (hasta 366 días).
- Filtros de sucursal y vendedor. El vendedor filtra ventas en las que participó y muestra su importe completo; no representa el reparto de comisiones.
- Gráfica de área o barras; agrupación por día, mes u hora (esta última para periodos de hasta siete días). Fechas y horas del reporte en America/Mexico_City.
- Detalle flotante con importe y número de ventas mediante puntero, clic o foco de teclado. Tabla alternativa de valores exactos y listado de las últimas doce ventas del periodo.
- Estados sin ventas, transiciones de gráfica y menú, reglas de diseño para pantallas estrechas y respeto a la preferencia de reducir movimiento.

Solo se representan operaciones confirmadas, aplicando las correcciones vigentes y excluyendo anuladas. No se agregan cifras ilustrativas ni métricas aún no implementadas, como reembolsos o beneficio bruto. La vista se actualiza con el mecanismo existente y conserva filtros durante sus actualizaciones; al recargar se abre el periodo de los últimos siete días.

## Verificación de esta entrega

- JavaScript validado con `node --check`.
- Recorrido en navegador: icono Empleados → Derechos de acceso → Reportes → Resumen de ventas; menú desplegable y selección verificados.
- Filtro Sucursal 2: tarjetas, gráfica de barras y tabla coinciden en $1,300.00 y una venta con los datos existentes del laboratorio.
- Periodo Ayer: mensaje sin ventas. Periodo siguiente: cuatro ventas por $4,950.00. Agrupación por hora: a las 09:00 aparecen tres ventas por $3,950.00, con detalle flotante visible.
- Inspección visual de interfaz y detalle de gráfica; consola sin errores en el recorrido. No se crearon ventas ni se modificaron empleados durante estas comprobaciones.

La suite de 21 pruebas de E1 corresponde a la entrega anterior; no se presenta como una nueva ejecución para este cambio visual. No se ejecutó una auditoría integral de accesibilidad ni una prueba en dispositivos físicos pequeños.
