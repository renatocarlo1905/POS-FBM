# Verificación de E0

Fecha: 23/09/2026. Resultado: entregables de diseño preparados para revisión. La aprobación de negocio G0 sigue pendiente; este reporte no certifica un sistema operativo.

## Cobertura documental

- Se cotejaron 209 identificadores impresos con su texto y página en el PDF v2 de 40 páginas. Los identificadores agrupados se conservan tal cual. La matriz incluye tarea, pantalla, dependencias, decisiones y escenarios de aceptación.
- El archivo fuente tiene SHA-256 `5d00d23a12eea66ebcc2e49762b9d77e2477fffc185b196e3bc3de394f9c9329`.
- A01-A30 son los 30 escenarios de aceptación del plan, conservados para ejecución durante el desarrollo. No son pruebas aprobadas del sistema final.
- D01-D24 conservan decisiones abiertas y propuestas diferenciadas de reglas confirmadas. Los acuerdos sin identificador se tratan además en flujos, reglas y modelo; la matriz no sustituye la lectura de las tablas y notas del PDF.
- La revisión del código previo fue estática. No se ejecutaron migraciones, PostgreSQL, restauraciones ni pruebas sobre datos del negocio.

## Comprobaciones automatizadas del prototipo

Ejecutado `node prototype/e0/test-domain.cjs`: **9 grupos aprobados**.

| Grupo | Comprobación |
| --- | --- |
| Dinero | Centavos exactos, coma decimal, rechazo de precisión ambigua |
| Pago mixto | Separación de efectivo recibido/aplicado/cambio |
| Límites del pago | Rechazo de pago insuficiente y cambio procedente de tarjeta |
| Disponibilidad | Rechazo de carrito vacío o cantidad superior a existencia conocida |
| Apartados | Abono positivo hasta el saldo, únicamente conectado |
| Reparaciones | Rechazo de abonos intermedios |
| COR-17 | Bloqueo económico tras liquidar |
| Entrega | Requiere POS, conexión, liquidación y reparación lista |
| Caja | Diferencia permitida; fondo y sobre deben sumar el contado |

También se comprobó la sintaxis de `app.js`. Estas pruebas corresponden a funciones de la maqueta en memoria, sin garantías de concurrencia, seguridad o durabilidad.

## Recorridos realizados en navegador

| Recorrido | Resultado observado |
| --- | --- |
| Resumen inicial | Ventas netas $3,930; cobros $3,830; beneficio $2,090 en los datos ficticios |
| Filtro Sucursal 1 | Ventas $1,650; cobros $2,150; beneficio $870 |
| Apertura y venta | Apertura $500; venta de anillo $1,000 con recibido efectivo $500 y tarjeta $600: aplicado $400, cambio $100, disponibilidad pasa de 8 a 7 |
| Cierre ciego | Formulario sin esperado explícito; contado $880/fondo $500/sobre $300 rechazado; sobre $380 aceptado; esperado $900, diferencia -$20 |
| Apartado AP-001 | Pago final $600 sobre anticipo $400; queda liquidado, pendiente de entregar; aviso COR-17 y acción de entrega separados |
| Entrega AP-001 | Estado pasa a Entregada |
| Desconexión simulada | Nuevo apartado deshabilitado; aviso del módulo conectado visible |
| Inspección visual | Dashboard de escritorio revisado: navegación, filtros, indicadores y gráfica legibles |
| Restablecimiento | Reiniciar devuelve el ejemplo a sus valores iniciales |

Se restableció la demostración al terminar. No se ejecutó una auditoría de accesibilidad, compatibilidad completa entre navegadores ni verificación en los equipos físicos del negocio. El navegador solo prueba la simulación; no se cortó una red real.

## Límites y siguientes comprobaciones

La maqueta omite implementación real de descuentos, crédito, cambios, correcciones, importación, permisos, impresión, persistencia y sincronización. Esas funciones mantienen su lugar en las tareas E1-E8 y en el alcance de la primera puesta en operación. Las vistas informativas y los ejemplos no deben confundirse con funciones terminadas.

Antes de certificar E1 se necesitan pruebas con dos dispositivos, fallos/reintentos, inventario compartido, permisos aplicados en servidor, cola persistente, copias independientes y restauración. Antes de la sustitución operativa deberán pasar todos los escenarios A01-A30 con los módulos integrados, migración y equipos reales.
