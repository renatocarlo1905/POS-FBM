# Diccionario, ejemplos y decisiones

E0 v1.0 · 23/09/2026. **Confirmado** indica regla del PDF. **Propuesta** requiere revisión, incluso si aparece en una maqueta. No se han recibido nuevas aprobaciones al generar esta versión.

## Indicadores confirmados y alcance

| Indicador | Definición / fecha | Exclusiones y pendientes |
| --- | --- | --- |
| Ventas brutas | Importe de mercancía antes de descuentos reconocida en el período | Apartado al liquidar; reparaciones separadas; cambios según D03 |
| Descuentos | Reducciones comerciales de esas ventas | No descuentos en apartado/reparación; reparto por pieza pendiente D01 |
| Ventas netas | Brutas menos descuentos, con ajustes reconocidos y vínculos al período correcto | Anticipos no se suman como ventas otra vez; conversiones D03/D06 |
| Cobros recibidos | Dinero neto efectivamente recibido en efectivo, tarjeta y transferencia en fecha de cobro | Saldo a favor no es dinero nuevo; fondo/entradas/retiros no son ventas/cobros comerciales |
| Beneficio bruto mercancía | Neto menos costo histórico asociado | Apartado usa costo al alta; reparaciones aparte; no utilidad después de renta/sueldos; cambios D03 |
| Efectivo esperado | Fondo + cobros netos efectivo + entradas - gastos - retiros | Tarjeta/transferencia/saldo excluidos; vista ajustada separada del cierre original |
| Diferencia de caja | Contado menos esperado | Negativo faltante, positivo sobrante; original no se sobrescribe |
| Atribución vendedor | Neto atribuible dividido entre participantes | Operador/autorizador distinto; apartado a iniciales; reparación Matanga; diferencia de cambio a quienes atienden |
| Comisión | Atribuido en filtro × porcentaje del cálculo | Guardar filtros/porcentaje/fecha; no estados de comisión pagada; redondeo D01 |
| Disponible | Movimientos por producto/almacén/estado disponible | Apartadas y dañadas excluidas; sin cupos ni inventario consultable por sucursal |

**Día de negocio:** America/Mexico_City. Ventanas naturales incluyen el último instante del día límite para cambios/apartados según PDF. La hora de vencimiento del saldo sigue D07. Histórico sin hora debe aparecer como precisión de fecha y no falsear análisis horario.

## Ejemplos verificables (en MXN)

| Caso | Resultado esperado confirmado |
| --- | --- |
| Venta 1,000; tarjeta 600; efectivo recibido 500 | Aplicado efectivo 400; cambio 100; caja +400; venta 1,000; cobro neto 1,000 |
| Venta 1,000, dos vendedores | Atribuido 500/500; filtro de ambos 1,000 |
| Fondo 500 + efectivo 400 + entrada 100 - gasto 50 - retiro 200 | Esperado 750; contado 730 → diferencia -20; fondo 300 + sobre 430 = 730 |
| Apartado 1,000, costo alta 500; septiembre 400, octubre 600 | Cobros 400/600; venta y atribución 1,000 en octubre; beneficio 500; entrega no suma |
| Cambio: devuelta neta 800, nueva neta 1,000 | Cobro diferencia 200; valor 800 conserva vendedores, diferencia 200 a quienes atienden; costo D03 |
| Cancelación temprana apartado 1,000 con 400 pagados | Mercancía nueva por al menos 400; no exigir 1,000; no devolución de dinero |
| Reparación pendiente 1,000 con 500 pagados; presupuesto baja a 400 | Exceso 100 en saldo a favor; cómo registrar liquidación de los 400 está pendiente D05 |
| Ambos POS offline conocen 1 y cada uno vende 1 | Conservar 2 ventas; central -1 y alerta; nuevo intento con conocido ≤0 se bloquea |
| Corregir efectivo a tarjeta 1,000 tras cierre | Ajusta sesión histórica, conserva contado y diferencia original; no efectivo físico en caja de hoy |

Estos ejemplos no resuelven automáticamente los casos de frontera pendientes. La maqueta usa importes simples y no representa aprobación fiscal o contable externa.

## Registro D01-D24

Todas abiertas a revisión. Responsable N = negocio; D = desarrollo; S = soporte. Cada cierre necesita respuesta, fecha, responsable y actualización de pruebas. Se conservan IDs del plan.

| ID | Decisión / propuesta concreta | Responsable | Antes de | Evidencia de cierre |
| --- | --- | --- | --- | --- |
| D01 | Modalidad descuento: permitir % e importe con tope efectivo equivalente por usuario (propuesta). Guardar dinero en centavos; reparto proporcional por pieza y mayor residuo, desempate por número de partida (propuesta). Pregunta al usuario pendiente. | N+D | E1 ejemplo; E3/E6 | Casos 100/3, descuento parcial y comisión con centavos |
| D02 | Liquidación en otra sucursal: recomendar reconocer venta en sucursal del alta, mostrar sucursal de cada cobro separada. Alternativa: sucursal de liquidación. No cambia vendedores iniciales. | N | E5/E7 | Apartado abierto S1 y liquidado S2, reporte esperado |
| D03 | Proponer ajustar costo por entrada de pieza retornada con costo histórico y salida de pieza nueva con su costo aplicable; validar cambios repetidos y conversiones. Fórmula definitiva abierta. | N+D | E6/E7 | Tres cambios encadenados y filtros de vendedor sin duplicar |
| D04 | Distinguir corregir registro de cobrar diferencia real. No habilitar reemplazo de importe distinto hasta definir cada resultado. | N | E6 | Ejemplos cobrado real menor/igual/mayor al correcto |
| D05 | Proponer evento de liquidación por ajuste de presupuesto cuando deuda llega a cero; no reabrir después COR-17. Definir orden bajo mínimo tras anulación. | N | E5/E6 | Caso reparación 500 pagado/400 presupuesto; apartado bajo 40% |
| D06 | Mantener saldo por origen y aplicación separada de dinero; definir atribución y reporte de saldo manual/anticipos cancelados. | N+D | E4-E7 | Caso origen manual y reparación usados en mercancía |
| D07 | Proponer vigencia en días naturales hasta fin de día de vencimiento local; opción sin vencimiento por defecto permanece. | N | E4 | Caso hora límite, restitución vencida y configuración futura |
| D08 | Proponer conservar configuración futura de ficha sobreviviente con vista previa; verificación de identidad para reimpresión por definir. | N | E4 | Unificación con vencimientos y bloqueo distintos |
| D09 | Proponer plantilla con IDs de catálogos, 2 descripciones, cantidad, costo/precio, peso/imagen opcionales. Límites y normalización deben acordarse. | N+D | E2 | Archivo válido, duplicado interno y repetición legítima |
| D10 | Evaluar Code 128 para 15 dígitos (candidato, sin compatibilidad afirmada). Congelar esquema y alias después de prueba de lector/etiqueta. | N+D+S | E2 | Lectura con ceros y código histórico; agotamiento |
| D11 | Proponer descargar y validar imagen de enlace al importar, con límites y fallo explicable; sin imagen no bloquear venta. | D+N | E2 | PNG, enlace fallido y archivo no permitido |
| D12 | Proponer trazabilidad de ingreso y bloqueo de reversión cuando unidades comprometidas no pueden deshacerse; determinar lotes y productos inactivos. | N+D | E2 | Ingreso con venta/reserva/traspaso posterior |
| D13 | Proponer barrera de sincronización por terminal antes de traspaso, no solo indicador de internet. Negocio decide extensión a bajas/ajustes. | N+D | E2 | Venta pendiente en otro POS impide salida |
| D14 | Mapear fuente PV a modelo propuesto sobre copia; no se restauró el respaldo en E0. | N+D | E8 | Correspondencias y referencias antiguas preservadas |
| D15 | Elegir fecha de corte; tres años relativos a esa fecha. Negativos se revisan externamente, no se convierten automáticamente a cero. | N+D | E8 | Conteos y acta de corte |
| D16 | Proponer indicadores de cobertura conocida/desconocida y filtros que expliquen exclusión de horas faltantes. | N+D | E7/E8 | Dataset histórico con faltantes y totales conciliados |
| D17 | Proponer aplicación central modular con PostgreSQL; evaluar servicio local por POS para persistencia/impresión. Hospedaje, lenguajes y versiones no elegidos. | D+N | E1 | Prueba técnica y costo/mantenimiento comparados |
| D18 | Separar usuarios, vendedores y credenciales; permisos por acción. Diseñar reimpresión protegida del código del cliente (hash solo no permite recuperar código fijo). Vigencia offline abierta. | N+D | E1/E4 | Matriz de denegaciones y mecanismo de recuperación |
| D19 | Identificador estable, secuencia local y acuse; no reemplazar saldo central con saldo local. Definir una sesión operativa por sucursal y recuperación de contador/reloj. | D+N | E1/E3 | Dos dispositivos, pérdida de acuse, reinstalación |
| D20 | Evaluar dispositivo local dedicado independiente del otro POS. Elegir frecuencia/retención, pérdida máxima tolerable y tiempo de restauración. Ninguna compra aprobada. | N+D+S | E1/E8 | Restauración central/POS con otra caja apagada |
| D21 | Obtener modelo Star y tamaños reales; verificar Linux/USB, corte, etiqueta y lector Sewoo. | S+D+N | E1/E2 | Muestras físicas firmadas para uso |
| D22 | Proponer plantillas separadas cliente/negocio/trabajo, sin código cliente en copias internas. Acordar evidencia de cambios de presupuesto. | N+D | E5 | Ejemplos de recepción/entrega y firma manuscrita |
| D23 | Medir volumen y concurrencia real; acordar límites de respuesta/tiempo offline antes de prometer capacidades. | N+D | E7/E8 | Carga representativa y tiempos medidos |
| D24 | Responsable de corte/retorno/soporte por designar; proponer ensayo de jornada y retorno incluyendo ventas nuevas. | N+D+S | E8 | Procedimiento ensayado y responsables identificados |

## Decisiones iniciales para E1

Cerrar solo el caso base de D01, arquitectura candidata y alcance de prueba D17, identidad/permisos de prueba D18, secuencia D19, destino/objetivos iniciales D20 y equipos/formato mínimo D21-D22. Se puede diseñar/probar con datos ficticios sin fijar aún todas las reglas de cambios y migración, dejando pendientes explícitos.

## Matriz mínima de permisos

| Derecho independiente | Delegable a empleado con derecho | Admin exclusivo | Internet |
| --- | --- | --- | --- |
| Venta, descuento y límite; apertura/cierre; entrada/gasto/retiro | Sí, cada uno separado | No | Admitido offline con política local definida |
| Ver/modificar costo; modificar precio; catálogo/ingreso/traspaso/baja | Sí, separado | No | Online para mutar inventario |
| Cambio comercial; cancelación errónea; corregir pago; corregir vendedor | Sí, separado | No | Sí |
| Modificar presupuesto pendiente; estados/correcciones reparación; excepciones apartado | Sí, separado | No | Sí |
| Anular pago de orden pendiente | No | Sí | Sí |
| Aplicar saldo; editar ficha; reimprimir código | Sí, separado | No | Sí para saldo/código |
| Vigencia, sustituir/desbloquear código, saldo manual/anulación, unificación | No | Sí | Sí |
| Dashboard | No | Sí | Información central recibida |

Una autorización puntual registra operador y autorizador; no cambia atribución ni sobrepasa COR-17, cambio vinculado, saldo vencido o saldo manual ya utilizado. Los perfiles nominales de empleados y sus porcentajes no están inventados.
