# FRIDA BLANCAS MÉXICO

## Plan de desarrollo del nuevo POS

De los requerimientos a la primera puesta en operación completa

**Versión:** 1.0 propuesta · **Fecha:** 19 de septiembre de 2026

**Base funcional:** Requerimientos_POS_Frida_Blancas_Mexico_v2.pdf, versión 2.0, 18 de septiembre de 2026, 40 páginas.

> **Compromiso de alcance.** La primera sustitución del programa actual incluirá todos los módulos operativos acordados, incluidos apartados y reparaciones. Las etapas intermedias producen demostraciones y pruebas; ninguna autoriza por sí sola una sustitución parcial.

El plan organiza entregables, dependencias, decisiones pendientes y pruebas de aceptación. Conserva los acuerdos del PDF y distingue las propuestas de organización de las reglas ya confirmadas del negocio.

**Estado al emitir este plan:** planificación. No se ha implementado ni certificado una nueva versión operativa. Las pruebas A01-A30 están por ejecutar. Las decisiones D01-D24 siguen abiertas salvo los acuerdos base que cada una debe respetar.

**Nueve etapas:** definición; arquitectura; inventario; ventas y caja; clientes y saldo; apartados y reparaciones; cambios y correcciones; dashboard; migración y puesta en marcha.

**Lectura recomendada:** ruta y alcance en páginas 2-3; etapas en 4-12; decisiones en 13-15; aceptación en 16-20; cobertura de requisitos en 21-22; primeros trabajos y responsabilidades en 23.

**Límite de esta revisión.** Se analizó el PDF y se leyó el README del prototipo existente para detectar diferencias documentales. No se auditó su código, no se restauró el respaldo PV y no se ejecutaron pruebas sobre las computadoras o impresoras de los locales.

Fuente local: output/pdf/Requerimientos_POS_Frida_Blancas_Mexico_v2.pdf. Documento auxiliar consultado: README.md del proyecto POS-nuevo. Ante diferencias, este plan usa la versión 2.0 de requisitos como base solicitada por el usuario.

<!-- PAGE -->

## Ruta de desarrollo y dependencias

Cada etapa entrega una versión demostrable y evidencia. El inicio del diseño de una etapa puede adelantarse; su aceptación requiere integrar y verificar las dependencias indicadas.

| Etapa | Entregable principal | Depende de |
| --- | --- | --- |
| E0 · Definición | Flujos, modelo, prototipo visual, tareas y decisiones | PDF v2 y revisión documental |
| E1 · Arquitectura | Prueba de persistencia, sincronización, seguridad e impresión | E0 para contratos y reglas de la prueba |
| E2 · Inventario | Catálogo, códigos, ingresos, etiquetas y movimientos | E1; decisiones de catálogo y disponibilidad |
| E3 · Ventas y caja | Jornada completa, pagos y operación sin internet | E1 + E2; saldo se integra en E4 |
| E4 · Clientes y saldo | Expedientes, códigos, vigencias y movimientos de saldo | E1 + E3; integra origen por reparación en E5 |
| E5 · Órdenes | Apartados y reparaciones completos | E2 + E3 + E4 |
| E6 · Cambios y correcciones | Flujos comerciales y ajustes auditados | E2 + E3 + E4 + E5 |
| E7 · Administración | Dashboard, reportes, alertas, comisiones y exportación | Datos y reglas de E2-E6 |
| E8 · Puesta en operación | Migración verificada, capacitación y restauración probada | Aceptación integrada de E1-E7 |

**Trabajo que comienza temprano.** E0 dibuja el dashboard; E1 comprueba hardware y analiza una copia de los datos antiguos; desde E3 se calculan reportes básicos para verificar cifras; E8 prepara el mapeo de migración desde E0 y ejecuta la carga final al terminar la integración.

**Ruta que condiciona la salida:** contratos y modelo → persistencia y permisos → inventario y caja → clientes, órdenes y correcciones → reportes integrados → ensayo de migración y recuperación → autorización de salida.

**Puertas de avance propuestas:** G0, reglas de la próxima etapa claras; G1, riesgos técnicos demostrados; G2, alcance funcional integrado; G3, datos y equipos aceptados; G4, decisión de puesta en operación. La evidencia de una puerta no reemplaza la de las demás.

No se fija una fecha final ni una duración por etapa sin revisar capacidad del equipo, código reutilizable, volumen de datos y disponibilidad de equipos. Al cerrar G1 se estima el trabajo restante por tareas, con supuestos y margen explícito para fallas encontradas.

<!-- PAGE -->

## Alcance obligatorio de la primera salida

**Operación:** ventas; descuentos autorizados; efectivo, tarjeta, transferencia y saldo a favor; apertura, movimientos y cierre ciego de caja; vendedores y autorizadores; cambios; apartados; reparaciones; clientes; correcciones; tickets y etiquetas.

**Administración:** dashboard remoto exclusivo del administrador; catálogo y proveedores; tres almacenes; importación y recepción recurrente; traspasos, bajas, estados y mínimos; comprobantes; reportes y comisiones; alertas; exportaciones; permisos; migración y respaldos.

| Conectividad | Operaciones que deben respetarla |
| --- | --- |
| Admitidas sin internet | Ventas ordinarias y descuentos permitidos; apertura, cierre, entradas extra, gastos y retiros. Guardado previo, secuencia y sincronización posterior. |
| Requieren conexión | Todas las operaciones de apartados y reparaciones; cambios y correcciones; consulta vigente y uso de saldo; altas, importaciones y movimientos de inventario. |
| Control adicional | Traspasos de salida de Coyoacán requieren ambas sucursales conectadas y sincronizadas, con disponibilidad revalidada al confirmar. |
| Consulta remota | Muestra lo recibido, última sincronización y datos incompletos. Las entregas físicas se registran exclusivamente en POS. |

**Reglas que el diseño debe conservar:** un inventario de Coyoacán compartido, sin cupos por computadora; caja y ventas identificadas por sucursal; varias unidades por producto/código; existencias por almacén y estado; bloqueo por saldo conocido insuficiente; conservación de ventas offline que produzcan una discrepancia al sincronizar.

**Separaciones esenciales:** venta, cobro y movimiento de caja; operador, vendedor y autorizador; liquidación y entrega; corrección y cambio comercial; cierre original y vista ajustada; fecha de operación, recepción central y corrección. COR-17 bloquea correcciones económicas de órdenes liquidadas incluso al administrador.

**Fuera del alcance acordado:** conteo y conciliación física de inventario; precios automáticos por metal/peso; integración bancaria; abonos intermedios en reparaciones; devoluciones comerciales en dinero; comisiones pagadas/pendientes; firma digital; avisos automáticos por mensajería; entregas desde dashboard. Facturación fiscal, tienda en línea y autoservicio no se dan por incluidos. Las garantías y el tratamiento fiscal requieren definición aparte si se solicitan.

La revisión externa de existencias iniciales forma parte de preparar datos. No autoriza añadir un módulo de conteo al producto. Los límites funcionales de esta página proceden del PDF, no de las funciones generales de Loyverse.

<!-- PAGE -->

## E0 · Definición y preparación

**Objetivo:** transformar los requisitos en tareas comprobables y diseñar los contratos comunes antes de construir los módulos. **Responsables propuestos:** negocio valida reglas; desarrollo prepara especificación y alternativas; soporte aporta equipos y datos.

**Entrada y dependencias:** PDF v2; ejemplos de tickets; inventario de equipos; copia de trabajo de la información antigua cuando esté disponible. No es necesario cerrar todo D01-D24 para comenzar; sí las decisiones que afecten al siguiente entregable.

### Entregables

- E0.1 Matriz de requisitos con identificador, pantalla, regla, etapa, decisión, prueba, evidencia y estado. Las páginas 21-22 constituyen la cobertura inicial por sección.
- E0.2 Flujos completos y estados de ventas, caja, apartados, reparaciones, cambios y correcciones; incluir fallas y acciones bloqueadas.
- E0.3 Diccionario de ventas/cobros/beneficio/atribución y ejemplos numéricos aprobados. Precios y costos históricos se distinguen de los vigentes.
- E0.4 Modelo de datos: catálogo, almacenes/estados, movimientos, caja, pagos, participantes, clientes, saldos, órdenes, comprobantes, correcciones y sincronización.
- E0.5 Prototipo navegable con datos ficticios: POS de venta/caja y dashboard con filtros, tarjetas, tabla y panel lateral inspirados en Loyverse.
- E0.6 Revisión del prototipo existente: conservar, adaptar o retirar cada componente; registrar diferencias sin cambiar datos operativos. Repositorio, tareas y registro de decisiones versionados.

### Decisiones y criterios de salida

Resolver D01 y las bases de D17-D20 para E1. Clasificar los demás pendientes por etapa; registrar responsable, alternativa elegida, ejemplo y fecha. El negocio puede recorrer venta, apartado y reparación, explicar sus estados y localizar las restricciones de entrega y corrección. Cada sección funcional del PDF tiene etapa y prueba asignadas.

**Diferencia documental detectada:** el README de la base v0.1 describe existencias por local, asignaciones y módulos de órdenes pendientes. El PDF v2 confirma inventario compartido sin cupos y órdenes completas al sustituir el programa. La revisión técnica deberá comprobar qué cambios reales hacen falta; el README no demuestra por sí solo el estado del código.

**Demostración y evidencia:** prototipo, modelo, tabla de diferencias y ejemplos validados. **Puerta G0:** la siguiente etapa tiene entradas claras. **Fuentes:** GEN-01/05; ALM-01/03; DAS-01/09; sección 37; pp. 3-7, 20 y 38 del PDF.

<!-- PAGE -->

## E1 · Arquitectura y prueba técnica

**Objetivo:** demostrar que se puede guardar, imprimir, reiniciar, recuperar y sincronizar una operación sin pérdida ni duplicación. **Depende de:** E0. **Responsables:** desarrollo y soporte; negocio valida los escenarios de continuidad.

### Entregables

- E1.1 Decisión de arquitectura: servidor de aplicación, PostgreSQL central preferido, persistencia local, identidad de dispositivo, transporte autenticado y acceso remoto. El almacenamiento local y el mecanismo de impresión se eligen con evidencia.
- E1.2 Prueba con dos POS, catálogo mínimo ficticio, apertura/venta/cierre y nueva apertura. Guardar antes de confirmar; conservar identificador, fecha real, sesión, operador, vendedores, pagos y orden local.
- E1.3 Cola persistente, acuses, reintentos y recepción central atómica. Si un identificador reaparece con contenido diferente, detener el conflicto y mostrar incidencia sin duplicarlo ni sobrescribirlo silenciosamente.
- E1.4 Autenticación, matriz inicial de permisos, autorizaciones puntuales y auditoría. Contrato para permisos/precios/catálogos actualizados y límites de operación offline. La validación local y central debe ser coherente.
- E1.5 Prueba Linux/USB: ticket Star, etiqueta Sewoo LK-B24 y lector. Separar operación guardada, trabajo de impresión y confirmación central; reimprimir no repite movimientos.
- E1.6 Segunda copia fuera del POS de origen, independiente de que la otra caja esté encendida; respaldo central y primer ensayo de recuperación. Estado visible de conexión, sincronización y copia local.

### Decisiones y aceptación

Cerrar D17-D22 para seleccionar arquitectura, credenciales, persistencia, red, respaldos e impresoras; usar D01 para importes de prueba. PostgreSQL, servicio local u otras herramientas no quedan aprobados por una maqueta.

**A01-A06 y A30:** simular desconexión, pérdida de acuse, doble envío, reinicio, una sucursal apagada, respaldo local no disponible e impresora desconectada. Recuperar lo guardado y reenviarlo una sola vez; conservar secuencia de cajas y discrepancias. El POS sigue vendiendo si la segunda copia falla, con advertencia; el ensayo distingue ese riesgo de la protección contra reinicios.

**Evidencia:** protocolo ejecutado, versiones/equipos usados, comprobantes escaneados, comparación local-central y reporte de restauración. **Puerta G1:** solución elegida y riesgos pendientes visibles. Esta prueba aún usa datos ficticios. **Fuentes:** ARQ, OFF, RES, TIC; pp. 5-6, 25, 36-37.

<!-- PAGE -->

## E2 · Catálogo e inventario

**Objetivo:** disponer de mercancía identificable y movimientos trazables para alimentar ventas y órdenes. **Depende de:** E1. **Responsables:** desarrollo; negocio valida catálogo, etiquetas y movimientos; soporte prueba periféricos.

### Entregables

- E2.1 Material, tipo, dos subcategorías, proveedor obligatorio, descripciones corta/larga, costo protegido, precio manual, peso opcional y una imagen opcional. Desactivación/reactivación y claves estables.
- E2.2 Existencias por código, almacén y estado: disponibles, apartadas y dañadas. Coyoacán compartido por ambos locales; piezas de reparación pertenecen a órdenes y quedan fuera del stock para venta.
- E2.3 Generación de códigos, conservación de históricos como texto, alias de códigos anteriores y etiquetas con descripción, precio opcional y peso en clave. Varias unidades iguales comparten código.
- E2.4 Plantilla Excel para nuevos productos: un almacén, fila por producto y cantidad; validar todo, vista previa, confirmar, comprobante y etiquetas. Reporte descargable de errores y detección de duplicados/reintentos.
- E2.5 Ingreso recurrente sin Excel, búsqueda por descripciones y reutilización de código; cambios autorizados de costo/precio con historial y sin recalcular operaciones antiguas.
- E2.6 Traspasos inmediatos, estados, bajas, recuperación de dañadas, mínimos y reversión completa de ingresos. Conservar vínculos de reservas. La segunda venta offline no debe ser descartada por una discrepancia central.

### Decisiones y aceptación

Cerrar D09-D13; D21 para lectura/etiqueta. La reversión de ingresos con movimientos posteriores y el alcance de los bloqueos por sucursales desconectadas deben quedar explícitos antes de implementar esas acciones.

**A04 y A07-A10:** cinco unidades iguales producen un producto, cinco unidades y cinco etiquetas; Excel con un error ingresa cero filas; repetir confirmación no vuelve a ingresar; peso ausente no se inventa. Un cambio de costo no altera el beneficio histórico. Dañadas y apartadas no se ofrecen como disponibles. Mínimo 3 mantiene alerta con saldo 3 y se resuelve al subir a 4.

Traspasar conserva cantidad, estado y reserva; la salida de Coyoacán exige ambas sucursales sincronizadas y revalidación. Reversión se aplica una vez, por todo el ingreso, y no restaura automáticamente precio/costo. La integración con reservas se revalida en E5.

**Evidencia:** archivos válidos/erróneos, comprobantes, etiquetas leídas y libro de movimientos esperado/obtenido. **Fuentes:** ALM, INV, IMP, ING, MOV, MIN, OFF-05/09; pp. 4 y 15-19, 37.

<!-- PAGE -->

## E3 · Ventas, pagos y caja

**Objetivo:** completar una jornada de mostrador, incluida continuidad sin internet. **Depende de:** E1 + E2. Los contratos de pagos admiten saldo a favor; su uso se activa y acepta al integrar E4.

### Entregables

- E3.1 Venta con búsqueda/lector, cantidades, precios históricos, descuento global autorizado y uno o varios vendedores con reparto igual del neto. Separar atribución comercial de operador/autorizador.
- E3.2 Pago combinado: efectivo, máximo una tarjeta y una transferencia, más saldo al integrar E4. Guardar tipo crédito/débito, banco, últimos cuatro dígitos y referencia de transferencia. Cobro bancario y verificación siguen siendo externos.
- E3.3 Efectivo recibido, aplicado y cambio separados. Totales monetarios y redondeos consistentes; el saldo a favor no genera dinero nuevo.
- E3.4 Una caja compartida y una sesión abierta por local; aperturas múltiples por fecha, fondo sugerido y diferencia explícita frente al cierre previo.
- E3.5 Entradas extra, gastos y retiros con motivo/derechos; cierre ciego, esperado, contado, diferencia, fondo siguiente y sobre. Cierre original conservado para futuras correcciones.
- E3.6 Ticket, reimpresión, pagos y movimientos persistentes; interfaz de conexión/pendientes; sincronización de aperturas, movimientos, cierres y nuevas aperturas en secuencia.

### Decisiones y aceptación

Cerrar D01, D17-D19 y límites de descuentos. Prever desde el modelo la imputación histórica de correcciones D02-D04; su implementación completa corresponde a E6.

**A02-A06 y A11-A14:** venta de $1,000 con tarjeta $600 y efectivo recibido $500 aplica efectivo $400 y entrega cambio $100. No se obtiene cambio de tarjeta/transferencia. Venta neta $1,000 con dos vendedores atribuye $500 a cada uno, sin duplicar el total.

En una sesión ficticia, fondo $500 + efectivo neto $400 + entrada $100 - gasto $50 - retiro $200 produce esperado $750. Conteo $730 declara -$20; fondo $300 + sobre $430 distribuyen $730. Tarjeta y saldo no aumentan ese esperado. El cajero captura antes de ver la comparación; un descuadre no impide cerrar.

**Demostración:** jornada offline con descuento autorizado, cierre y nueva apertura; reiniciar y sincronizar. **Evidencia:** tickets, sesiones y totales local-central. Pruebas de saldo y órdenes completan E3 en E4/E5. **Fuentes:** ACC, VEN, VTA, PAG, CAJ, OFF; pp. 6-9.

<!-- PAGE -->

## E4 · Clientes y saldo a favor

**Objetivo:** controlar identidad, vigencia y uso del saldo sin duplicar dinero ni permitir consumos concurrentes. **Depende de:** E1 + E3; prepara la integración de apartados y reparaciones en E5.

### Entregables

- E4.1 Ficha con nombre, teléfono, observaciones, historial de operaciones/comprobantes y búsqueda de coincidencias. Cliente opcional en venta ordinaria y obligatorio en saldo, apartados y reparaciones. Teléfono compartido no fusiona fichas.
- E4.2 Movimientos de saldo por origen, vigencia, aplicación, restitución y anulación. Por defecto sin vencimiento; configuración por cliente solo afecta saldos futuros. Consumir primero por vencimiento y luego antigüedad; sin vencimiento al final.
- E4.3 Aplicación online, cliente, código y derecho independiente. Validación atómica entre sucursales. Integra pago combinado sin exceder el importe debido.
- E4.4 Código fijo generado, emisión inicial y reimpresión con permiso/motivo; sustitución y desbloqueo exclusivos del administrador. Quinto fallo consecutivo bloquea; no hay desbloqueo por tiempo.
- E4.5 Alta manual de saldo y anulación solo por administrador; anulación únicamente si no se ha usado ni parcialmente. Ninguna de esas acciones crea efectivo ni venta.
- E4.6 Edición auditada y unificación de duplicados: reunir sin duplicar importes ni alterar vigencias, invalidar códigos previos, emitir uno nuevo y conservar bloqueos.

### Decisiones y aceptación

Cerrar D06-D08 y D18. El diseño debe resolver cómo entregar/reimprimir el código sin exponerlo en historial, registros técnicos, copias internas o descarga genérica de tickets. Mantener diferenciadas clave de empleado y código del cliente.

**A15-A17:** dos intentos simultáneos de consumir un mismo saldo no pueden gastar más del disponible; el permiso de empleado no reemplaza el código. Restituir un importe conserva su vigencia; si venció, permanece no disponible. Cambiar configuración no altera saldos existentes.

Unificar clientes conserva cada saldo y vencimiento, no duplica operaciones y conserva el bloqueo si cualquiera lo tenía. Reimprimir exige permiso; sustituir código no desbloquea. El bloqueo no impide compras con otros medios. La creación por reducción de presupuesto se acepta en E5; restituciones y correcciones se completan en E6.

**Evidencia:** libro de saldo antes/después, prueba concurrente, accesos denegados, tickets y trazas sin códigos expuestos. **Fuentes:** CLI-01/29, CLI-18-A, CLI-27-A y matriz de derechos; pp. 31-35.

<!-- PAGE -->

## E5 · Apartados y reparaciones

**Objetivo:** completar ambos ciclos, incluidos cobro, entrega y excepciones. **Depende de:** E2 + E3 + E4. **Responsables:** desarrollo; negocio valida reglas y comprobantes; empleados designados ensayan recepción/entrega.

### Entregables

- E5.1 Apartado online con cliente, varias piezas como conjunto, reserva y precio/costo del alta; anticipo mínimo 40%, sin descuento; abonos positivos hasta saldo, en cualquiera de las sucursales.
- E5.2 Liquidación y entrega independientes; reconocimiento de venta y vendedores originales al liquidar; entrega completa exclusivamente en POS, en cualquiera de los locales. COR-17 bloquea cambios económicos desde liquidación.
- E5.3 Vencimiento a final del día natural 45, plazo conservado por orden, aviso desde siete días antes, liberación autorizada y liquidación excepcional antes de liberar. Cancelación temprana hasta final del día 7 se integra con E6.
- E5.4 Reparación online de piezas del cliente, presupuesto y anticipo mínimo 50%; únicamente anticipo y liquidación, sin descuento ni atribución comercial; clasificación Matanga. Reducción de presupuesto pendiente puede generar saldo a favor.
- E5.5 Estados recibida, en reparación, lista, entregada y cancelada; historial, ajustes autorizados y plazo de recogida de 45 días desde lista. Dashboard solo realiza transiciones permitidas; entrega en POS con liquidación completa.
- E5.6 Comprobantes: dos copias por movimiento de apartado; tres al recibir reparación; dos al entregar, con firma manuscrita en la copia del negocio. Reimpresión sin nuevo cobro.

### Decisiones y aceptación

Cerrar D02, D05-D08 y D22 para formularios/evidencia. E6 resuelve conversiones comerciales y correcciones; E7 integra reconocimiento y filtros. La etapa no se considera aceptada como conjunto hasta probar esas integraciones.

**A18-A22:** apartado $1,000: anticipo $400, abono $200, liquidación $400; cada cobro afecta su caja y la venta completa se reconoce una vez al liquidar. Entregar no vuelve a sumar venta ni atribución. No sustituir piezas ni entregar parcialmente un conjunto.

Reparación $1,000 requiere $500; aumentar presupuesto no exige otro anticipo. Una disminución debajo de lo pagado genera el exceso como saldo conforme a D05. Haber pasado a en reparación bloquea cancelación aunque se corrija a recibida. Corregir lista a en reparación anula el plazo previo; volver a lista inicia uno completo. Orden liquidada permite terminar trabajo/entrega, conservando bloqueo económico.

**Evidencia:** estados, pagos, reservas, tickets y fechas límite. **Fuentes:** APA, REP, COR-17, CLI-02/03; pp. 11-14, 29 y 31.

<!-- PAGE -->

## E6 · Cambios y correcciones auditadas

**Objetivo:** aplicar las políticas comerciales y corregir errores conservando originales y efectos históricos. **Depende de:** E2-E5. **Responsables:** desarrollo; negocio valida ejemplos económicos y bloqueos.

### Entregables

- E6.1 Cambio online autorizado, parcial/completo, en cualquiera de las sucursales; verificar origen, condición y ausencia de cambio previo de esas unidades. Reconocer valor neto pagado y exigir mercancía igual o mayor después de descuento autorizado.
- E6.2 Plazo hasta final del día 15; nuevo plazo solo para piezas entregadas en cambio. Conservar atribución original y asignar la diferencia a quienes atienden. Comprobantes enlazados e inventario compartido.
- E6.3 Cancelación temprana de apartado y cancelación admisible de reparación: convertir lo pagado en mercancía igual/mayor; liberar/devolver piezas y registrar diferencia. Sin crear automáticamente un saldo guardado.
- E6.4 Módulo único: buscar original, elegir acción, motivo, comparar antes/después, autorizar y confirmar. Derechos independientes para anular venta, corregir pagos y vendedores. No editar partidas de venta finalizada; anular y reemplazar con vínculo.
- E6.5 Original y ajuste de caja separados; fechas original/corrección/inventario conservadas. Corrección desde POS imprime ticket interno; desde dashboard no crea impresión remota ni pendiente.
- E6.6 Corrección de pagos en órdenes no liquidadas y anulación de pago solo por administrador; restitución de saldo con origen/vigencia; revisión de cálculos de comisión guardados afectados.

### Decisiones y aceptación

Cerrar D01-D08 para redondeos, costos, imputación por sucursal, reemplazos, anticipos y saldo. Evitar implementar una compensación económica sin ejemplo aprobado.

**A19, A22-A25:** pieza devuelta con valor neto $800 y nueva $1,000 genera cobro adicional $200; $800 conservan atribución original y $200 van a quienes atienden. Apartado $1,000 con $400 pagados cancelado en plazo reconoce $400.

Corregir en octubre una venta de septiembre de efectivo a tarjeta ajusta su sesión original, conserva conteo/fondo/sobre y no mueve efectivo físico de octubre. La anulación revierte inventario en la fecha real de cancelación. Se bloquean segunda anulación, anulación de venta con cambios vinculados y toda corrección económica de orden liquidada. Un cambio de pieza pagada con saldo no restituye además ese saldo.

**Evidencia:** antes/después, movimientos, períodos, bloqueos y comprobantes relacionados. **Fuentes:** CAM, APA-14/16, REP-14/15, COR, CLI-20/25; pp. 10, 12, 14, 27-30, 33.

<!-- PAGE -->

## E7 · Dashboard y administración

**Objetivo:** explicar la operación con cifras verificables y acciones remotas autorizadas. **Depende de:** E2-E6 integradas; diseño visual iniciado en E0. **Responsables:** desarrollo; administrador valida indicadores, navegación y exportaciones.

### Entregables

- E7.1 Dashboard privado inspirado en Loyverse: navegación lateral, filtros superiores, tarjetas compactas, gráfica, tabla y detalle lateral. Entregas físicas siguen en POS; correcciones remotas no imprimen en locales.
- E7.2 Ventas brutas, descuentos, netas, cobros y beneficio bruto, con diccionario y ejemplos. Reparaciones separadas de venta/beneficio de mercancía; uso de saldo separado del dinero recibido.
- E7.3 Fechas y franja horaria en Ciudad de México; accesos rápidos, sucursal y uno/varios vendedores; agrupación hora/día/semana/mes y comparaciones equivalentes. Base cero no produce porcentaje infinito; mes en curso compara días transcurridos.
- E7.4 Categorías hacia productos, unidades/neto, material/subcategorías y vendedores. Comisión porcentual sobre atribuido; capturas de cálculos conservadas con filtros, porcentaje y fecha. Cambios posteriores señalan necesidad de revisión.
- E7.5 Caja: abiertas primero, cerradas recientes después; detalle de pagos/movimientos, faltantes revisados, original y ajustes. Comprobantes buscables, vínculos y PDF individual con controles del código del cliente.
- E7.6 Apartados y reparaciones con estados/plazos; filtro liquidado pendiente de entrega; inventario por almacén/estado; clientes, saldo y correcciones. Alertas con origen navegable, revisión distinta de resolución y reapertura como nuevo evento vinculado.
- E7.7 Exportación Excel respeta filtros, período y estado de actualización. Última sincronización por sucursal visible; indicadores incompletos identificados.

### Decisiones y aceptación

Cerrar D01-D04 y D06 para fórmulas, costos, sucursal y saldo; D14-D16 para calidad histórica; D23 para objetivos medibles de respuesta y carga. Cualquier indicador adicional necesita definición explícita.

**A14 y A26-A28:** comparar tarjetas, gráfica, tabla y exportación con el mismo conjunto de operaciones; ventas compartidas no se duplican; anticipos y entregas no duplican ventas; costos históricos no cambian al editar catálogo. La referencia Loyverse guía la navegación, no impone fórmulas.

**Evidencia:** ejemplos firmados por negocio, resultados esperados/obtenidos, exportaciones y recorrido del administrador. **Puerta G2:** todos los módulos integrados y pruebas funcionales aprobadas. **Fuentes:** DAS, CAL, RPT, MIN; pp. 19-24 y 31-35.

<!-- PAGE -->

## E8 · Migración y puesta en operación

**Objetivo:** sustituir el programa actual con datos conciliados, equipos probados y recuperación preparada. **Depende de:** E1-E7 aceptadas. Análisis/mapeo de datos comienza en E0; el ensayo final usa el modelo definitivo.

### Entregables

- E8.1 Mapeo reproducible de códigos, catálogo, clientes, vendedores, estados, saldos, pagos y referencias. Separar existencias iniciales, órdenes activas e histórico; conservar referencia al origen y excepciones.
- E8.2 Carga de catálogo con existencia positiva y revisión de negativos; preservar productos/documentos necesarios para órdenes o vínculos históricos aunque no entren en ese filtro.
- E8.3 Apartados y reparaciones pendientes sin límite de antigüedad; ventas de los tres años previos a la fecha de salida. Histórico más antiguo preservado aparte; no borrar futuros registros al cumplir tres años.
- E8.4 Tratamiento explícito de hora, sucursal y costo histórico desconocidos. Nunca inventar medianoche, local o beneficio con costo vigente. Cobertura de métricas visible.
- E8.5 Ensayos de importación, comparación de conteos/saldos/totales y restauración; capacitación por rol; manual de operación, incidencias, instalación y mantenimiento.
- E8.6 Plan de corte con responsables, respaldo final, suspensión de capturas en el sistema anterior, carga final, verificación en ambos locales y autorización documentada. Definir fuente única de registro durante el cambio.
- E8.7 Plan de retorno: preservar todas las operaciones nuevas, detener nuevas capturas cuando corresponda y reconciliarlas antes de reanudar el anterior. Restaurar un respaldo sin tratar esas operaciones no constituye un retorno completo.

### Decisiones y criterios de salida

Cerrar D14-D16 y D20-D24. **A01-A30:** ejecutar suite integrada, ensayo de jornada, dispositivos reales, volúmenes acordados, importación repetida y recuperación. La carga histórica no modifica stock ni caja actual. Toda diferencia en saldos, cantidades o referencias debe quedar explicada y resuelta/aceptada expresamente por el negocio antes del corte.

**G3:** datos, periféricos, formación y restauración verificados. **G4:** todos los módulos obligatorios disponibles, cero fallas abiertas que violen una regla confirmada o comprometan datos/dinero/permisos; ningún pendiente de decisión que bloquee una función de salida. Detalles cosméticos sin efecto funcional pueden registrarse para mejora por acuerdo explícito.

**Evidencia:** acta de conciliación, checklist de salida, pruebas con versión exacta, responsables y procedimiento de contingencia. La estabilización posterior atiende incidencias y mantenimiento; no recibe módulos obligatorios pospuestos. **Fuentes:** GEN-01, MIG, RES, TIC y secciones 37-39; pp. 3, 25-26, 36, 38-40.

<!-- PAGE -->

## Decisiones D01-D08 · Reglas económicas

Todas permanecen **por cerrar** en este plan. Cada resolución deberá indicar responsable, opción elegida, ejemplos, fecha, requisitos afectados y pruebas actualizadas. Resolver detalles no permite contradecir los acuerdos base citados.

**D01 · Importes, descuentos y centavos.** Definir captura del descuento, límites, precisión y reparto del descuento global y centavos entre piezas/vendedores; validar datos de tarjeta y transferencia. Entregar ejemplos de pagos y cambios parciales. Decide negocio con desarrollo. Antes de E3/E6/E7; ejemplo mínimo en E1. VTA, PAG, CAM-05, VEN; A11/A14/A23/A26.

**D02 · Reconocimiento por sucursal.** Precisar a qué sucursal se atribuye la venta al liquidar un apartado atendido en otro local. Los cobros conservan la sucursal y caja donde se recibieron; vendedores originales conservan atribución. Decide negocio. Antes de E5/E7. CAL-03/04 y pendientes p. 21; A18/A26.

**D03 · Beneficio y cantidades en cambios.** Definir ajustes de costo/beneficio en cambios parciales, repetidos y conversiones de anticipos a mercancía; distribución al filtrar vendedores. Usar costos históricos y evitar duplicación del valor original. Decide negocio con desarrollo. Antes de E6/E7. CAL-06, CAM, APA-16, REP-15; A19/A22/A23/A26.

**D04 · Venta de reemplazo con importe distinto.** Resolver diferencia entre registro erróneo, pago realmente realizado y total correcto; distinguir ajuste documental de movimiento físico de dinero, con fechas/caja afectadas. No asumir cobro nuevo o devolución. Decide negocio. Antes de E6. COR-05/15, p. 30; A24/A25.

**D05 · Anticipos y presupuesto pendiente.** Precisar qué pasa si anular un anticipo deja menos de 40%/50%; cómo marcar liquidada una reparación cubierta por reducción de presupuesto y registrar acuerdo del cliente. Mantener COR-17. Decide negocio. Antes de E5/E6. REP-04, COR-16/17, p. 38; A20/A25.

**D06 · Tratamiento comercial del saldo.** Definir presentación de mercancía pagada con saldo manual, saldo originado en reparación y anticipos cancelados que usaron saldo. Conservar origen y evitar contar dinero dos veces. Decide negocio. Antes de E4-E7 en las partes afectadas. CLI-02/03/20/24, p. 33; A15/A19/A22/A26.

**D07 · Vigencia del saldo.** Fijar unidad de configuración y hora exacta de vencimiento en zona del negocio. La configuración nueva solo afecta saldos futuros; restituciones mantienen vigencia original. Decide negocio. Antes de E4/E6. CLI-05/09/20; A15.

**D08 · Unificación y verificación de cliente.** Elegir configuración para saldos futuros al unir fichas distintas y evidencia requerida para reimprimir código. Conservar vigencias existentes, separación de personas con teléfono común y bloqueo heredado. Decide negocio con desarrollo. Antes de E4. CLI-15/16/26/29; A16/A17.

<!-- PAGE -->

## Decisiones D09-D16 · Catálogo y datos

**D09 · Diccionario y duplicados de producto.** Publicar columnas Excel, longitudes y normalización para detectar duplicados; verificar material, tipo, subcategorías, descripciones y peso. Resolver interpretación de contenido repetido frente a un ingreso nuevo legítimo. Peso opcional, tres decimales y máximo 999 g; costo/proveedor obligatorios. Negocio + desarrollo; antes de E2. INV-01/09, IMP; A07/A08.

**D10 · Identificación y etiquetas.** Cerrar simbología y validar esquema numérico de 15 posiciones, alcance/agotamiento del consecutivo, colisiones históricas, cambios de material/tipo/peso, alias y formato de peso en clave. Los códigos previos no se reutilizan para otro producto. Negocio + desarrollo + soporte; antes de E2. INV-20/25; A07.

**D11 · Imagen del producto.** Precisar carga PNG o enlace, validación, descarga/almacenamiento, límites y manejo de enlaces fallidos. Mantener una imagen opcional y decidir su disponibilidad local sin afectar venta si falta. Desarrollo propone y negocio valida experiencia; antes de E2. INV-07; A07.

**D12 · Reversión y desactivación.** Definir seguimiento por ingreso/lote y condiciones de reversión después de venta, reserva, baja o traspaso; precisar eliminación/desactivación sin borrar historial ni reutilizar códigos. Reversión completa no restaura precios/costos. Negocio + desarrollo; antes de E2. ING-06/07; A09.

**D13 · Movimientos con información desactualizada.** Definir cómo se demuestra que ambos POS están sincronizados para traspasar desde Coyoacán y si aplica también a bajas/ajustes. Mantener revalidación al confirmar y ningún cupo por computadora. Negocio + desarrollo; antes de E2/E5. MOV y OFF; A04/A10.

**D14 · Correspondencias de migración.** Inventariar tablas y calidad real de PV; mapear catálogo, órdenes, pagos, clientes, vendedores, saldos existentes si los hay y referencias antiguas. Conservar identidades y vínculos necesarios fuera del filtro de catálogo/histórico. Negocio valida; desarrollo implementa sobre copia. Preparar desde E0; cerrar antes de E8. MIG; A29.

**D15 · Corte del histórico e iniciales.** Fijar fecha de puesta en marcha y límites exactos de los tres años, archivo del resto y respaldo/fuente de corte. Revisar negativos y stock inicial externamente; pendientes se trasladan aunque sean anteriores. Negocio + desarrollo; antes del ensayo final E8. MIG-01/03/06; A29.

**D16 · Calidad histórica y conciliación.** Definir presentación/filtros de registros sin hora, sucursal o costo; cobertura de indicadores, conteos, saldos, referencias y excepciones que se compararán. No completar con supuestos silenciosos. Negocio acepta datos; desarrollo documenta cobertura. Antes de E7/E8. MIG-04/06 y CAL; A28/A29.

El dato que no exista en la fuente se conserva como desconocido o se corrige con evidencia del negocio. No se inventan costos, fechas precisas o asignaciones para completar una pantalla.

<!-- PAGE -->

## Decisiones D17-D24 · Operación técnica

**D17 · Arquitectura y equipos.** Elegir hospedaje, aplicación central, PostgreSQL, persistencia local, protocolos, impresión y despliegue. Inventariar sistemas operativos, terminales y volúmenes. El navegador accede a la aplicación, no directamente a la base. Desarrollo propone; negocio valida costo/soporte. Cerrar en E1. GEN/ARQ; A02/A05/A30.

**D18 · Identidades y credenciales.** Cerrar matriz por usuario, límites, autorización puntual, sesiones, recuperación/revocación y vigencia offline. Diseñar código de cliente: longitud, generación, protección, validación global, reimpresión y contador de fallos. Negocio asigna derechos; desarrollo diseña controles. E1 para empleados; E4 para clientes. ACC/CLI; A01/A16.

**D19 · Protocolo offline y concurrencia.** Definir identificadores, secuencias, acuses, conflictos, reloj y versiones de permisos/precios. Precisar política de terminales y exclusión de sesiones para garantizar una caja abierta por local, incluso tras recuperación. Desarrollo; validar con negocio. Antes de E3. OFF/CAJ/ARQ; A02-A05/A12.

**D20 · Respaldo y recuperación.** Elegir destino local independiente, red probada, frecuencia, retención, protección y copia central fuera del servidor. Acordar pérdida máxima tolerable y tiempo de recuperación; escenario sin segunda copia no bloquea ventas. Desarrollo + soporte; negocio acepta objetivos. E1 y validación final E8. RES; A06/A30.

**D21 · Periféricos reales.** Identificar modelo Star, controlador Linux, Sewoo LK-B24, lector, papel, etiqueta, márgenes y corte. Probar USB y lectura de códigos; definir recuperación de impresión fallida. Soporte + desarrollo con muestra validada por negocio. E1/E2. TIC/INV-25; A05/A07.

**D22 · Formatos y evidencia.** Aprobar campos y copias por movimiento; recepción de reparación, firma manuscrita, aceptación de cambio de presupuesto y protección del código en reimpresión/PDF. Negocio decide formato/evidencia; desarrollo implementa. E1 como muestra; definitivo E5-E7. TIC/REP/CLI/DAS-33; A05/A16/A20/A27.

**D23 · Objetivos de servicio.** Acordar número de terminales simultáneas, volumen de catálogo/histórico, duración de desconexión a ensayar y tiempos objetivo para cobrar, buscar, reportar y sincronizar. Son criterios técnicos por definir, no capacidades ya garantizadas. Negocio + desarrollo; antes de aceptar E7/E8. GEN/ARQ/RES; A02/A28/A30.

**D24 · Corte, retorno y soporte.** Nombrar responsables, ventana de cambio, disponibilidad de equipos, congelamiento/carga final, criterio de abortar y tratamiento de ventas nuevas al volver atrás. Definir formación, avisos de incidentes y mantenimiento. Negocio + desarrollo + soporte; antes de E8. MIG/RES/GEN-01; A29/A30.

<!-- PAGE -->

## Aceptación A01-A06 · Base técnica

Cada prueba requiere datos/estado inicial, acciones, resultado esperado y obtenido, versión, fecha y evidencia. Estos son escenarios de aceptación propuestos a partir del PDF; todavía no se han ejecutado. Se amplían con casos límite al especificar cada tarea.

**A01 · Identidad y permisos.** Preparar administrador y empleados con derechos distintos. Intentar venta, descuento, costo, retiro, corrección y acceso al dashboard; repetir por interfaz y acceso directo a la aplicación. Denegar sin derecho; autorizar puntualmente con identidad de operador/autorizador; conservar vendedores. Probar límites locales y cambios remotos según D18. Evidencia: matriz de intentos y auditoría. E1/E3-E7; ACC, GEN-03.

**A02 · Persistencia y secuencia offline.** Con sesión preparada, cortar internet, abrir/vender/descontar/registrar movimientos/cerrar/abrir otra sesión y reiniciar navegador/equipo. Recuperar operaciones guardadas y sincronizar con fecha, sucursal, pagos y sesión originales, en secuencia. Ensayar corte durante guardado; nunca confirmar algo que no quedó persistido. Evidencia: comparación local-central. E1/E3; OFF-01/03, CAJ-07.

**A03 · Reintentos y acuses.** Reenviar la misma venta y movimientos varias veces; perder respuesta después de guardado central y reiniciar antes de persistir el acuse. Una sola venta, pago y movimiento efectivo. Identificador repetido con contenido diferente produce conflicto visible. Restaurar copia y reenviar respeta lo ya recibido. E1/E3/E8; OFF-02, RES-06.

**A04 · Stock compartido.** Dos POS conocen una unidad: desconectar ambos y registrar una venta en cada uno. Al sincronizar conservar ambas, saldo -1 y alerta vinculada; intentos posteriores con conocido cero/negativo se bloquean sin excepción. También bloquear cantidad mayor al conocido y excluir apartadas/dañadas. Probar competencia online según contrato acordado. E1-E3; OFF-05/09.

**A05 · Ticket e impresión independiente.** Ejecutar venta con Star USB, etiqueta con Sewoo y lectura real bajo Linux. Fallar impresión después de guardar; reimprimir sin nuevo cobro/stock. Verificar copias por operación, márgenes/corte y ausencia de impresión remota por corrección de dashboard. Evidencia: muestras físicas y registros. E1/E2/E5-E7; TIC, COR-14.

**A06 · Segunda copia y sucursal apagada.** Mantener otra caja apagada y verificar copia fuera del equipo de origen. Quitar destino de respaldo: advertir sin bloquear ventas. Reconectar y comprobar recuperación conforme a D20, sin duplicaciones. Separar pérdida de internet de caída de red local; el servidor muestra solo último estado conocido. E1/E8; RES-02/05.

<!-- PAGE -->

## Aceptación A07-A12 · Inventario y caja

**A07 · Catálogo, códigos y etiquetas.** Registrar productos iguales/distintos y catálogos inactivos. Validar proveedor/costo/descripciones, peso opcional hasta 999 g con tres decimales e imagen opcional. Conservar ceros históricos; leer código nuevo y anterior con aviso/datos vigentes. Cinco unidades iguales usan un código y cinco etiquetas. Precio opcional, peso en clave; imprimir no cambia stock. E2; INV, D09-D11/D21.

**A08 · Importación íntegra y única.** Cargar archivo de un almacén con un error, duplicado interno o coincidencia existente: rechazar toda la carga y emitir fila/campo/motivo. Corregir, previsualizar y confirmar; reintentar y cargar mismo contenido según D09 sin duplicar. Cantidad cinco en una fila crea cinco unidades. Costos solo a autorizados. E2; IMP-01/08.

**A09 · Ingreso y reversión.** Buscar producto con saldo cero/positivo, reactivar si corresponde y recibir cantidad. Cambiar costo/precio con permiso: afecta catálogo y preserva histórico. Revertir ingreso completo una vez según D12; rechazar si movimientos posteriores lo impiden. Conservar historial y no restaurar automáticamente costo/precio. E2; ING-01/07.

**A10 · Estados, traspasos y mínimos.** Trasladar disponibles/dañadas/apartadas conservando estado y vínculo; validar cantidades/origen/destino. Salida de Coyoacán exige ambos POS sincronizados. Recuperar dañadas con motivo; dar baja y registrar nuevo ingreso si reaparecen. Mínimo 3: saldo 3 alerta, saldo 4 resuelve, por almacén disponible. Sin módulo de conteo físico. E2/E5/E7; MOV, MIN.

**A11 · Cobro combinado y descuentos.** Con caja abierta, venta $1,000: tarjeta $600, efectivo recibido $500 → efectivo aplicado $400 y cambio $100. Verificar descuento global y redondeos D01; máximo una tarjeta/transferencia y metadatos. Rechazar cambio financiado con tarjeta o pago que no cubra total. Saldo integrado requiere cliente, código, permiso y conexión. E3/E4; VTA, PAG.

**A12 · Aperturas y movimientos.** Intentar segunda sesión simultánea en el mismo local, incluyendo escenario D19: bloquear; permitir sesiones independientes entre locales. Fondo sugerido puede cambiar conservando diferencia. Entradas/gastos/retiros exigen derecho, motivo, usuario y sesión. Secuencia cierre/nueva apertura sigue válida offline y al sincronizar. E3; CAJ-01/02/06/07.

<!-- PAGE -->

## Aceptación A13-A18 · Clientes y apartados

**A13 · Cierre ciego.** Fondo $500 + cobro neto $400 + entrada $100 - gasto $50 - retiro $200 = esperado $750. Capturar conteo $730 antes de revelar comparación; diferencia -$20. Fondo siguiente $300 + sobre $430 = $730. Cerrar con descuadre sin compensarlo automáticamente en próxima apertura. Tarjeta, transferencia y saldo no aumentan efectivo esperado. E3; CAJ-03/05.

**A14 · Vendedores y comisiones.** Venta neta $1,000 entre dos vendedores → $500 cada uno. Filtrar ambos da $1,000. Cambiar porcentaje de comisión no cambia atribución; conservar cada cálculo guardado y marcar revisión por corrección/sincronización tardía. Apartados mantienen vendedores iniciales y reparaciones Matanga sin comisión. E3/E5/E7; VEN, RPT-04/07.

**A15 · Saldo, vigencia y concurrencia.** Crear saldos con vencimientos distintos y sin vencimiento; consumir por orden pactado y remanentes. Dos locales no exceden disponible. Restituir conserva origen/vigencia, incluso vencido. Solo admin crea saldo manual y anula el no usado; aplicación/alta/anulación no generan dinero. Configuración futura no altera saldos previos. E4/E6; CLI-01/11/20/25.

**A16 · Código de cliente.** Probar emisión, reimpresión autorizada con motivo, quinto fallo global y bloqueo sin desbloqueo temporal. Solo admin sustituye o desbloquea; sustituir no desbloquea por sí solo. Código viejo deja de servir; compra con otro medio sigue disponible. Código no aparece en copias internas, historial, logs o descarga genérica; el derecho de empleado no lo sustituye. E4/E7; CLI-12/19.

**A17 · Edición y unificación.** Editar ficha con permiso conservando antes/después y comprobantes originales. Dos personas con mismo teléfono siguen separadas. Admin unifica duplicado con motivo: mismo total de saldo, vencimientos intactos, vínculos únicos, códigos viejos invalidados, nuevo emitido y bloqueo heredado. Aplicar D08 para configuración futura. E4; CLI-26/29.

**A18 · Ciclo de apartado.** Total $1,000: anticipo $400, abono $200, liquidación $400, en distintas sesiones/locales. Registrar cobros donde ocurren; reservar conjunto, mantener precio/costo inicial y vendedores; reconocer venta $1,000 una vez al liquidar. Entregar completo solo desde POS con conexión; no sustituir piezas ni cobrar de más. Emitir dos copias por movimiento. E5/E7; APA-01/09, D02.

<!-- PAGE -->

## Aceptación A19-A24 · Órdenes y cambios

**A19 · Plazos y cancelación de apartado.** Probar final de días naturales 7 y 45, alerta desde siete días antes de vencer y plazo configurado conservado. Vencimiento no libera automáticamente; liberar requiere autorización. Admitir liquidación excepcional antes de liberar. Cancelación válida de total $1,000 con $400 pagados entrega mercancía por al menos $400; libera originales y conserva atribución/diferencia sin duplicar. E5/E6; APA-10/16, D03/D06.

**A20 · Reparación y presupuesto.** Recibir varias piezas del cliente fuera del inventario comercial; total $1,000, mínimo $500. Rechazar descuento y abono intermedio. Modificar presupuesto pendiente con permiso, motivo y acuerdo: al subir no pedir otro anticipo; al bajar debajo de pagado crear solo exceso como saldo. Aplicar D05 para liquidación. Tres tickets al recibir y dos al entregar, copia interna con firma. E5; REP-01/07.

**A21 · Estados y recogida.** Recibida → en reparación → lista → entregada. Dashboard solo avanza estados permitidos; entrega exclusivamente en POS y liquidada. Plazo 45 días desde lista, conservado por orden: al vencer alerta sin cancelación/baja automática. Corregir lista → en reparación suspende plazo; nuevo lista reinicia uno completo con historial. E5/E7; REP-08/13.

**A22 · Cancelación de reparación.** Permitir solo recibida, nunca antes en reparación y no liquidada, online con autorización. Si se corrigió de en reparación a recibida sigue bloqueada. En cancelación válida devolver piezas, aplicar anticipo a mercancía igual/mayor y documentar diferencia; no saldo guardado automático. Valor previo sigue Matanga; diferencia a vendedores. Ticket interno firmado. E5/E6; REP-12/15.

**A23 · Cambios parciales/repetidos.** Devolver valor neto original $800 y entregar $1,000 → cobrar $200, conservar atribución $800 y asignar $200 a quienes atienden. Verificar buen estado, origen y no reutilización de unidades ya cambiadas; plazo hasta final día 15 y nuevo plazo solo para nuevas piezas. Descuento, costo y cantidades conforme D01/D03; saldo usado no se restituye además. E6; CAM, CLI-23.

**A24 · Corrección y reemplazo de venta.** Intentar editar partidas finalizadas: usar anulación/reemplazo enlazados. Revertir una vez, bloquear venta con cambio vinculado y guardar motivo/autorización. Inventario revierte en fecha real de cancelación; importes ajustados se vinculan al período/sesión originales. Probar medio de pago conservando total y reemplazo distinto según D04. POS imprime interno; dashboard no. E6; COR-01/15.

<!-- PAGE -->

## Aceptación A25-A30 · Integración y salida

**A25 · Cierre corregido y bloqueo económico.** Corregir en octubre venta de septiembre $1,000 de efectivo a tarjeta: conservar cierre contado/fondo/sobre/diferencia original, mostrar ajuste y no mover efectivo físico de octubre. Pago de orden pendiente puede corregirse y solo admin anularlo según D05. En orden liquidada bloquear importes, medios, piezas/presupuesto incluso al admin; consulta/entrega siguen permitidas. E6; COR-09/17.

**A26 · Indicadores y períodos.** Apartado $1,000 recibe $400 en septiembre y $600 al liquidar en octubre: cobros por esas fechas y venta completa en octubre; costo del alta $500 conserva beneficio $500. Reparaciones separadas, saldo sin dinero nuevo; cambios/cancelaciones según fórmulas aprobadas. Comparar tarjetas, gráfica, tabla y Excel; filtros no duplican vendedores ni tickets. E7; CAL, RPT.

**A27 · Navegación, seguimiento y alertas.** Buscar folio/cliente/teléfono, abrir vínculos y PDF cliente/negocio con controles. Sesiones abiertas primero; revisar diferencia sin alterar cierre. Apartado liquidado sin recoger aparece separado de vencidos. Alerta lleva al origen; revisar no resuelve, desaparecer causa resuelve y reaparecer crea nueva vinculada. Probar estados permitidos del dashboard y entrega bloqueada. E7; DAS-26/45.

**A28 · Filtros, frescura y carga.** Verificar fecha/hora en Ciudad de México, accesos rápidos, sucursales/vendedores y agrupación. Comparar mes en curso con mismos días previos y evitar infinito con base cero. Excel conserva filtros/actualización; POS desconectado se identifica con última recepción. Histórico sin hora/costo no inventa precisión/beneficio. Medir objetivos D23 con datos de prueba representativos. E7/E8; DAS-04/09, MIG-04/05.

**A29 · Migración reproducible.** Cargar sobre entorno de ensayo, comparar conteos, importes, stock por estado, saldos y referencias. Repetir carga no duplica. Tres años de ventas y pendientes sin límite; conservar referencias antiguas y archivo del resto. Histórico no descuenta stock ni ingresa caja; negativos y faltantes tienen tratamiento documentado. Ensayar congelamiento, carga final y rechazo ante diferencias sin explicar. E8; MIG.

**A30 · Restauración y jornada de salida.** Restaurar central y sustituir un POS con pendientes; reenvío no duplica recibidos. Verificar segunda copia, objetivos D20, una caja apagada y fallas de red/impresora. Ejecutar jornada de todos los módulos con roles reales y datos de prueba, después ensayo de corte/retorno incluyendo ventas nuevas. Evidencia de capacitación, soporte y versión aprobada. E8; RES, TIC, GEN-01.

<!-- PAGE -->

## Cobertura del PDF · Operación e inventario

La columna página corresponde a la numeración impresa del PDF v2. Los rangos incluyen todos los requisitos presentes del grupo; los identificadores no consecutivos se respetan. Esta matriz asigna cobertura, no certifica cumplimiento.

| Sección / página fuente | Requisitos y contenido | Etapa / pruebas |
| --- | --- | --- |
| 02 / p. 3 | GEN-01/05; alcance, web, remoto, fechas e identidades | E0/E1/E8; A01/A28/A30 |
| 03 / p. 4 | ALM-01/03; tres almacenes, Coyoacán compartido | E0/E2; A04/A10 |
| 04 / p. 5 | ARQ-01/04; central/local y actualización remota | E1; A01-A03/A06/A28 |
| 05 / p. 6 | OFF-01/04; operaciones offline y secuencia | E1/E3; A02/A03 |
| 06 / p. 7 | ACC-01/04, VEN-01/03; permisos y atribución | E1/E3/E7; A01/A14 |
| 07 / p. 8 | VTA-01/02, PAG-01/05; ventas y medios | E3/E4; A11/A15 |
| 08 / p. 9 | CAJ-01/07; caja, fórmula y cierre | E3/E6; A12/A13/A25 |
| 09 / p. 10 | CAM-01/08; cambio, plazo y atribución | E6; A23 |
| 10 / p. 11 | APA-01/09; alta, abonos, liquidación y entrega | E5; A18/A25 |
| 11 / p. 12 | APA-10/16; vencimiento y cancelación | E5/E6; A19 |
| 12 / p. 13 | REP-01/07; presupuesto, pagos y tickets | E5; A20 |
| 13 / p. 14 | REP-08/15; estados, plazo y cancelación | E5/E6; A21/A22 |
| 14 / p. 15 | INV-01/09; catálogo y proveedores | E2; A07 |
| 15 / p. 16 | INV-20/25; códigos y etiquetas | E2; A05/A07 |
| 16 / p. 17 | IMP-01/08; Excel, errores y reintentos | E2; A08 |
| 17 / p. 18 | ING-01/07; recepción recurrente y reversión | E2; A09 |
| 18 / p. 19 | MOV-01/05, MIN-01/02; movimientos y mínimos | E2/E5/E7; A10/A27 |

Para programar, cada fila se desglosa en tareas por requisito. Una tarea incorpora condiciones normales, límites, permisos, conexión, efectos en datos, comprobante, auditoría y prueba. La aceptación se contrasta con el texto completo de la fuente, también cuando agrupa varios identificadores.

<!-- PAGE -->

## Cobertura del PDF · Administración y control

| Sección / página fuente | Requisitos y contenido | Etapa / pruebas |
| --- | --- | --- |
| 19 / p. 20 | DAS-01/09; dashboard, filtros y exportación | E0/E7; A26/A28 |
| 20 / p. 21 | CAL-01/06; ventas, cobros y beneficio | E3/E5/E6/E7; A26 |
| 21 / p. 22 | RPT-01/07; productos, vendedores y comisiones | E7; A14/A26 |
| 22 / p. 23 | DAS-26/29, DAS-31/33; caja y comprobantes | E7; A16/A25/A27 |
| 23 / p. 24 | DAS-34/45; órdenes y alertas, IDs agrupados | E5/E7; A19/A21/A27 |
| 24 / p. 25 | TIC-01/03; impresión y continuidad | E1/E2/E5/E8; A05/A20/A30 |
| 25 / p. 26 | MIG-01/06; tres años, pendientes y calidad | E0/E8; A28/A29 |
| 26 / p. 27 | COR-01/08; anulación, pagos y vendedores | E6; A14/A24 |
| 27 / p. 28 | COR-09/14; original, ajuste y remoto | E6/E7; A24/A25 |
| 28 / p. 29 | COR-15/17; fechas y órdenes liquidadas | E5/E6; A24/A25 |
| 29 / p. 30 | Ejemplos de corrección y reemplazo pendiente | E0/E6; D04, A24/A25 |
| 30 / p. 31 | CLI-01/11; ficha, saldo y vigencia | E4; A15/A17 |
| 31 / p. 32 | CLI-12/19 y CLI-18-A; código y bloqueo | E4; A16 |
| 32 / p. 33 | CLI-20/25; restituciones y altas manuales | E4/E6; A15/A23/A25 |
| 33 / p. 34 | CLI-26/29 y CLI-27-A; edición/unificación | E4; A17 |
| 34 / p. 35 | Matriz confirmada y precedencia de bloqueos | E1/E4/E6; A01/A16/A25 |
| 35 / p. 36 | RES-01/06; copias y restauración | E1/E8; A02/A03/A06/A30 |
| 36 / p. 37 | OFF-05/09; disponibilidad y sin conteo | E1/E2/E3; A04/A10 |

Las secciones 37-39 (pp. 38-40) se reflejan en D01-D24, A01-A30 y en la condición de primera salida completa. La portada y guía (pp. 1-2) aportan versión, contexto y precedencia COR-17. No se tratan las referencias a prototipos previos como funciones terminadas.

<!-- PAGE -->

## Primeros trabajos y forma de colaboración

### Encargos iniciales, en orden

**T01 · Abrir matriz de trabajo.** Desglosar las páginas 21-22 por identificador exacto del PDF; relacionar tarea, decisión y prueba. Entrega: lista priorizada con estado «pendiente». Comprobación: todas las secciones/IDs presentes tienen destino.

**T02 · Revisar base existente.** Leer código, esquema y pruebas del prototipo en un entorno aislado; documentar diferencias con v2. Entrega: conservar/adaptar/retirar, sin asumir validez por pruebas antiguas. Atender inventario compartido, pagos, órdenes y sesiones.

**T03 · Cerrar casos base y diseñar.** Resolver ejemplo D01, dibujar venta/caja y estados de órdenes, acordar modelo y prototipo POS/dashboard con datos ficticios. Entrega: recorrido revisable y decisiones para E1. Se puede preparar mientras se revisa el prototipo.

**T04 · Inventariar equipos y datos.** Obtener modelo Star, etiquetas, lectores, sistemas operativos, topología de red, volumen de PV y responsables de acceso. Entrega: ficha técnica y copia de ensayo disponible; nunca credenciales en documentos compartidos.

**T05 · Ejecutar prueba E1.** Con T02-T04 y contratos listos, implementar persistencia/sincronización/impresión y recuperación; ejecutar A01-A06/A30 en su alcance inicial. Entrega: informe de resultados y decisiones D17-D22 sustentadas.

### Responsabilidades y control del avance

| Participante | Responsabilidad |
| --- | --- |
| Responsable del negocio | Prioridades, reglas pendientes, datos iniciales, validación funcional y decisión de puesta en operación. |
| Desarrollo, con apoyo de Codex | Especificación, prototipos, código, migraciones, pruebas, documentación y evidencias; registrar límites y fallas. |
| Soporte / persona con acceso físico | Equipos, red, impresoras, restauración física, instalación y contingencia. La persona concreta está por designar. |
| Usuarios designados | Ensayar venta, caja, recepción y entrega; comprobar claridad de pantallas y tickets. |

**Ciclo de trabajo:** elegir tarea → cerrar dependencias → implementar → ejecutar pruebas → demostrar → registrar resultado. Una función termina cuando cumple requisitos, permisos, conectividad, datos, comprobantes y pruebas aplicables, con documentación suficiente para repetir la verificación.

**Estado y costos:** registrar por tarea pendiente/en curso/en validación/aceptada, con evidencia. Tras G1 estimar esfuerzo por módulo y costos recurrentes de alojamiento, respaldos y mantenimiento. Mantener entornos de desarrollo, ensayo y operación separados. Los cambios de alcance se documentan con impacto; ninguna reducción del primer lanzamiento se presume autorizada.
