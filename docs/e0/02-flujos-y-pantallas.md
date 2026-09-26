# Flujos, estados y pantallas

E0 v1.0 · 23/09/2026 · Diseño funcional basado en el PDF v2. Los nombres internos de estado son propuestas; los comportamientos citados conservan los acuerdos.

## Mapa de pantallas

| Código | Pantalla | Usuario / entrada | Contenido y acciones |
| --- | --- | --- | --- |
| P01 | Venta y pago | POS, caja abierta | Buscar/escanear; cantidades; vendedores; descuento global autorizado; medios combinados; confirmar y ticket |
| P02 | Caja | POS, derecho específico | Apertura, fondo, entradas/gastos/retiros, conteo ciego, cierre, fondo/sobre |
| P03 | Apartados | POS online | Cliente/piezas; anticipo; abonar; liquidar; entregar; liberar/cancelar con autorización |
| P04 | Reparaciones | POS online | Cliente/piezas; presupuesto; anticipo; estados; liquidación/entrega y comprobantes |
| P05 | Clientes y saldo | POS online / administración | Buscar/editar; saldos por origen/vigencia; aplicar con código; emisión/reimpresión controlada |
| P06 | Mercancía | POS online con permisos / administración | Alta/importación, ingreso recurrente, etiquetas, traspasos/estados/bajas |
| P07 | Cambios | POS online autorizado | Buscar origen; piezas retornadas/nuevas; valor reconocido; diferencia; comprobantes |
| P08 | Correcciones | POS o administración online | Original; acción; motivo; antes/después; autorización; confirmación auditable |
| D01 | Resumen | Solo administrador | Brutas, descuentos, netas, cobros, beneficio; filtros y gráfica; frescura por local |
| D02 | Comprobantes | Solo administrador | Fecha/hora/folio/cliente/vendedor/tipo; tabla, panel y vínculos; PDF protegido |
| D03 | Caja | Solo administrador | Abiertas primero; cerradas recientes; esperado/contado/diferencia; original/ajustado |
| D04 | Inventario | Solo administrador | Almacén/estado/producto; movimientos, mínimos y alertas |
| D05 | Seguimiento de órdenes | Solo administrador | Apartados por vencer/liquidados sin entregar; reparación por estado/plazo; entrega solo POS |
| D06 | Vendedores | Solo administrador | Atribución, porcentaje y cálculos guardados; revisión tras corrección |
| D07 | Alertas | Solo administrador | Origen, revisada/resuelta, observación; historial de recurrencias |
| D08 | Configuración y clientes | Solo administrador | Catálogos/permisos/plazos/códigos/saldo manual/unificación según derechos |

El prototipo desarrolla navegación y los recorridos base; las acciones no implementadas en la maqueta se identifican como diseño pendiente, sin aparentar una operación exitosa.

## F01 · Venta de mostrador

1. Identificar dispositivo/sucursal y operador. Verificar sesión de caja abierta; registrar vendedores independientemente del operador.
2. Buscar producto por código vigente o alias histórico, o descripción. Mostrar disponibilidad conocida de Coyoacán y estado de conexión. Bloquear cantidades insuficientes; apartadas/dañadas no cuentan.
3. Preparar partidas con descripción/precio/costo histórico y cantidad. Descuento global solo con derecho/límite; solicitar autorización puntual si procede. D01 resuelve modalidades y redondeo.
4. Elegir cliente opcional; obligatorio si se usa saldo. Capturar efectivo recibido/aplicado/cambio, tarjeta y transferencia con sus datos. Máximo una de cada una de estas dos últimas. Saldo requiere internet, cliente, código y permiso.
5. Mostrar resumen. Guardar operación con todos sus efectos y folio antes de confirmar. Descontar conocimiento local, registrar pagos y atribución. La tarjeta y transferencia se verifican fuera del sistema.
6. Emitir ticket; si falla la impresora, conservar venta y ofrecer reimpresión. Sin internet queda pendiente; reconectar reenvía el mismo identificador.

**Estados técnicos propuestos:** borrador → guardada pendiente → recibida centralmente, o recibida con incidencia. Impresión tiene estado independiente. Un timeout no demuestra rechazo: consultar/reintentar la misma operación. Nunca volver a cobrar porque faltó el acuse. Las ventas cobradas con discrepancia se conservan.

**Errores:** caja cerrada, cantidad conocida insuficiente, descuento sin derecho, total no cubierto, metadatos incompletos, saldo sin conexión. Mostrar causa y conservar el borrador. Si no se pudo guardar localmente, no anunciar venta registrada. Pruebas A01-A05/A11/A14; VTA/PAG/OFF/VEN.

## F02 · Caja

Estados: cerrada → abierta → conteo en captura → cerrada. Una sesión operativa por sucursal. La captura de conteo no revela esperado; el servidor también debe aplicar esa restricción de acceso.

1. Abrir con fondo sugerido anterior, confirmable distinto; guardar diferencia sin compensar descuadre antiguo.
2. Vincular cada cobro neto de efectivo, entrada, gasto/retiro a sesión, usuario, motivo y autorización. Tarjeta/transferencia/saldo no son efectivo.
3. Capturar efectivo físico a ciegas; después comparar esperado. Guardar contado, esperado original, diferencia y observación opcional.
4. Distribuir contado entre fondo siguiente y sobre; ambos deben sumar contado. Se puede cerrar con faltante/sobrante y volver a abrir ese día.
5. Guardar secuencia antes de confirmar. Sincronizar cierre incluso si llega después de otra apertura, manteniendo orden causal.

Corrección posterior nunca modifica el conteo, fondo o sobre originales; genera vista ajustada. Recuperar un POS no permite abrir dos sesiones por error; protocolo D19 pendiente. Pruebas A02/A12/A13/A25; CAJ.

## F03 · Apartados

Se mantienen dos ejes: **económico** pendiente/liquidado y **custodia** reservado/entregado/liberado. Vencido es condición calculada de un pendiente, no liberación automática. Liquidado pendiente de entrega no es vencido por falta de pago.

1. Online, cliente con nombre/teléfono, piezas disponibles, precio/costo congelados y vendedores iniciales. Anticipo mínimo 40%, sin descuento. Reserva del conjunto y primer pago se confirman juntos.
2. Abonos positivos hasta cubrir saldo en cualquiera de los locales; dinero en la caja receptora, vendedores originales intactos. Cada movimiento emite copias cliente/negocio.
3. Liquidación reconoce venta y atribución completa una vez y activa COR-17. D02 decide sucursal de reconocimiento. La reserva/custodia sigue controlada hasta entrega.
4. Entrega completa solo POS online autorizado; no se cambian piezas ni se entregan parcialmente. Para entregas separadas se crean apartados separados. Entregar no suma otra venta.
5. Plazo conservado por orden; actual 45 días, inclusive fin del día 45. Desde siete días antes alerta. Vencido pendiente puede liberarse manualmente o liquidarse con excepción autorizada antes de liberar. Conservar pagos/historial; sin devolución de dinero según política fuente.
6. Cancelación comercial hasta fin del día 7: reconoce pagado, libera originales, entrega mercancía igual/mayor y cobra diferencia. Se conserva atribución previa, diferencia a quienes atienden. D03/D06 precisan reporte y saldo usado.

Después de liquidado y entregado, cambio conforme política general con plazo desde entrega. COR-17 bloquea cambios económicos desde liquidar, no desde entregar. Pruebas A18/A19/A25/A26; APA/CAL/COR.

## F04 · Reparaciones

Ejes: **trabajo** recibida → en reparación → lista para entregar → entregada; cancelada solo bajo condiciones. **Pago** pendiente/liquidada. Mantener `inició_trabajo_alguna_vez` derivado del historial, no solo estado actual.

1. Online, cliente, piezas propias del cliente fuera de inventario vendible, instrucciones, presupuesto y entrega prevista. Mínimo 50% y tres comprobantes al recibir. Matanga sin atribución comercial; operador siempre identificado.
2. Estado puede avanzar desde dashboard a en reparación/lista. Presupuesto pendiente admite cambio autorizado con motivo y acuerdo del cliente; subir no exige nuevo anticipo. Bajar por debajo de pagado genera exceso como saldo, con tratamiento de liquidación pendiente D05.
3. Solo anticipo y liquidación final; no abonos intermedios ni descuento. Liquidar activa COR-17; no requiere que el trabajo ya esté listo, pero la entrega requiere listo y liquidado.
4. Lista inicia plazo conservado de 45 días de recogida. Al exceder se alerta, sin baja/cancelación/cobro automático. Corregir lista a en reparación suspende ese plazo; nueva lista inicia plazo completo, dejando historial.
5. Entregar conjunto completo solo POS online; dos copias, interna con firma manuscrita.
6. Cancelar únicamente recibida, nunca antes en reparación, no liquidada y autorizado. Devolver piezas y aplicar anticipo a mercancía igual/mayor, sin saldo guardado automático; valor previo Matanga y diferencia atribuida. Ticket interno firmado.

Si una corrección regresa de en reparación a recibida, permanece prohibido cancelar. Orden liquidada puede avanzar trabajo/entrega, pero no cambiar economía. A20-A22/A25; REP.

## F05 · Cambios comerciales

Buscar origen por ticket o consulta → seleccionar unidades originales no cambiadas → validar buen estado y plazo inclusive día 15 → valorar con precio pagado neto original → elegir nuevas piezas y descuento autorizado → exigir neto nuevo igual/mayor → cobrar solo diferencia → confirmar entradas/salidas, atribución y comprobantes enlazados.

Operación nueva con fecha propia; nunca borra original/cierre. Nuevas piezas reciben plazo nuevo; las no cambiadas conservan anterior. Se atiende en ambos locales, con entrada al compartido de Coyoacán. Descuento parcial/costo/beneficio siguen D01/D03. Si original usó saldo, no restituirlo además del valor reconocido. Garantías fuera de política definida. A23; CAM/CLI-23.

## F06 · Correcciones

Buscar → ver original y vínculos → escoger acción según derecho → motivo obligatorio → antes/después con efectos en caja/inventario/atribución → autorización → confirmar una vez → conservar original y documento de corrección.

| Acción | Precondición | Efecto | Bloqueo |
| --- | --- | --- | --- |
| Corregir medio/reparto | Online y derecho; total conservado | Ajuste de medios vinculado a caja original, no dinero físico hoy | Orden liquidada; saldo sin sus controles |
| Corregir vendedores | Derecho independiente y conjunto válido | Redistribuir neto; señalar cálculos guardados, sin alterar pagos/productos | Regla aplicable a operación concreta; nunca conceder otro derecho implícito |
| Anular venta errónea | Derecho, motivo, no anulada antes | Revertir una vez y conservar original | Venta con cambios vinculados |
| Reemplazar partidas | Anular y registrar correcta vinculada | Pago registrado correcto sin cobrar otra vez; inventario con fechas reales | Diferencia de importe sin D04 resuelto |
| Anular pago de orden | Solo admin; orden pendiente | Recalcular saldo y restituir saldo usado con vigencia | Liquidada; mínimos resultantes pendientes D05 |

No hay límite temporal general. Fechas de operación, corrección y movimiento de inventario se separan. Ticket interno si POS; dashboard no envía impresión. Corrección de pagos que consume saldo exige código/derecho/disponible; restituir no prorroga. A24/A25; COR.

## F07 · Mercancía y clientes

Importación: archivo de un almacén → validar TODO → errores descargables o vista previa → confirmar ingreso único → etiquetas/comprobante. Recurrente: buscar → reactivar si procede → cantidad/almacén → costo/precio opcionales autorizados → vista previa → confirmar. Traspaso conserva estado/reserva y revalida disponibilidad; salida de Coyoacán necesita ambos POS sincronizados. Reversión solo total y una vez, según D12. Conteo físico externo.

Saldo: identificar cliente → verificar código y derecho online → consumir por vencimiento/antigüedad en transacción atómica → registrar cada origen y remanente. Reimprimir código requiere derecho/motivo; cinco fallos consecutivos bloquean globalmente. Solo admin sustituye/desbloquea/crea saldo manual/unifica. Unificación conserva importes, vigencias y bloqueo e invalida códigos previos. A07-A10/A15-A17.

## F08 · Consulta administrativa

Filtros aplicables → cifras/gráfica/tabla del MISMO universo → abrir detalle → navegar al origen → exportar con filtros y estado de actualización. Datos tardíos no aparecen como completos. Alertas: activa → revisada (puede seguir activa) → resuelta cuando desaparece causa; si reaparece, nueva vinculada. Cálculo de comisión es una captura; recalcular no lo sobrescribe. A26-A28.
