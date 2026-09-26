# Revisión estática del prototipo existente

23/09/2026. Se leyeron todas las migraciones 001-003 y ambas pruebas de base/restauración, además de `manage.py`, README y modelo. **No se inició Docker, no se aplicaron migraciones, no se leyeron credenciales, no se restauró PV y no se ejecutaron las pruebas de PostgreSQL.** Hallazgos de código, no certificación de comportamiento ejecutado.

La definición efectiva de `receive_sale` es la de migración 003, que reemplaza la de 001. Las referencias siguientes son relativas a la raíz POS-nuevo; líneas verificadas en los archivos actuales.

## Conservar y ampliar

| Evidencia | Valor aprovechable | Acción |
| --- | --- | --- |
| 001_core.sql:7, 59-79 | Decimales exactos, snapshots de partidas, hora de operación/recepción separadas | Conservar conceptos; ampliar campos/calidad histórica |
| 003_validation.sql:14-20 | Bloqueo por UUID, mismo payload devuelve resultado, cambio de payload se rechaza | Generalizar a caja/órdenes/inventario; comprobar acuse perdido en E1 |
| 003_validation.sql:51-69 | Cabecera/partidas/medios/vendedores dentro de una función transaccional | Conservar unidad atómica; ampliar permisos y reglas antes del cobro |
| 003_validation.sql:57-60, 70-72 | Ventas ya cobradas con faltante se conservan y alertan | Conservar para ingestión offline; distinguir autorización de venta nueva |
| 001_core.sql:135-141 | Prohibición de sobrescribir/borrar hechos | Conservar originales; diseñar eventos compensatorios para correcciones |
| 001_core.sql:128-133 | Correspondencias legacy | Ampliar integridad destino, lotes y calidad; no equivale a migración hecha |
| manage.py:13-20 | Migraciones versionadas | Añadir nuevas migraciones, no reescribir las ya aplicadas |
| test_database.py:49-83 | Casos de reintento, atomicidad, secuencia y concurrencia | Reutilizar intención; actualizar fixtures y ampliar a v2 |

## Adaptar antes de construir operación real

| Hallazgo y evidencia | Diferencia con v2 | Cambio requerido / prueba |
| --- | --- | --- |
| 001_core.sql:20-27; 003_validation.sql:23, 56-59 | Terminal posee ubicación; saldo/salida calculados por ubicación local | Desvincular disponibilidad de local y consumir Coyoacán compartido por estado. ALM/OFF, A04/A10 |
| 001_core.sql:95-115 | Movimientos no distinguen disponible/apartado/dañado | Añadir estado y reserva; vistas por almacén/estado; traspasos conservan vínculos. E2/E5 |
| 001_core.sql:37-44 | Costo/descripción larga opcionales; proveedor e imagen ausentes; pureza extra y peso sin máximo 999 | Modelo de catálogo v2, validaciones/alias/catálogos. No promover campo pureza a requisito. A07 |
| 001_core.sql:45-55 | Sesión por terminal; faltan movimientos, esperado, fondo/sobre y coordinación operativa | Modelo por sucursal con origen dispositivo y secuencia offline; cierre ciego, única sesión operativa. A12/A13 |
| 001_core.sql:81-87; 002_locations.sql:14 | Pago enlazado solo a venta; semillas efectivo/tarjeta | Destino de órdenes/correcciones; transferencia/saldo; recibido/aplicado/cambio; datos tarjeta. A11/A15/A18/A20 |
| 001_core.sql:88-92 | Lista de participantes sin reparto/versiones | Reparto exacto y ajustes auditados, reconocimiento apartado, comisión capturada. A14 |
| 003_validation.sql:60-67 | No exige conjunto de vendedores no vacío; pagos carecen de límites por tipo/datos tarjeta | Validar antes de confirmar nueva venta. Recepción antigua debe conservar hechos con revisión si política cambió. A01/A11/A14 |
| 003_validation.sql:50 | Total debe ser >0, sin decisión explícita en v2 sobre descuento del 100% | No trasladar ese supuesto como acuerdo: resolver D01 |
| 001_core.sql:118-126 | Acuse ligado a una venta y dependencia solo en FK | Generalizar eventos/caja/acuses y espera causal, persistencia local y recuperación. A02/A03 |
| 001_core.sql:28-32, 220-221 | Staff no es autenticación; REVOKE público no implementa permisos de negocio | Identidad de terminal/usuario, validación de derechos/límites y autorización. A01 |
| 001_core.sql:135-141 | Inmutabilidad sola impide editar, pero no permite corregir con historial | Crear modelos/eventos COR sin desactivar protección original. A24/A25 |

## Diseñar como módulos nuevos

No se encontraron implementaciones de clientes/saldo/códigos, apartados, reparaciones, cambios/correcciones, dashboard, generación de etiquetas, importación Excel, cola local durable o respaldo externo local en los archivos revisados. E0 define su diseño; el plan E1-E8 mantiene su construcción y pruebas obligatorias.

`test_database.py:88-92` valida que no se comparta una asignación local y que Coyoacán se obtenga sumando ubicaciones. Debe retirarse **ese supuesto de las pruebas nuevas**, conservando el historial del laboratorio. Pasar esos tests antiguos no demostraría stock compartido v2.

`test_backup.py:15-23` compara estructura, catálogos, funciones y conteo de ventas tras restaurar un dump de desarrollo. No prueba recuperar operaciones no sincronizadas desde un POS perdido, retención externa ni tiempo de recuperación. `manage.py:40-46` produce backup bajo comando; no programa copias automáticas de producción.

## Orden de adaptación propuesto

1. Mantener laboratorio actual como antecedente. En E1, migración nueva y base desechable para ensayos; conservar las migraciones publicadas.
2. Modelar stock por almacén/estado, sesiones operativas por sucursal y pagos generalizados, con contratos antes de tocar consumidores.
3. Separar autorización de venta nueva de recepción idempotente de venta ya cobrada.
4. Construir persistencia local/cola, política de identidades y recuperación; probar fallo entre guardado, impresión y acuse.
5. Extender módulos según dependencias del plan. Hacer migración PV solo sobre copia y, al final, bajo procedimiento E8.

Conclusión: la base es aprovechable como laboratorio de transacciones, idempotencia e historial. El modelo operativo necesita adaptación a v2; no se recomienda conectar todavía las cajas al esquema actual.
