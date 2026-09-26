# Matriz de requisitos por identificador

E0 v1.0 · 23/09/2026

**209 identificadores impresos**, incluidos grupos exactamente como aparecen en el PDF. Se cotejaron texto y página contra el PDF real; los IDs agrupados no se expanden a números inventados. Fuente SHA-256: `5d00d23a12eea66ebcc2e49762b9d77e2477fffc185b196e3bc3de394f9c9329`.

Esta es trazabilidad de diseño, no evidencia de implementación. Las pruebas A01-A30 se encuentran en [08-pruebas-aceptacion.md](08-pruebas-aceptacion.md). Las tareas están definidas en [06-tareas-y-puerta-e1.md](06-tareas-y-puerta-e1.md). Los acuerdos sin ID (tablas, notas, fórmulas) se conservan por las reglas transversales, flujos y decisiones E0; consultar siempre la página fuente completa.

## GEN-01

**Fuente:** PDF v2, p. 3. **Regla:** La primera versión que entre en operación deberá sustituir completamente el programa actual, incluyendo apartados y reparaciones. El desarrollo puede dividirse en etapas, pero la sustitución operativa no debe omitir esos módulos.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## GEN-02

**Fuente:** PDF v2, p. 3. **Regla:** Las sucursales 1 y 2 de Coyoacán usarán el POS desde sus computadoras. Se prefiere una aplicación web y herramientas de código abierto. Se busca poder utilizar Linux; la impresión y los periféricos deben validarse en las máquinas reales.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## GEN-03

**Fuente:** PDF v2, p. 3. **Regla:** El administrador tendrá acceso remoto mediante navegador a un dashboard privado y a la gestión del negocio. La consulta de costos en el POS seguirá protegida por permisos, aunque el dashboard sea exclusivo del administrador.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## GEN-04

**Fuente:** PDF v2, p. 3. **Regla:** La operación tendrá fecha y hora reales, sucursal y usuario. Los registros históricos que carezcan de hora no deben presentarse como si se conociera la hora original.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## GEN-05

**Fuente:** PDF v2, p. 3. **Regla:** Se distinguirán sucursales, almacenes, usuarios vendedores, operadores y personas que autorizan. Estos conceptos no deben confundirse entre sí.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ALM-01

**Fuente:** PDF v2, p. 4. **Regla:** Existirán tres almacenes: Coyoacán, oficina y Santa Rosa. Coyoacán abastece las ventas de ambos locales; oficina guarda mercancía adicional y Santa Rosa concentra la reserva principal.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ALM-02

**Fuente:** PDF v2, p. 4. **Regla:** La última definición del usuario mantiene un inventario general de Coyoacán, sin separar su consulta de existencias por sucursal. Las ventas y cajas sí se identifican por sucursal.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ALM-03

**Fuente:** PDF v2, p. 4. **Regla:** Se podrá dar de alta mercancía en cualquiera de los tres almacenes. Las existencias se controlarán por código, almacén y estado, diferenciando disponibles, apartadas y dañadas.

**Tarea:** E0-01 (E0). **Pantalla:** Documento de alcance. **Depende de:** Base para E1.

**Decisiones relacionadas:** Ninguna para definir alcance. **Pruebas:** A01, A28, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01,A28,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ARQ-01

**Fuente:** PDF v2, p. 5. **Regla:** Las operaciones de ambos POS se concentrarán en el servidor de la aplicación y su base de datos central. El dashboard consultará los datos recibidos por ese servidor.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ARQ-02

**Fuente:** PDF v2, p. 5. **Regla:** El POS necesitará conservar localmente las operaciones permitidas durante un corte de internet y enviarlas al recuperar la conexión. La interfaz web por sí sola no define cómo se logra esta persistencia.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ARQ-03

**Fuente:** PDF v2, p. 5. **Regla:** Cada sucursal mostrará el estado de conexión y sincronización. El administrador verá la última actualización recibida y sabrá cuándo la información es incompleta.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ARQ-04

**Fuente:** PDF v2, p. 5. **Regla:** Los cambios remotos de datos y permisos deberán llegar a los POS conectados. Si un local está sin internet, no se deberá asumir que ya recibió esos cambios.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-01

**Fuente:** PDF v2, p. 6. **Regla:** Las operaciones se guardarán localmente antes de confirmarse y se enviarán al recuperar internet, conservando fecha, hora, sucursal, usuarios, pagos y sesión de caja de origen.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-02

**Fuente:** PDF v2, p. 6. **Regla:** Un reintento no generará otra venta, pago o movimiento. Cerrar el navegador o reiniciar el equipo no deberá borrar operaciones guardadas y pendientes.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-03

**Fuente:** PDF v2, p. 6. **Regla:** Se conservará la secuencia apertura, movimientos, cierre y nueva apertura. La fecha de recepción en el servidor no sustituirá la fecha real de operación.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-04

**Fuente:** PDF v2, p. 6. **Regla:** Se conservarán las ventas cobradas que generen discrepancias al sincronizar. Se alertará sin descartarlas, ocultarlas o duplicarlas. Se detallan las reglas de disponibilidad en la sección 36.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ACC-01

**Fuente:** PDF v2, p. 7. **Regla:** Existirán derechos de acceso específicos por usuario. No todos podrán registrar ventas, consultar costos, registrar entradas de efectivo, gastos, retiros, descuentos o cambios de inventario.

**Tarea:** E1-01 (E1). **Pantalla:** Acceso y autorización. **Depende de:** E0-03,E0-05.

**Decisiones relacionadas:** D18. **Pruebas:** A01.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ACC-02

**Fuente:** PDF v2, p. 7. **Regla:** Una persona sin determinado derecho podrá solicitar una autorización puntual a otra persona que sí lo tenga. Se registrarán tanto quien realiza la operación como quien la autoriza. La autorización no cambiará la atribución de vendedores.

**Tarea:** E1-01 (E1). **Pantalla:** Acceso y autorización. **Depende de:** E0-03,E0-05.

**Decisiones relacionadas:** D18. **Pruebas:** A01.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ACC-03

**Fuente:** PDF v2, p. 7. **Regla:** El código de barras del vendedor identificará la atribución comercial. Debe distinguirse de la clave utilizada para conceder derechos o autorizar operaciones.

**Tarea:** E1-01 (E1). **Pantalla:** Acceso y autorización. **Depende de:** E0-03,E0-05.

**Decisiones relacionadas:** D18. **Pruebas:** A01.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ACC-04

**Fuente:** PDF v2, p. 7. **Regla:** La aplicación de descuentos sin conexión deberá respetar los derechos disponibles localmente. Los límites concretos por usuario y la política de actualización de permisos deberán documentarse en una matriz de acceso.

**Tarea:** E1-01 (E1). **Pantalla:** Acceso y autorización. **Depende de:** E0-03,E0-05.

**Decisiones relacionadas:** D18. **Pruebas:** A01.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A01; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## VEN-01

**Fuente:** PDF v2, p. 7. **Regla:** Una venta podrá atribuirse a uno o varios vendedores. Si participan varios, el importe neto se repartirá por partes iguales entre ellos; por ejemplo, $1,000 entre dos vendedores equivale a $500 para cada uno.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## VEN-02

**Fuente:** PDF v2, p. 7. **Regla:** El importe acumulado de ventas de un vendedor es independiente del porcentaje de comisión. El administrador podrá aplicar posteriormente un porcentaje a ese acumulado; cambiarlo no modificará las ventas atribuidas.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## VEN-03

**Fuente:** PDF v2, p. 7. **Regla:** Las reparaciones se registrarán bajo “Matanga”, como operaciones sin asignación comercial a un vendedor. Se conservará de todas formas la identidad de quien recibe, cobra o entrega.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## VTA-01

**Fuente:** PDF v2, p. 8. **Regla:** Para cobrar una venta deberá existir una sesión de caja abierta en el local. La venta conservará sus productos, cantidades, precios, descuento, pagos, fecha y hora, sucursal, operador y vendedores atribuidos.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## VTA-02

**Fuente:** PDF v2, p. 8. **Regla:** El descuento se aplicará sobre el total de la venta, con los derechos de acceso correspondientes. Los límites se definirán como parte de dichos derechos. No habrá descuentos en apartados ni en presupuestos de reparación.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## PAG-01

**Fuente:** PDF v2, p. 8. **Regla:** Se aceptarán efectivo, tarjeta, transferencia y saldo a favor. En una misma venta se permitirá como máximo una tarjeta y una transferencia, además de efectivo y saldo a favor cuando aplique. Usar saldo a favor exige cliente, código, derecho específico y conexión.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## PAG-02

**Fuente:** PDF v2, p. 8. **Regla:** La tarjeta se cobrará en una terminal independiente. La transferencia se verificará por fuera del POS. Posteriormente se registrarán manualmente ambos pagos; no se ha solicitado integración bancaria.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## PAG-03

**Fuente:** PDF v2, p. 8. **Regla:** Para tarjeta se capturarán crédito o débito, banco y últimos cuatro dígitos. No se ha requerido distinguir redes de tarjeta. Para transferencia se capturará la referencia que permita corroborarla.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## PAG-04

**Fuente:** PDF v2, p. 8. **Regla:** El cambio se calculará exclusivamente sobre el efectivo recibido. Se distinguirán efectivo recibido, aplicado y cambio entregado. Los importes aplicados deberán cubrir el total, sin usar tarjeta o transferencia para producir cambio en efectivo.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## PAG-05

**Fuente:** PDF v2, p. 8. **Regla:** Los mismos medios podrán utilizarse para diferencias de cambios, pagos de apartados y pagos de reparaciones, respetando sus reglas y la conexión obligatoria de esos módulos.

**Tarea:** E3-01 (E3). **Pantalla:** P01 Venta y pago. **Depende de:** E1-02,E2-02; saldo E4.

**Decisiones relacionadas:** D01, D18. **Pruebas:** A11, A14.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A11,A14; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-01

**Fuente:** PDF v2, p. 9. **Regla:** Cada local tendrá una caja compartida y solamente una sesión abierta a la vez. Se podrá abrir y cerrar sin depender del día o de un turno fijo, incluso varias veces en la misma fecha.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-02

**Fuente:** PDF v2, p. 9. **Regla:** En cada apertura el responsable capturará el fondo inicial. Se sugerirá el fondo dejado en el cierre anterior, pero podrá confirmarse un monto distinto. Se conservará la diferencia sin compensar automáticamente un descuadre anterior.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-03

**Fuente:** PDF v2, p. 9. **Regla:** El cierre será con conteo ciego: primero se contará y capturará el efectivo físico; después se mostrará la comparación con el importe esperado. La consulta del administrador no debe revelar anticipadamente esa comparación al cajero.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-04

**Fuente:** PDF v2, p. 9. **Regla:** Se podrá cerrar con faltante o sobrante. Se guardarán el efectivo esperado, el contado, la diferencia y una observación opcional. La diferencia quedará disponible para revisión posterior del administrador.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-05

**Fuente:** PDF v2, p. 9. **Regla:** Se registrarán por separado el efectivo que queda como fondo siguiente y el efectivo que se guarda en el sobre. Esos importes representan la distribución del efectivo contado, no ventas nuevas.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-06

**Fuente:** PDF v2, p. 9. **Regla:** Se permitirán entradas adicionales, gastos y retiros de efectivo. Cada movimiento requerirá importe, motivo, usuario, fecha, hora, sesión y autorización cuando el operador no tenga el derecho necesario.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAJ-07

**Fuente:** PDF v2, p. 9. **Regla:** Aperturas, cierres y movimientos anteriores funcionarán sin conexión y se sincronizarán posteriormente, conservando su secuencia y sin duplicarse.

**Tarea:** E3-02 (E3). **Pantalla:** P02/D03 Caja. **Depende de:** E1-02,E3-01.

**Decisiones relacionadas:** D19. **Pruebas:** A02, A12, A13.

**Conectividad:** Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A12,A13; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-01

**Fuente:** PDF v2, p. 10. **Regla:** La política comercial no contempla devolver dinero. Se podrán cambiar algunas o todas las piezas de una venta por mercancía cuyo total, después del descuento autorizado, sea igual o mayor al valor reconocido de las piezas devueltas.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-02

**Fuente:** PDF v2, p. 10. **Regla:** Se exigirá conexión y autorización. El cambio se podrá atender en cualquiera de las dos sucursales. Las piezas recibidas volverán al inventario compartido de Coyoacán.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-03

**Fuente:** PDF v2, p. 10. **Regla:** Se admitirán cambios hasta 15 días naturales después de la compra. Se incluye el final del día natural 15. Las piezas entregadas mediante un cambio tendrán un nuevo plazo de 15 días a partir de ese cambio; las piezas no cambiadas conservarán su plazo original.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-04

**Fuente:** PDF v2, p. 10. **Regla:** Se solicitará el ticket al cliente; si no lo tiene, se podrá buscar la operación. Se verificará el origen de las piezas y que no hayan sido cambiadas previamente. Deberán estar en buenas condiciones, sin rayaduras ni defectos.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-05

**Fuente:** PDF v2, p. 10. **Regla:** El valor del cambio se basará en el importe pagado por los artículos recibidos, considerando el descuento original, no en su precio de venta actual. El reparto exacto del descuento y los redondeos deben quedar documentados.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-06

**Fuente:** PDF v2, p. 10. **Regla:** La venta original y su cierre de caja se conservarán. Un cambio realizado otro día será una operación nueva vinculada a la original, con su propia fecha y hora. Solo la diferencia efectivamente cobrada ingresará como nuevo pago.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-07

**Fuente:** PDF v2, p. 10. **Regla:** La atribución del valor original permanecerá con los vendedores originales. El importe adicional se atribuirá a quienes atiendan el cambio, repartido entre ellos según la regla de participación.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAM-08

**Fuente:** PDF v2, p. 10. **Regla:** Se emitirán comprobantes para el cliente y el local con la operación de origen, mercancía recibida y entregada, importes, descuento, diferencia, pagos y datos de la operación. La diferencia podrá pagarse como una venta ordinaria.

**Tarea:** E6-01 (E6). **Pantalla:** P07 Cambios. **Depende de:** E2,E3,E4,E5.

**Decisiones relacionadas:** D01, D03, D06. **Pruebas:** A19, A22, A23.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A19,A22,A23; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-01

**Fuente:** PDF v2, p. 11. **Regla:** Todas las operaciones de apartados requerirán conexión. Un apartado podrá incluir varias piezas como un conjunto; se registrarán nombre, teléfono del cliente y una observación opcional.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-02

**Fuente:** PDF v2, p. 11. **Regla:** El anticipo mínimo será del 40% del valor total de las piezas. No se permitirán descuentos. Se conservarán el precio y el costo existentes al registrar el apartado.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-03

**Fuente:** PDF v2, p. 11. **Regla:** El cliente podrá abonar cualquier cantidad positiva, sin exceder el saldo pendiente, hasta liquidar. Cada pago conservará su fecha, hora, medios de pago, operador y sucursal. Se podrá pagar en cualquiera de los locales.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-04

**Fuente:** PDF v2, p. 11. **Regla:** Las piezas permanecerán reservadas y no podrán sustituirse mientras el apartado esté pendiente. Si contiene varias piezas, deberá liquidarse en conjunto y entregarse completo. Para retirar piezas por separado deberán registrarse apartados separados desde el inicio.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-05

**Fuente:** PDF v2, p. 11. **Regla:** La liquidación y la entrega serán hechos distintos. Un apartado liquidado que todavía no se recoge conservará las piezas bajo control. Desde la liquidación quedará bloqueado a correcciones económicas y de sus piezas; se podrá registrar la entrega y consultar o reimprimir comprobantes.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-06

**Fuente:** PDF v2, p. 11. **Regla:** La entrega solo se registrará desde el POS de cualquiera de las dos sucursales de Coyoacán, con conexión y los derechos correspondientes. El dashboard servirá para consultar el estado y el comprobante, no para efectuar esa entrega.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-07

**Fuente:** PDF v2, p. 11. **Regla:** Cada movimiento generará un comprobante para el cliente y otro para el local. Los abonos y la liquidación se vincularán al folio original; la reimpresión no generará otro pago.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-08

**Fuente:** PDF v2, p. 11. **Regla:** Los vendedores del registro inicial conservarán la atribución de toda la venta, aunque otros usuarios reciban abonos o entreguen las piezas. El monto se les atribuirá al liquidarse el apartado, no al recibir cada anticipo o abono.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-09

**Fuente:** PDF v2, p. 11. **Regla:** Una vez liquidado y entregado, la mercancía podrá cambiarse conforme a la política general, con el plazo correspondiente desde la entrega.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-10

**Fuente:** PDF v2, p. 12. **Regla:** El plazo vigente acordado es de 45 días naturales después de la fecha del apartado. Se incluye el final del día 45. Sustituye al plazo de 90 días planteado antes. Se podrá configurar para nuevos apartados; los existentes conservarán el plazo que se les asignó.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-11

**Fuente:** PDF v2, p. 12. **Regla:** Al vencer un apartado pendiente de liquidación, se alertará para revisión. Una persona autorizada confirmará la liberación de las piezas. No se liberarán automáticamente por el simple paso del tiempo.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-12

**Fuente:** PDF v2, p. 12. **Regla:** Conforme a la política indicada por el usuario, no se devolverá el dinero del apartado vencido. Las piezas quedarán disponibles cuando se confirme su liberación. Se conservarán los pagos y el historial de la decisión.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-13

**Fuente:** PDF v2, p. 12. **Regla:** Una persona con el derecho especial podrá autorizar una liquidación fuera del plazo antes de liberar las piezas. La excepción deberá quedar identificada en el historial.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-14

**Fuente:** PDF v2, p. 12. **Regla:** La cancelación temprana se permitirá hasta el final del día natural 7 después de la fecha del apartado. Requerirá conexión y autorización. Se podrán cambiar los importes pagados por mercancía de igual o mayor valor, sin devolución de dinero.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-15

**Fuente:** PDF v2, p. 12. **Regla:** El valor reconocido para esa cancelación será la suma realmente pagada, no el valor total del apartado. Se liberarán las piezas originales y se registrarán los artículos entregados y cualquier diferencia cobrada.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## APA-16

**Fuente:** PDF v2, p. 12. **Regla:** El importe pagado conservará la atribución de los vendedores originales; el importe adicional corresponderá a quienes atiendan el cambio. Deberán evitarse duplicidades en reportes y conservarse los documentos vinculados.

**Tarea:** E5-01 (E5). **Pantalla:** P03/D05 Apartados. **Depende de:** E2,E3,E4; cambios E6.

**Decisiones relacionadas:** D02, D05. **Pruebas:** A18, A19, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A18,A19,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-01

**Fuente:** PDF v2, p. 13. **Regla:** Todas las operaciones requerirán conexión. Una orden podrá incluir varias piezas del cliente; se recibirán, liquidarán y entregarán como un conjunto. Esas piezas no se incorporarán al inventario de mercancía para venta.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-02

**Fuente:** PDF v2, p. 13. **Regla:** Se registrarán cliente y teléfono, descripción de las piezas, instrucciones del trabajo, presupuesto acordado y la información de entrega prevista. Se conservará la sucursal de recepción.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-03

**Fuente:** PDF v2, p. 13. **Regla:** El presupuesto se determinará al recibir las piezas. Se exigirá al menos 50% de anticipo. No habrá descuentos en la reparación.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-04

**Fuente:** PDF v2, p. 13. **Regla:** Mientras no esté liquidada, se podrá aumentar o reducir el presupuesto con un derecho específico, conexión, motivo y acuerdo del cliente, conservando valores anteriores y autorización. Si aumenta, la diferencia se pagará al recoger sin exigir otro anticipo. Si baja por debajo de lo pagado, la diferencia se guardará como saldo a favor del cliente, sin devolver efectivo.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-05

**Fuente:** PDF v2, p. 13. **Regla:** Se registrarán únicamente anticipo y liquidación final, sin abonos intermedios. Se aceptarán los medios del POS, incluido saldo a favor con sus controles. La liquidación completa será necesaria para entregar y bloqueará cambios económicos, de pagos, piezas o presupuesto, conforme a COR-17.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-06

**Fuente:** PDF v2, p. 13. **Regla:** No habrá atribución comercial ni comisión de reparación para vendedores. Se clasificará como “Matanga - sin asignación”, conservando los usuarios que realizaron cada operación.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-07

**Fuente:** PDF v2, p. 13. **Regla:** Al entregar se emitirá comprobante para el cliente y para el negocio. La copia del negocio incluirá espacio para firma de conformidad del cliente, realizada a mano sobre el ticket impreso.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-08

**Fuente:** PDF v2, p. 14. **Regla:** Los estados serán recibida, en reparación, lista para entregar, entregada y cancelada. Cada transición guardará usuario, fecha, hora y estado anterior.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-09

**Fuente:** PDF v2, p. 14. **Regla:** Desde el dashboard se podrá cambiar de recibida a en reparación y a lista para entregar. La entrega física se registrará únicamente desde el POS de cualquiera de las dos sucursales de Coyoacán, con conexión y autorización.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-10

**Fuente:** PDF v2, p. 14. **Regla:** Habrá 45 días naturales para recoger, contados desde que la orden cambie a lista para entregar. Al superar el plazo se generará una alerta de revisión; no una baja, cancelación o cobro automático. Los plazos configurados deberán conservarse por orden.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-11

**Fuente:** PDF v2, p. 14. **Regla:** Las correcciones de estado requerirán derecho específico y motivo obligatorio. Se guardará el historial y no se borrarán pagos, comprobantes ni movimientos anteriores.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-12

**Fuente:** PDF v2, p. 14. **Regla:** Si una orden alguna vez pasó a en reparación, su cancelación quedará bloqueada aunque una corrección posterior la regrese a recibida. Se revisará el historial, no solo el estado actual.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-13

**Fuente:** PDF v2, p. 14. **Regla:** Si lista para entregar se registró por error y se corrige a en reparación, el plazo anterior dejará de aplicarse. Al volver a marcarla lista comenzará un plazo completo nuevo, conservando ambas fechas, el motivo y el usuario de la corrección; las alertas se ajustarán.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-14

**Fuente:** PDF v2, p. 14. **Regla:** La cancelación comercial se permitirá mientras siga recibida, nunca haya pasado a en reparación y no esté liquidada, con conexión y autorización. Se devolverán las piezas y el anticipo se aplicará a mercancía de igual o mayor valor, sin devolución de dinero. No crea automáticamente un saldo guardado para otra visita.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## REP-15

**Fuente:** PDF v2, p. 14. **Regla:** En esa cancelación se registrarán la devolución de piezas, mercancía entregada y diferencia pagada. El valor procedente de la reparación seguirá sin asignación comercial; la diferencia se atribuirá a quienes atiendan. Se emitirá comprobante interno con firma manuscrita de recepción de las piezas.

**Tarea:** E5-02 (E5). **Pantalla:** P04/D05 Reparaciones. **Depende de:** E3,E4; cambios E6.

**Decisiones relacionadas:** D05, D22. **Pruebas:** A20, A21, A22, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A20,A21,A22,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-01

**Fuente:** PDF v2, p. 15. **Regla:** Un producto podrá representar varias unidades con el mismo código de barras cuando tengan las mismas características. Esta definición sustituye al supuesto inicial de un código único para cada unidad física.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-02

**Fuente:** PDF v2, p. 15. **Regla:** Se registrarán material predominante, tipo de pieza, hasta dos niveles de subcategorías, descripción corta y larga, precio de venta, costo, proveedor, peso opcional y una imagen opcional. No se requieren campos específicos de pureza, talla o medidas.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-03

**Fuente:** PDF v2, p. 15. **Regla:** El material será un campo de identificación y filtro. Se podrá partir de plata, oro, tumbaga y alpaca y ampliar el catálogo. Si una pieza combina materiales, se asignará el predominante.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-04

**Fuente:** PDF v2, p. 15. **Regla:** El tipo de pieza funcionará como categoría principal para los reportes: aretes, anillos, dijes, pulseras, collares y los tipos adicionales que se requieran. Las dos subcategorías permitirán mayor detalle y se utilizarán como filtros.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-05

**Fuente:** PDF v2, p. 15. **Regla:** El precio se capturará manualmente. Cuando dependa del peso o material, ese cálculo se realizará por fuera del sistema. El costo será obligatorio y su consulta y modificación requerirán el derecho correspondiente.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-06

**Fuente:** PDF v2, p. 15. **Regla:** El peso será opcional para todos los productos, en gramos, con tres decimales y máximo de 999 gramos. No se deberá inventar un peso para completar una carga.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-07

**Fuente:** PDF v2, p. 15. **Regla:** Se admitirá una sola imagen opcional por producto, mediante archivo PNG o enlace. La descarga, almacenamiento y validación de enlaces se definirán técnicamente.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-08

**Fuente:** PDF v2, p. 15. **Regla:** Se asignará obligatoriamente un proveedor previamente registrado, mediante un identificador numérico. El catálogo deberá identificar al proveedor por nombre; teléfono, contacto y dirección podrán completar su ficha.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-09

**Fuente:** PDF v2, p. 15. **Regla:** Materiales, tipos, subcategorías y proveedores deberán existir antes de importarse productos. Se administrarán con derechos, conservarán sus claves y podrán desactivarse y reactivarse. Para volver a ingresar mercancía asociada a un catálogo inactivo, deberá reactivarse primero.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-20

**Fuente:** PDF v2, p. 16. **Regla:** Los códigos existentes se importarán como texto, conservando ceros y formato. Los nuevos serán numéricos y expresarán material, tipo de pieza, peso cuando se defina y un consecutivo.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-21

**Fuente:** PDF v2, p. 16. **Regla:** El esquema discutido es MM + TT + PPPPPP + NNNNN: dos dígitos de material, dos de tipo, seis para el peso en milésimas de gramo y cinco de consecutivo. El consecutivo tendrá el alcance acordado por combinación material/tipo, sin reutilizar identificadores.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-22

**Fuente:** PDF v2, p. 16. **Regla:** El precio no formará parte del código. Se podrá actualizar el producto; cambios de información codificada requerirán actualizar su identificación conservando el historial. Los códigos anteriores deberán mantener una relación con el producto para reconocer etiquetas previas, advertir que están desactualizadas y usar la información vigente. No se asignarán a otro producto; los detalles de reasignación requieren validación.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-23

**Fuente:** PDF v2, p. 16. **Regla:** La etiqueta mostrará la descripción y, por defecto, el precio de venta. Se podrá elegir por producto imprimir u omitir el precio. Reimprimir etiquetas no modificará existencias.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-24

**Fuente:** PDF v2, p. 16. **Regla:** El peso, cuando se imprima, se mostrará en clave; por ejemplo, 2.4 g como 2D4. Se podrá agregar un sufijo opcional configurable, como MX. Ese sufijo impreso no cambia el requisito de un código de barras numérico.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## INV-25

**Fuente:** PDF v2, p. 16. **Regla:** Una cantidad de cinco unidades iguales dará lugar a cinco etiquetas con el mismo código. Cuando las características o el peso sean distintos, se deberán distinguir los productos.

**Tarea:** E2-01 (E2). **Pantalla:** P06/D04 Catálogo y etiquetas. **Depende de:** E1-01,E1-03.

**Decisiones relacionadas:** D09, D10, D11, D21. **Pruebas:** A07.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A07; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-01

**Fuente:** PDF v2, p. 17. **Regla:** La plantilla se utilizará para productos nuevos. Cada fila corresponderá a un producto y contendrá una cantidad de unidades. No será necesario repetir cinco filas si ingresan cinco unidades idénticas.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-02

**Fuente:** PDF v2, p. 17. **Regla:** Cada archivo se destinará a un solo almacén. Se indicarán los datos obligatorios del producto, las claves de catálogos y la cantidad. El peso y la imagen serán opcionales; imprimir precio estará activado por defecto.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-03

**Fuente:** PDF v2, p. 17. **Regla:** La secuencia será cargar archivo, validar, mostrar vista previa, confirmar el ingreso y generar etiquetas. La vista previa permitirá revisar los datos y cantidades antes de afectar inventario.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-04

**Fuente:** PDF v2, p. 17. **Regla:** Si existe cualquier error, se bloqueará toda la carga. No se permitirán ingresos parciales del archivo. Los errores se corregirán en Excel y después se volverá a cargar.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-05

**Fuente:** PDF v2, p. 17. **Regla:** Se ofrecerá un reporte descargable de errores con fila, campo, valor y motivo, para facilitar la corrección. Los catálogos referidos deberán existir y ser válidos antes del ingreso.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-06

**Fuente:** PDF v2, p. 17. **Regla:** Se detectarán productos repetidos dentro del archivo y coincidencias con productos existentes para impedir altas duplicadas. Cuando corresponda se dirigirá al ingreso recurrente. La comparación contemplará material, tipo, subcategorías, descripciones y peso, normalizando mayúsculas y espacios. No se sumarán automáticamente filas repetidas.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-07

**Fuente:** PDF v2, p. 17. **Regla:** Se evitará que reintentar la confirmación o cargar nuevamente el mismo contenido produzca otro ingreso. Se conservará un folio de carga y su resultado para consultar lo ya realizado.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## IMP-08

**Fuente:** PDF v2, p. 17. **Regla:** Se generará un comprobante del ingreso completo con almacén, productos, cantidades, fecha y usuario. Los costos solo se mostrarán a usuarios con el derecho de consulta. El ingreso y la emisión de etiquetas serán trazables.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-01

**Fuente:** PDF v2, p. 18. **Regla:** Existirá un módulo dentro del POS para mercancía recurrente. Permitirá buscar un producto por descripción corta o larga, recuperar sus datos y capturar cantidad y almacén. No requerirá Excel.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-02

**Fuente:** PDF v2, p. 18. **Regla:** Se reutilizará el mismo código para mercancía con las mismas características, tenga actualmente existencia cero o positiva. Un producto inactivo deberá reactivarse antes de ingresarlo.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-03

**Fuente:** PDF v2, p. 18. **Regla:** Se ofrecerá actualizar el costo de forma opcional. Si se elige, se exigirá el derecho de acceso correspondiente. El costo actualizado aplicará a todas las unidades del código; no se modificará el costo histórico de operaciones ya registradas.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-04

**Fuente:** PDF v2, p. 18. **Regla:** También se podrá actualizar el precio con su permiso correspondiente. Se conservarán valor anterior, valor nuevo, usuario y fecha. El precio vigente será común a las unidades del código, preservando los precios de ventas y apartados existentes.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-05

**Fuente:** PDF v2, p. 18. **Regla:** Habrá vista previa y confirmación antes de ingresar. Se podrán emitir etiquetas con los datos actuales y consultar el comprobante e historial del ingreso.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-06

**Fuente:** PDF v2, p. 18. **Regla:** La reversión de un ingreso deberá abarcar todo el ingreso, con conexión, derecho específico y motivo. Se verificará que las unidades permitan la reversión; no se permitirá repetirla ni borrar el historial.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## ING-07

**Fuente:** PDF v2, p. 18. **Regla:** Revertir un ingreso no restaurará automáticamente costos o precios anteriores. La modificación de esos valores será una acción independiente y autorizada.

**Tarea:** E2-03 (E2). **Pantalla:** P06 Ingresos Excel/recurrentes. **Depende de:** E2-01,E2-02.

**Decisiones relacionadas:** D09, D12. **Pruebas:** A08, A09.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A08,A09; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MOV-01

**Fuente:** PDF v2, p. 19. **Regla:** Los traspasos entre almacenes serán inmediatos, con conexión y autorización. Permitirán indicar código, cantidad y estado de las unidades trasladadas; por ejemplo, mover solo unidades dañadas.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MOV-02

**Fuente:** PDF v2, p. 19. **Regla:** El movimiento conservará origen, destino, cantidad, estado, usuario y fecha. No convertirá automáticamente mercancía dañada o apartada en disponible; conservará los vínculos de las unidades apartadas con su apartado. Las piezas de clientes en reparación se controlarán en órdenes, no como mercancía de almacén.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MOV-03

**Fuente:** PDF v2, p. 19. **Regla:** Se registrará un estado especial para mercancía dañada. Las unidades dañadas no estarán disponibles para vender, apartar o entregar como mercancía de cambio. Su recuperación a disponible requerirá revisión, autorización, motivo e historial.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MOV-04

**Fuente:** PDF v2, p. 19. **Regla:** Las bajas requerirán cantidad y motivo: pérdida, robo, daño definitivo u otro, con explicación cuando sea otro. Si posteriormente aparece la mercancía, se registrará un nuevo ingreso; se podrá usar el mismo código cuando siga existiendo y corresponda a las mismas características.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MOV-05

**Fuente:** PDF v2, p. 19. **Regla:** La consulta de inventario distinguirá las cantidades por almacén y estado, permitiendo localizar el producto y consultar sus movimientos. Los movimientos no deben ocultar discrepancias ni reemplazar el historial con un nuevo saldo sin explicación.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIN-01

**Fuente:** PDF v2, p. 19. **Regla:** Cada producto podrá tener un mínimo de unidades y una opción para activar o desactivar su alerta. Se compararán únicamente las unidades disponibles en cada almacén por separado, sin sumar los tres almacenes.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIN-02

**Fuente:** PDF v2, p. 19. **Regla:** La alerta se activará cuando la disponibilidad sea igual o menor al mínimo, si está habilitada. Se mostrará en el dashboard por producto y almacén. Se resolverá cuando la disponibilidad supere el mínimo, conservando el historial.

**Tarea:** E2-02 (E2). **Pantalla:** P06/D04 Inventario por estado. **Depende de:** E1-02,E2-01.

**Decisiones relacionadas:** D13. **Pruebas:** A04, A10.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A04,A10; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-01

**Fuente:** PDF v2, p. 20. **Regla:** El dashboard será exclusivo del administrador y accesible remotamente. Incluirá gestión de clientes, saldo a favor y Correcciones de operaciones. Las entregas físicas se registrarán solo en el POS. Las correcciones remotas no enviarán tickets a imprimir al local.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-02

**Fuente:** PDF v2, p. 20. **Regla:** La referencia visual será Loyverse: barra lateral de navegación, filtros superiores, tarjetas compactas, una gráfica principal y tablas de detalle. Se evitará saturar la primera pantalla; los detalles se abrirán por sección o en un panel lateral.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-03

**Fuente:** PDF v2, p. 20. **Regla:** Las tarjetas principales incluirán ventas brutas, descuentos, ventas netas, cobros recibidos y beneficio bruto. Las cifras deben conservar una definición propia del negocio, sin copiar rótulos o fórmulas incompatibles de la referencia visual.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-04

**Fuente:** PDF v2, p. 20. **Regla:** Habrá filtros de fecha, intervalo de horas, sucursal y vendedor cuando sean aplicables. Se incluirán accesos rápidos como hoy, ayer, esta semana, semana anterior, este mes, mes anterior, últimos 7 días, últimos 30 días y rango personalizado.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-05

**Fuente:** PDF v2, p. 20. **Regla:** Se podrá elegir día completo o una franja horaria. Las fechas y horas se interpretarán en la zona del negocio, Ciudad de México, utilizando la hora original de la operación.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-06

**Fuente:** PDF v2, p. 20. **Regla:** Se podrán consultar las dos sucursales en conjunto o por separado y uno o varios vendedores. Al filtrar vendedores, solo se contabilizará la parte atribuida a los seleccionados, sin multiplicar el total de un ticket compartido.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-07

**Fuente:** PDF v2, p. 20. **Regla:** Las tarjetas permitirán explorar el indicador en una gráfica de líneas, área o barras y agrupar por hora, día, semana o mes. Se mostrará el valor del punto consultado y se podrá acceder al detalle.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-08

**Fuente:** PDF v2, p. 20. **Regla:** Se mostrarán comparaciones con un período anterior equivalente, en importe y porcentaje. Si el período de referencia es cero, no se mostrará un porcentaje infinito. El mes en curso se comparará con los mismos días transcurridos del mes previo.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-09

**Fuente:** PDF v2, p. 20. **Regla:** Los reportes se podrán exportar a Excel respetando los filtros. Se identificarán el período y el estado de actualización. El dashboard indicará la última sincronización por sucursal y no presentará datos incompletos como definitivos.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-01

**Fuente:** PDF v2, p. 21. **Regla:** Se distinguirán ventas de mercancía, cobros de dinero y movimientos de caja. Un fondo inicial, una entrada extra o un retiro no son ventas. Un anticipo y un abono no deben sumarse otra vez como ventas al liquidar.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-02

**Fuente:** PDF v2, p. 21. **Regla:** Las ventas ordinarias se reconocerán con sus precios y costos históricos. La venta neta descontará los descuentos; el beneficio bruto de mercancía se obtendrá a partir de la venta neta y su costo histórico asociado.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-03

**Fuente:** PDF v2, p. 21. **Regla:** Los apartados se reconocerán como venta y atribución comercial al liquidarse. El costo para su beneficio será el existente cuando se registró el apartado. La entrega posterior no volverá a generar venta.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-04

**Fuente:** PDF v2, p. 21. **Regla:** Los cobros de apartados se mostrarán en las fechas en que fueron recibidos. Un apartado cobrado en varias sesiones podrá aportar efectivo a varias cajas, aunque su venta se reconozca una sola vez.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-05

**Fuente:** PDF v2, p. 21. **Regla:** Las reparaciones se mostrarán separadas de la venta y beneficio de mercancía y sin atribución a vendedores. Los cobros efectivos de dinero se incluirán en cobros recibidos. Aplicar saldo a favor cubre una obligación, pero no es una nueva entrada de dinero; se identificará por separado.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CAL-06

**Fuente:** PDF v2, p. 21. **Regla:** En los cambios no se duplicará la venta original. Se conservará la atribución acordada y se distinguirá la diferencia cobrada. La salida y entrada de mercancía requiere una fórmula explícita de ajuste de costos y beneficio.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-01

**Fuente:** PDF v2, p. 22. **Regla:** El reporte comercial comenzará con las categorías o tipos de pieza más vendidos. Al seleccionar una categoría se accederá a sus productos más vendidos.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-02

**Fuente:** PDF v2, p. 22. **Regla:** Se podrá ordenar tanto por unidades como por importe de ventas netas. Las subcategorías servirán como filtros, junto con el material, período, sucursal y otros filtros aplicables.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-03

**Fuente:** PDF v2, p. 22. **Regla:** Se podrá visualizar la participación por categoría y consultar los productos en tabla. Las listas y sus filtros se podrán exportar a Excel.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-04

**Fuente:** PDF v2, p. 22. **Regla:** El reporte por vendedor mostrará el importe de ventas que tiene atribuido durante el período. Las ventas compartidas se dividirán; los apartados liquidados se asignarán a los vendedores originales y las diferencias de cambios a quienes los atiendan.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-05

**Fuente:** PDF v2, p. 22. **Regla:** La comisión se calculará aplicando un porcentaje elegido por el administrador al acumulado correspondiente. El porcentaje podrá variar por vendedor y su modificación no alterará el monto histórico atribuido.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-06

**Fuente:** PDF v2, p. 22. **Regla:** Se podrá conservar una captura del cálculo de comisiones con período, filtros, vendedor, acumulado, porcentaje, importe y fecha. Un cálculo posterior no sobrescribirá el anterior. La sincronización tardía deberá poder motivar un nuevo cálculo identificable.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RPT-07

**Fuente:** PDF v2, p. 22. **Regla:** Por el momento no se requiere administrar estados de comisión pagada o pendiente. Matanga identificará montos sin asignación a vendedores y no generará comisión de reparación.

**Tarea:** E7-01 (E7). **Pantalla:** D01/D06 Resumen y reportes. **Depende de:** E3,E4,E5,E6.

**Decisiones relacionadas:** D01, D02, D03, D06, D16. **Pruebas:** A14, A26, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A14,A26,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-26

**Fuente:** PDF v2, p. 23. **Regla:** La sección caja mostrará una tabla de sesiones y un panel lateral de detalle, como en la referencia Loyverse. Se verán folio, sucursal, apertura, cierre, efectivo esperado, contado, diferencia y estado de sincronización.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-27

**Fuente:** PDF v2, p. 23. **Regla:** El detalle incluirá responsables, fondo inicial, cobros por medio y concepto, entradas extra, gastos, retiros, efectivo contado, fondo siguiente, sobre y observaciones. Permitirá consultar los movimientos que explican el cierre y exportar a Excel.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-28

**Fuente:** PDF v2, p. 23. **Regla:** El administrador podrá marcar diferencias revisadas y añadir observaciones sin alterar el cierre. Las correcciones mostrarán sus efectos en una vista ajustada junto al original, conservando operador, autorización, motivo y fechas.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-29

**Fuente:** PDF v2, p. 23. **Regla:** Las sesiones abiertas aparecerán primero; las cerradas, de más reciente a más antigua. El administrador podrá consultar el estado recibido de una sesión abierta, con advertencia de datos pendientes cuando corresponda.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-31

**Fuente:** PDF v2, p. 23. **Regla:** La sección comprobantes ofrecerá búsqueda por folio y por cliente o teléfono cuando existan. Tendrá filtros de fecha, hora, sucursal, vendedor y tipo de operación, con lista central y detalle lateral.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-32

**Fuente:** PDF v2, p. 23. **Regla:** Se distinguirán ventas, cambios, anticipos, abonos, liquidaciones y entregas. El panel mostrará productos, cantidades, precios, descuentos, medios de pago y saldo cuando aplique, además de enlaces a operaciones relacionadas.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-33

**Fuente:** PDF v2, p. 23. **Regla:** Se podrá descargar un comprobante individual en PDF con datos originales y copia cliente o negocio cuando corresponda. Descargar o reimprimir no creará otra operación. El código del cliente exige el control especial de emisión o reimpresión autorizada; una descarga genérica no deberá eludirlo.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-34

**Fuente:** PDF v2, p. 24. **Regla:** Apartados: tabla con folio, cliente, fecha de registro, vencimiento, total, abonado, saldo y estado; detalle lateral de piezas, pagos, comprobantes y entrega. Se destacarán los pendientes desde siete días antes de vencer.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-35

**Fuente:** PDF v2, p. 24. **Regla:** Existirá el filtro “Liquidados pendientes de entrega”. Mostrará los que tengan saldo cero y aún no se entreguen, con fecha de liquidación y datos del cliente. No se confundirán con vencidos por falta de pago.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-36/37

**Fuente:** PDF v2, p. 24. **Regla:** La entrega de apartados y reparaciones se realizará solo desde el POS de cualquiera de las dos sucursales de Coyoacán. El dashboard consultará sucursal, usuario, fecha, hora y comprobantes de entrega.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-38/39

**Fuente:** PDF v2, p. 24. **Regla:** Reparaciones: filtros por recibida, en reparación, lista para entregar, entregada, cancelada y listas con plazo vencido. El detalle incluirá piezas, trabajo, presupuesto y sus modificaciones, anticipo, saldo y comprobantes. El administrador podrá actualizar los estados operativos permitidos.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-40/42

**Fuente:** PDF v2, p. 24. **Regla:** Las correcciones remotas de estado exigirán permiso y motivo, conservarán el historial, no reabrirán la cancelación si ya inició la reparación y recalcularán el plazo de recogida únicamente en el caso de corrección acordado.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-43

**Fuente:** PDF v2, p. 24. **Regla:** Las alertas permitirán abrir directamente el apartado, reparación, producto y almacén, cierre de caja o incidencia de sincronización correspondiente.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-44

**Fuente:** PDF v2, p. 24. **Regla:** Una alerta podrá marcarse revisada con observación opcional. Se guardarán administrador, fecha y hora. Revisar no equivale a resolver; el problema podrá seguir pendiente y se conservará el historial.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## DAS-45

**Fuente:** PDF v2, p. 24. **Regla:** Cuando desaparezca la causa, la alerta se marcará automáticamente resuelta. Si reaparece, se generará una nueva alerta vinculada al registro. Esto no sustituye las acciones manuales de autorización, entrega o liberación.

**Tarea:** E7-02 (E7). **Pantalla:** D02-D05/D07 Consultas y alertas. **Depende de:** E2,E3,E4,E5,E6.

**Decisiones relacionadas:** D22, D23. **Pruebas:** A27, A28.

**Conectividad:** Consulta central: indicar última sincronización y datos incompletos.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A27,A28; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## TIC-01

**Fuente:** PDF v2, p. 25. **Regla:** El programa emitirá tickets para cliente y control interno según la operación, además de las etiquetas de mercancía. La impresión de una copia o reimpresión no deberá volver a afectar caja o existencias.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## TIC-02

**Fuente:** PDF v2, p. 25. **Regla:** La impresora de tickets es Star Micronics por USB; su modelo exacto está pendiente. La impresora de etiquetas identificada es Sewoo LK-B24, también USB. Deben validarse controladores, tamaño de papel, márgenes, corte y lectura del código.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## TIC-03

**Fuente:** PDF v2, p. 25. **Regla:** Las reparaciones requieren tres comprobantes de recepción y una copia interna con firma manuscrita en la entrega. Los apartados requieren copia para cliente y negocio en sus movimientos. Los cambios necesitan ambas copias con sus vínculos e importes.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-01

**Fuente:** PDF v2, p. 26. **Regla:** Se importará el catálogo solicitado con existencia mayor que cero, conservando sus códigos. Se depurarán existencias negativas con revisión del negocio, sin convertirlas arbitrariamente en cero.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-02

**Fuente:** PDF v2, p. 26. **Regla:** Se trasladarán apartados y reparaciones pendientes, aunque su fecha sea anterior al período de ventas importado. El filtro de productos no deberá eliminar referencias necesarias para operar esas órdenes.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-03

**Fuente:** PDF v2, p. 26. **Regla:** Se podrán consultar las ventas de los tres años anteriores a la puesta en marcha. Las más antiguas se conservarán por separado. Es una ventana de carga inicial, no una orden de borrar ventas futuras al cumplir tres años.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-04

**Fuente:** PDF v2, p. 26. **Regla:** El historial importado participará en gráficas, reportes y comparaciones, identificado como procedente del sistema anterior. Si no existe hora, no se inventará medianoche. Los registros sin sucursal no se asignarán arbitrariamente a una de las actuales.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-05

**Fuente:** PDF v2, p. 26. **Regla:** Si falta costo histórico, no se sustituirá por el costo actual para inventar beneficio. El indicador se marcará incompleto o no disponible. Se documentará la cobertura de cada indicador.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## MIG-06

**Fuente:** PDF v2, p. 26. **Regla:** Importar ventas históricas no volverá a descontar inventario ni abrirá ingresos en las nuevas cajas. Existencias iniciales, órdenes activas e historial serán procesos relacionados pero separados.

**Tarea:** E8-01 (E8). **Pantalla:** Migración y validación. **Depende de:** Modelo estable E2-E6.

**Decisiones relacionadas:** D14, D15, D16. **Pruebas:** A29.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A29; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-01

**Fuente:** PDF v2, p. 27. **Regla:** Se permitirá anular ventas registradas por error. La anulación revertirá sus efectos en inventario, pagos registrados y atribución, conservará la operación original y no representará devolución de dinero al cliente.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-02/03

**Fuente:** PDF v2, p. 27. **Regla:** Habrá un único módulo Correcciones de operaciones: buscar, consultar original, elegir acción, capturar motivo y datos, comparar antes y después, autorizar y confirmar. Permitirá corregir medio de pago o reparto de un pago combinado, conservando el total.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-04

**Fuente:** PDF v2, p. 27. **Regla:** Se podrán sustituir, agregar o quitar vendedores manteniendo una asignación válida. El neto atribuible se repartirá entre los resultantes. Se actualizarán acumulados sin cambiar pagos, caja o productos. Los cálculos de comisión guardados se conservarán y se señalarán para revisión.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-05

**Fuente:** PDF v2, p. 27. **Regla:** Los productos y cantidades de una venta finalizada no se editarán. Se anulará la venta errónea y se registrará la correcta, vinculándolas. No habrá una función para trasladar automáticamente el pago; se revertirá el registro anterior y se capturará el correcto sin cobrar de nuevo al cliente.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-06

**Fuente:** PDF v2, p. 27. **Regla:** La cancelación por error requerirá conexión, derecho específico y motivo escrito obligatorio. Se emitirá ticket interno en el POS con folio, importe, sucursal, motivo, responsables, fecha y hora. Una devolución solicitada por el cliente seguirá el flujo de cambio comercial.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-07

**Fuente:** PDF v2, p. 27. **Regla:** No se podrá cancelar dos veces una venta ni cancelar por error una venta con cambios de mercancía vinculados. Se mostrará el bloqueo y las operaciones relacionadas.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-08

**Fuente:** PDF v2, p. 27. **Regla:** Cancelar ventas, corregir pagos y corregir vendedores serán tres derechos independientes dentro del módulo. Uno no concede los otros. Se distinguirá operador de autorizador.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-09

**Fuente:** PDF v2, p. 28. **Regla:** La corrección de medio o reparto de pagos abarcará ventas y pagos de apartados o reparaciones aún no liquidados. Mantendrá el total; exigirá los datos de tarjeta o transferencia cuando corresponda. En reparaciones no habilita abonos intermedios.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-10

**Fuente:** PDF v2, p. 28. **Regla:** Toda corrección tendrá registro en movimientos, operación y caja afectadas. Mostrará tipo, folio, datos previos y nuevos, motivo, operador, autorizador y fechas. No contará como otra venta o cobro. Desde el POS se imprimirá ticket interno.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-11

**Fuente:** PDF v2, p. 28. **Regla:** No habrá límite de tiempo para las correcciones permitidas. Se conservarán la fecha de operación original y la fecha de corrección. La ausencia de plazo no elimina restricciones por estado, cambios vinculados o liquidación.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-12

**Fuente:** PDF v2, p. 28. **Regla:** El administrador podrá realizar las mismas correcciones desde una sección del dashboard, con búsqueda, historial y comparación antes/después. Las reglas y derechos serán los mismos que en el POS.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-13

**Fuente:** PDF v2, p. 28. **Regla:** Los cierres originales no se sobrescribirán. Se mostrará Correcciones posteriores y una vista ajustada, conservando efectivo contado, esperado original, diferencia declarada, fondo y sobre. Los reportes del período afectado se actualizarán y señalarán las correcciones.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-14

**Fuente:** PDF v2, p. 28. **Regla:** Una corrección del dashboard quedará registrada en el propio dashboard y vinculada a la operación. No enviará tickets a imprimir ni creará una impresión pendiente en el local. Las correcciones hechas en el POS conservarán la impresión interna.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-15

**Fuente:** PDF v2, p. 29. **Regla:** Cancelar una venta registrará la entrada de unidades en la fecha y hora de la cancelación, vinculada a la salida original. No reescribirá el historial. Una venta de reemplazo generará la salida correcta sin duplicar movimientos.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-16

**Fuente:** PDF v2, p. 29. **Regla:** Solo el administrador podrá anular un pago registrado por error en un apartado o reparación aún no liquidados, con conexión y motivo escrito. Se recalculará el saldo pendiente, conservarán pagos y cierres originales y restituirá el saldo a favor usado con su vigencia original. No implica devolver dinero.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## COR-17

**Fuente:** PDF v2, p. 29. **Regla:** Un apartado o reparación liquidado quedará cerrado a correcciones económicas: no se anularán pagos ni modificarán importes, medios de pago, piezas o presupuesto. Esta regla prevalece sobre la autorización general de corregir anticipos, abonos o liquidaciones. No habrá una excepción por calcular si quedaría deuda después de entregar.

**Tarea:** E6-02 (E6). **Pantalla:** P08 Correcciones. **Depende de:** E3,E4,E5.

**Decisiones relacionadas:** D04, D05, D07. **Pruebas:** A24, A25.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A24,A25; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-01

**Fuente:** PDF v2, p. 31. **Regla:** Existirá un módulo Clientes con identificador interno, nombre, teléfono y observaciones opcionales. Reunirá apartados, reparaciones, sus pagos y estados, saldos a favor, comprobantes y ventas asociadas. Se podrá buscar la ficha existente al registrar una operación.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-02

**Fuente:** PDF v2, p. 31. **Regla:** La reducción autorizada del presupuesto de una reparación no liquidada podrá generar saldo a favor por el exceso pagado. Se conservarán importe, motivo, origen, usuario y fecha. Su uso en otra operación no será una nueva entrada de dinero.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-03

**Fuente:** PDF v2, p. 31. **Regla:** Se podrá aplicar saldo a favor en mercancía, anticipos/abonos/liquidaciones de apartados y anticipos/liquidaciones de reparaciones. Cuenta para cubrir los mínimos del 40% y 50%. Puede combinarse con otros medios sin exceder el pago debido. No habilita abonos intermedios de reparación.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-04

**Fuente:** PDF v2, p. 31. **Regla:** La consulta actualizada y aplicación exigirán conexión y verificación del disponible, evitando uso simultáneo del mismo importe en los dos locales. Sin internet se podrá vender por otros medios, pero no aplicar saldo a favor.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-05/06

**Fuente:** PDF v2, p. 31. **Regla:** Por defecto no habrá vencimiento. Solo el administrador podrá configurar vigencia por cliente. Cada saldo conservará la condición o fecha asignada al crearlo; cambiar la configuración no alterará saldos existentes.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-07

**Fuente:** PDF v2, p. 31. **Regla:** Se consumirán primero los saldos vigentes que venzan antes y al final los que no vencen. A igual vencimiento se usará el más antiguo. Puede usarse una parte conservando remanente y vigencia. Los vencidos permanecen en historial, no disponibles.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-08/09

**Fuente:** PDF v2, p. 31. **Regla:** Aplicar saldo tendrá un derecho independiente y podrá autorizarlo otra persona habilitada. Configurar vigencia será exclusivo del administrador. Ambos procesos tendrán historial.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-10/11

**Fuente:** PDF v2, p. 31. **Regla:** Se admitirán clientes diferentes con el mismo teléfono, mostrando coincidencias sin fusionarlos. Identificar cliente será opcional en ventas ordinarias y obligatorio para saldo a favor, apartados y reparaciones; estos últimos requieren nombre y teléfono.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-12/14

**Fuente:** PDF v2, p. 32. **Regla:** Cada cliente tendrá un código fijo autogenerado para validar el uso de su saldo. Será distinto de la clave del empleado autorizador. Tener el código no concede permisos de empleado; autorizar como empleado no sustituye el código del cliente.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-15/16

**Fuente:** PDF v2, p. 32. **Regla:** Se entregará el código en el ticket del cliente inicialmente. No aparecerá en cada compra, en copias internas ni en el historial. Reimprimirlo exigirá un derecho específico; se registrarán motivo, cliente, operador, autorización y fecha, sin exponer el código en ese registro.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-17

**Fuente:** PDF v2, p. 32. **Regla:** Solo el administrador podrá sustituir un código, con conexión y motivo. El anterior quedará invalidado de inmediato y el nuevo se entregará en un ticket del cliente. Se conservarán saldos, vigencias e historial sin registrar los códigos en la bitácora.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-18/19

**Fuente:** PDF v2, p. 32. **Regla:** Cinco intentos incorrectos consecutivos bloquearán el uso del código para aplicar saldo a favor. No habrá desbloqueo automático por tiempo. Solo el administrador podrá desbloquear con su clave, conexión y motivo, reiniciando el contador de intentos y conservando el código.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-18-A

**Fuente:** PDF v2, p. 32. **Regla:** El bloqueo no impide compras con otros medios y no altera saldos. Sustituir un código y desbloquear son acciones distintas; las reglas no deben confundirse ni usarse para saltarse controles.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-20/21

**Fuente:** PDF v2, p. 33. **Regla:** Anular por error una venta que consumió saldo restituirá solo ese importe, vinculado a la anulación y a sus saldos de origen, sin duplicarse. Conservará cada vencimiento original; si venció, regresará como vencido y no se podrá usar. Sin vencimiento conserva esa condición.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-22

**Fuente:** PDF v2, p. 33. **Regla:** Corregir un pago con saldo a favor exige conexión y los derechos de corregir pagos y aplicar saldo. Si consume saldo, valida código y saldo vigente; si libera saldo usado, conserva origen y vigencia. Mantiene el total del pago. No se admite en órdenes liquidadas.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-23

**Fuente:** PDF v2, p. 33. **Regla:** Un cambio de mercancía pagada con saldo a favor reconoce el valor neto de las piezas recibidas para comprar mercancía igual o mayor. No restituye además ese importe al saldo del cliente. Se puede cubrir la diferencia con otro saldo vigente, con sus controles.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-24

**Fuente:** PDF v2, p. 33. **Regla:** Solo el administrador podrá crear saldo a favor manualmente, con conexión, cliente, importe y motivo escrito obligatorio. Se asignará la vigencia configurada en ese momento. El movimiento tendrá origen manual y no se contará como venta ni entrada de dinero.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-25

**Fuente:** PDF v2, p. 33. **Regla:** Solo el administrador podrá anular un saldo manual por error, con conexión y motivo, únicamente si no se ha utilizado ni parcialmente. Se conserva el alta y su anulación, se retira el disponible y no se crea un movimiento de efectivo.

**Tarea:** E4-02 (E4). **Pantalla:** P05 Saldo a favor. **Depende de:** E4-01,E3-02.

**Decisiones relacionadas:** D06, D07. **Pruebas:** A15.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A15; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-26

**Fuente:** PDF v2, p. 34. **Regla:** Un derecho específico permitirá editar nombre, teléfono y observaciones. Se guardarán valores anteriores y nuevos, usuario, fecha y hora. Este permiso no permite modificar saldos, códigos ni vigencias. Los comprobantes emitidos conservan sus datos originales.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-27

**Fuente:** PDF v2, p. 34. **Regla:** Solo el administrador podrá unificar fichas duplicadas, con conexión y motivo. Elegirá la ficha conservada, revisará ambas y confirmará. Se reunirán operaciones y saldos sin duplicar importes ni alterar vencimientos. Se conservarán identificadores anteriores e historial.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-27-A

**Fuente:** PDF v2, p. 34. **Regla:** Compartir teléfono no unificará clientes automáticamente. Las fichas de personas distintas, aunque sean familiares, mantendrán operaciones y saldos separados.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-28

**Fuente:** PDF v2, p. 34. **Regla:** Al unificar se invalidarán los códigos anteriores y se generará uno nuevo para la ficha unificada, entregado mediante el ticket del cliente. Se guardará el evento sin exponer los códigos.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## CLI-29

**Fuente:** PDF v2, p. 34. **Regla:** Si alguna ficha estaba bloqueada, la ficha unificada conservará el bloqueo. El nuevo código no permitirá usar saldo hasta el desbloqueo explícito del administrador, con autorización y motivo.

**Tarea:** E4-01 (E4). **Pantalla:** P05/D08 Clientes y códigos. **Depende de:** E1-01,E3-01.

**Decisiones relacionadas:** D08, D18. **Pruebas:** A16, A17.

**Conectividad:** Con conexión para operaciones del módulo; consulta de saldos vigente también online.

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A16,A17; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-01

**Fuente:** PDF v2, p. 36. **Regla:** Cada POS guardará de forma persistente sus operaciones antes de confirmarlas. La pérdida de internet, cierre del navegador o reinicio no debe borrar operaciones guardadas. Sincronizará cuando se recupere internet.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-02

**Fuente:** PDF v2, p. 36. **Regla:** Las computadoras comparten módem y normalmente horario, pero alguna puede estar apagada mientras la otra vende. El respaldo no debe depender exclusivamente de que la otra sucursal esté abierta.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-03

**Fuente:** PDF v2, p. 36. **Regla:** Las operaciones pendientes requieren una segunda copia fuera del equipo de origen. El consultor definirá el destino: por ejemplo, un dispositivo dedicado en red local. Una copia de recuperación no es otra venta ni un movimiento de inventario.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-04

**Fuente:** PDF v2, p. 36. **Regla:** Si la segunda copia no está disponible, se advertirá en el POS sin bloquear las ventas. El guardado local protege frente a reinicio, pero no garantiza recuperar operaciones si se pierde el disco antes de copiarlas o sincronizarlas.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-05

**Fuente:** PDF v2, p. 36. **Regla:** El servidor central tendrá respaldos automáticos e independientes. Se alertará sobre fallas conocidas y se mostrará el último estado recibido; un servidor no puede afirmar en tiempo real el estado de una caja aislada.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## RES-06

**Fuente:** PDF v2, p. 36. **Regla:** Se documentará y probará la restauración del servidor y la sustitución de un POS. La recuperación debe reenviar lo pendiente sin duplicar lo que el servidor ya recibió.

**Tarea:** E1-03 (E1). **Pantalla:** Impresión y recuperación. **Depende de:** E1-02,equipos.

**Decisiones relacionadas:** D20, D21, D22. **Pruebas:** A05, A06, A30.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A05,A06,A30; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-05

**Fuente:** PDF v2, p. 37. **Regla:** Habrá un único inventario general de Coyoacán, sin cupos por computadora. Los dos locales venderán de ese inventario, conservando sucursal para las ventas y cajas.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-06

**Fuente:** PDF v2, p. 37. **Regla:** Sin conexión cada POS conocerá la última existencia sincronizada y descontará sus propias ventas pendientes. No conocerá todavía nuevas ventas del otro local.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-07

**Fuente:** PDF v2, p. 37. **Regla:** Si la cantidad solicitada supera las unidades disponibles conocidas, se bloqueará la venta. No habrá derecho para saltarse el bloqueo. Las apartadas o dañadas no cuentan como disponibles. La regla rige con y sin conexión.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-08

**Fuente:** PDF v2, p. 37. **Regla:** Al sincronizar se conservarán todas las ventas cobradas, sin duplicarlas o descartarlas. Si el saldo resulta negativo, se registrará la discrepancia y una alerta vinculada a productos y movimientos, para revisión del administrador.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.

## OFF-09

**Fuente:** PDF v2, p. 37. **Regla:** No habrá módulo de conteo físico ni conciliación automática por conteo. La revisión se llevará por fuera del POS y dashboard. Esto no elimina los ingresos, traspasos, bajas y cambios de estado acordados.

**Tarea:** E1-02 (E1). **Pantalla:** Estado de conexión y sincronización. **Depende de:** E0-03,E0-04,E1-01.

**Decisiones relacionadas:** D17, D19. **Pruebas:** A02, A03, A04.

**Conectividad:** Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).

**Aceptación:** Verificar esta regla íntegra dentro de los escenarios A02,A03,A04; conservar resultado esperado/obtenido y evidencia por requisito.

**Estado:** diseño para revisión; no certificado como implementado.
