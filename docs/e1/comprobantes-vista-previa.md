# Vista previa e impresión de comprobantes

Las acciones «Ver comprobante» / «Ver e imprimir» abren una ventana independiente. No descargan archivos ni imprimen automáticamente. El botón Imprimir abre el diálogo del navegador, donde también se puede elegir Guardar como PDF. Deben permitirse ventanas emergentes del sitio local.

La vista previa usa el PDF autorizado de la operación, renderizado a 300 ppp, conservando todas las copias y las instantáneas de órdenes. Las páginas de impresión conservan sus dimensiones de ticket (58/80 mm). La impresora y su controlador deben admitir el papel elegido; las pruebas actuales no certifican una impresora física.

Requisito Linux: `pdftoppm` del paquete `poppler-utils`. Si falta, se devuelve un error explícito sin alterar la operación. Los archivos intermedios se eliminan al terminar la conversión. La respuesta autenticada tiene Cache-Control: no-store; no se publican comprobantes mediante enlaces permanentes.

El panel lateral usa `brand-symbol.png`. Los comprobantes combinan los originales transparentes `brand-symbol.png` y `brand-name.png`. Las plantillas con el antiguo logo corporativo se representan con la marca nueva sin reescribir los datos históricos. Se respetan los logos personalizados y la opción de quitar logo de las plantillas de venta.

Los endpoints PDF anteriores permanecen disponibles para compatibilidad. Las exportaciones CSV siguen descargándose. Los permisos de consulta/reimpresión se siguen validando en el servidor.
