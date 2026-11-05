# Ajustes de POS — 26/09/2026

- Comprobantes desaparece de la navegación sin permiso receipts; una vista seleccionada previamente vuelve a venta. El servicio omite operaciones y correcciones del estado y requiere receipts + reprint para descargar PDF. Se conservan los permisos descargados para operación sin conexión.
- El módulo se llama Inventario.
- Descuento se captura en pesos (hasta dos decimales). Porcentaje de referencia con dos decimales. La validación usa centavos exactos contra el máximo porcentual del rol, sin reconvertir el monto mediante un porcentaje redondeado. Se mantiene compatibilidad con solicitudes históricas por porcentaje.
- Vendedores: selección explícita de uno o varios mediante desplegable y etiquetas con opción de quitar. Código estable FBV- seguido del identificador en mayúsculas, visible en la ficha de empleado. Lector compatible: escribe texto y Enter en Escanear código de vendedor. No autentica ni confirma la venta. No añade dos veces al mismo empleado. Los códigos se descargan con los empleados para uso sin conexión. Se atribuye la venta a los seleccionados; no incorpora un nuevo cálculo de comisiones monetarias.
- Banco y últimos cuatro dígitos se muestran y requieren cuando tarjeta > 0. Referencia se muestra y requiere cuando transferencia > 0. Al retirar el medio se limpian y deshabilitan sus datos.
- Dos cajas simuladas históricas estaban abiertas además de las dos operativas. Se cerraron únicamente las simuladas (cuadre ficticio sin diferencia) con auditoría. Ahora hay una operativa abierta por sucursal. La semilla futura crea sesiones simuladas cerradas; el servicio ya impide otra apertura operativa por sucursal.

Verificación: 22 pruebas de integración aprobadas, más prueba adicional de segunda apertura bloqueada en ambas sucursales y las tres pruebas del reporte de cajas. HTTP rechaza PDF si receipts está desactivado aunque reprint esté activo. Navegador: $650 menos $259.16 = $390.84; porcentaje 39.87 %. Selección Melissa por menú y Ximena por código, datos bancarios condicionales, dos cajas abiertas totales. No se registraron ventas operativas durante la comprobación visual.

### Acceso visual condicionado a caja abierta — 4 de noviembre de 2026

Acuerdo: en ambos POS, mientras no exista una caja abierta, mostrar una pantalla de entrada «Caja cerrada». Ocultar navegación, productos, buscador, inventario, comprobantes, órdenes y consultas de caja. Permitir abrir caja según el permiso existente, actualizar/sincronizar, recuperar una petición pendiente y salir. Al abrir, habilitar la navegación; al cerrar, regresar a la pantalla de entrada. La administración central conserva su acceso independiente.

Se conserva el resumen inmediato del cierre y la impresión de ese comprobante, incluso para quien tiene `cash_close` sin `cash_summary`. Al descartarlo no se puede consultar el historial desde la pantalla bloqueada. Este cambio controla la interfaz del POS; no sustituye la autenticación ni los permisos del servidor.

Verificación: `tests/test_cash_lock.cjs` comprueba ambas sucursales, bloqueo de navegación, transición abierta/cerrada, permiso de apertura y excepción del comprobante inmediato. Revisión en navegador de pantalla bloqueada y apertura/cancelación del formulario, sin registrar operaciones.

### Ficha editable de producto y descripciones — 4 de noviembre de 2026

Los resultados de búsqueda del POS y la lista de Inventario/Artículos muestran descripción corta y larga. Administración dispone de «Editar», con ficha precargada, comparación previa y motivo obligatorio. Solo un administrador activo puede guardar en el endpoint administrativo; los POS no exponen esa ruta.

Se editan descripciones, material, categoría, peso, precio, costo, imagen y precio en etiqueta. El proveedor se muestra como referencia: otro proveedor requiere producto nuevo. No se editan existencias en la ficha. Material, tipo principal o peso modificados generan código nuevo y conservan el anterior en `aliases` del producto. La generación de códigos considera también esos alias y la búsqueda los reconoce con aviso de etiqueta anterior. Se exige confirmar la renovación de etiqueta. Peso vacío se conserva como NULL; peso informado debe ser positivo, hasta 999 g y tres decimales.

La edición utiliza transacción, revisión para detectar ediciones simultáneas, identificador para reintentos y auditoría antes/después. Requiere ambos POS conectados y sin operaciones pendientes. No reescribe comprobantes históricos. Limitación existente: los informes sin snapshot de costo siguen recurriendo al catálogo; la confirmación de edición lo informa. El versionado general de precios offline continúa pendiente.

Verificación en base desechable: edición autorizada, rechazo de personal no administrador, reintento sin duplicación, revisión obsoleta, validaciones de campos, conservación de existencias/eventos y alias sin reutilización. Regresión de alta/ingreso y categorías; comprobación de formulario precargado y ambas descripciones.

### Navegación y carga de órdenes — 4 de noviembre de 2026

Entrar en Apartados, Reparaciones o las vistas de órdenes cambia de pantalla inmediatamente. La consulta continúa en segundo plano con círculo giratorio y barra indeterminada (sin porcentaje ficticio). La primera carga no muestra conteos cero ni formularios antes de recibir datos. Las actualizaciones conservan los resultados previos con aviso de actualización. Un fallo muestra el error y permite reintentar sin un ciclo automático de solicitudes fallidas.

Las consultas simultáneas de órdenes comparten la misma promesa. La finalización no devuelve al usuario a una sección abandonada ni cierra un formulario. Se descartan respuestas de una sesión anterior. Las operaciones que registran cambios siguen esperando su confirmación y mantienen sus validaciones. La animación respeta la preferencia de movimiento reducido.

Verificación: `tests/test_orders_loading.cjs`, navegación con respuesta pendiente, cambio entre vistas sin consultas duplicadas, salida durante carga, actualización, fallo inicial, reintento y respuesta de sesión anterior.

### Cobro con importe exacto — 4 de noviembre de 2026

En nuevas ventas del POS se captura el efectivo aplicado, no el billete recibido. Efectivo, tarjeta y transferencia deben sumar exactamente el total. El servicio local rechaza sobrantes o faltantes antes de guardar una operación, también sin conexión. Se conserva la compatibilidad de los registros anteriores y no se modifican ventas guardadas. El detalle de venta y su PDF muestran una única línea de Efectivo y omiten Cambio. Esta actualización corresponde al cobro de ventas; los flujos de órdenes y cambios comerciales conservan sus validaciones actuales.

Verificado en base desechable: faltantes y sobrantes rechazados sin insertar operaciones, pago mixto exacto, validación offline y PDF sin la línea Cambio.

### Consulta de correcciones — 4 de noviembre de 2026

«Consultar y corregir» abre inmediatamente un diálogo con indicador animado. La consulta se ejecuta en segundo plano, permite cancelar y muestra error con reintento. Una respuesta tardía no reabre el diálogo cerrado ni sustituye una consulta posterior. Solo se habilita el formulario al recibir los datos actuales.

La ruta `correction-view` conserva la sincronización inicial, autenticación y validación de sucursal; omite el respaldo completo que se ejecutaba al consultar y la segunda sincronización posterior a la lectura. Las rutas de escritura conservan sus respaldos y sincronización. Prueba de interfaz: `tests/test_correction_loading.cjs`; comprobación aislada del despachador de rutas confirma respaldo al guardar y ausencia de respaldo al consultar. No se han medido tiempos antes/después en la sesión del usuario.

### Indicadores comunes de actividad — 4 de noviembre de 2026

Revisión de acciones que esperan al servidor: comparación/confirmación de correcciones y cambios, consulta de órdenes, guardado de catálogo y configuración, ingresos de mercancía, movimientos de caja, pagos/entregas de órdenes, exportaciones, sincronización manual y respaldos. Se incorpora un indicador común en botón y aviso flotante, con texto según la acción y umbral de 180 ms para evitar parpadeo en respuestas rápidas. Las operaciones conservan el bloqueo de doble envío; al terminar o fallar se restaura el estado previo del botón. Los diálogos de acciones pendientes no se pueden cerrar por Escape o la X; las consultas cancelables que ya cargan en segundo plano conservan su comportamiento.

También se anima la preparación de comprobantes en su propia ventana, el cálculo de resumen de cierre y la carga de informes de caja. Se respeta movimiento reducido. No se muestran porcentajes estimados. No se alteran datos, validaciones ni tiempos artificialmente; esta revisión identifica esperas de red en el código, no constituye medición de latencia de cada operación.

Verificación: `tests/test_activity.cjs`, regresión de carga de inicio de sesión y bloqueo de caja, comprobación de sintaxis de los scripts modificados.

### Anulación independiente y ticket de cancelación
Se retiró la creación de ventas correctas vinculadas tanto de la interfaz como de la validación central. Los registros antiguos siguen disponibles para consulta. Al anular se conserva el original, se revierten existencias y reconocimiento de importes, y se abre el comprobante con solicitud de impresión. Un fallo de impresión permite reintentar desde el resultado o historial, sin repetir la anulación. Dashboard también permite consultar estos tickets.
Validado en base desechable: rechazo de reemplazo, anulación idempotente, ticket de 58/80 mm, nueva venta independiente, bloqueo por cambios vinculados, caja cerrada y código 99. Prueba de interfaz cubre impresión automática, fallo de guardado y ventana bloqueada. La cancelación no revierte cobros bancarios.

### Cierre de ajustes de interfaz y comprobantes
- Cancelación directa con motivo y permisos, sin comparación previa; estado Cancelada en comprobantes.
- Tickets compactos de cancelación, movimientos de efectivo, apertura y cierre; los cierres conservan sus importes de control.
- Autocompletado desactivado en formularios y controles iniciales y dinámicos.
- Validación antes de publicar: 51 pruebas Python (46 pasan en ejecución general y cinco pruebas antiguas actualizadas y repetidas con resultado correcto); todas las pruebas JavaScript pasan. Las pruebas utilizan bases desechables.
