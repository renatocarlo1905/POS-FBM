# Tareas, dependencias y puerta hacia E1

Fecha 23/09/2026. Cada requisito de `requisitos.json` se asigna a una tarea siguiente. Los IDs E*-* son paquetes implementables, no funciones ya construidas. Todas las tareas E1-E8 están pendientes. El estado de entregables E0 se encuentra en README.

| Tarea | Entregable / pantalla | Dependencias | Decisiones | Aceptación |
| --- | --- | --- | --- | --- |
| E0-01 | Matriz exacta y casos de aceptación | PDF/plan | Ninguna para preparar | Cobertura de todo ID impreso; páginas verificadas |
| E0-02 | Flujos y prototipo de navegación | E0-01 | D01 ejemplos | Venta/caja/órdenes recorribles; prohibiciones visibles |
| E0-03 | Modelo y contratos | E0-01 | D01/D17-D20 | Identidades y hechos diferenciados; atomicidad explícita |
| E0-04 | Revisión del laboratorio | Archivos existentes | Ninguna | Evidencia por archivo/línea y acciones conservar/adaptar/nuevo |
| E0-05 | Revisar con negocio | E0-01/04 | D01 inicial, D17-D22 | Registrar respuesta, fecha, responsable; G0 |
| E1-01 | Identidades, permisos y autorización | E0-03/05 | D18 | A01, API deniega acceso directo |
| E1-02 | Cola local, acuse, reloj y recepción | E0-03/04, E1-01 | D17/D19 | A02-A04, reenvío y stock compartido |
| E1-03 | Impresión, copia local y restauración | E1-02, equipos | D20-D22 | A05/A06/A30 |
| E2-01 | Catálogo, proveedor, código y etiqueta / P06 | E1-01/03 | D09-D11/D21 | A07 |
| E2-02 | Inventario por estado, traspaso/mínimo / P06,D04 | E1-02, E2-01 | D13 | A04/A10 |
| E2-03 | Importación y recurrentes / P06 | E2-01/02 | D09/D12 | A08/A09 |
| E3-01 | Venta, pagos, atribución / P01 | E1-02,E2-02 | D01/D18 | A11/A14; saldo termina en E4 |
| E3-02 | Sesiones, movimientos y cierre / P02 | E1-02,E3-01 | D19 | A02/A12/A13 |
| E4-01 | Cliente, código y unificación / P05,D08 | E1-01,E3-01 | D08/D18 | A16/A17 |
| E4-02 | Saldo por origen y aplicación / P05 | E4-01,E3-02 | D06/D07 | A15; integra reducción en E5 |
| E5-01 | Apartado y entrega / P03,D05 | E2,E3,E4 | D02/D05 | A18/A19/A25 |
| E5-02 | Reparación y presupuesto / P04,D05 | E3,E4 | D05/D22 | A20-A22/A25 |
| E6-01 | Cambios/cancelaciones comerciales / P07 | E2-E5 | D01/D03/D06 | A19/A22/A23 |
| E6-02 | Correcciones / P08 | E3-E5 | D04/D05/D07 | A24/A25 |
| E7-01 | Indicadores, reportes, comisión / D01,D06 | E3-E6 | D01-D03/D06/D16 | A14/A26/A28 |
| E7-02 | Consultas, documentos y alertas / D02-D05,D07 | E2-E6 | D22/D23 | A27/A28 |
| E8-01 | Migración, calidad y conciliación | Modelo estable E2-E6 | D14-D16 | A29 |
| E8-02 | Ensayo, capacitación, corte/retorno | E1-E8-01 aceptadas | D20-D24 | A01-A30; todos los módulos de salida |

Referencias `E2`, `E3` etc. significan todas las tareas de esa etapa que afecten al entregable. E4/E5 integran funcionalidad pendiente de pago/órdenes en E3: completar pruebas integradas al incorporarlas, sin declarar prematuramente aceptado el conjunto.

## Criterio de terminado por tarea

Regla confirmada implementada; estados/límites probados; permisos reales y acceso directo verificados; modo conectado/desconectado apropiado; efecto en caja/stock/reportes consistente; comprobantes y auditoría; errores/reintentos sin duplicación; evidencia con versión exacta. Una maqueta solo satisface revisión visual, nunca esas garantías operativas.

## G0: lo que debe quedar resuelto para avanzar con E1

| Entrada | Estado | Responsable / siguiente acción |
| --- | --- | --- |
| Alcance completo y mapa funcional | Preparados, revisión pendiente | Negocio recorre prototipo y valida flujos |
| Matriz por ID y modelo de hechos | Preparados | Desarrollo incorpora observaciones |
| Modalidad de descuento y caso monetario inicial | Pregunta enviada, sin respuesta registrada todavía | Negocio decide D01; no cerrar todo redondeo implícitamente |
| Equipos: modelo Star, SO y tamaños de etiqueta/papel | No disponibles en el PDF | Persona con acceso físico aporta ficha D21 |
| Arquitectura/persistencia de prueba | Propuesta abierta | Desarrollo selecciona candidatos D17 con argumentos/costos |
| Identidades/permisos y sesión offline | Propuesta abierta | Desarrollo + negocio acuerdan D18-D19 |
| Segunda copia / pérdida tolerable / recuperación | Propuesta abierta | Negocio + soporte definen D20; no compra implícita |
| Protocolo de prueba de E1 | Derivado A01-A06/A30 | Desarrollo convierte en guion ejecutable con datos ficticios |

Preparar E1 no obliga a aprobar toda D01-D24. Probar alternativas técnicas en laboratorio no equivale a elegir proveedor ni autorizar uso con datos reales.

## Primera revisión sugerida con el usuario

1. Vender una pieza ficticia: revisar orden de campos y resumen de pago.
2. Recibir un apartado y liquidarlo; comprobar que entrega es otro paso.
3. Recibir reparación, avanzar estado y revisar bloqueo económico al liquidar.
4. En administración, filtrar por sucursal y abrir detalle de cobro/orden.
5. Simular desconexión: caja/venta ordinaria disponibles, órdenes/saldo bloqueados.
6. Registrar cambios de pantallas y elegir modalidad de descuento. Después reunir información física para E1.

## Gestión del trabajo

Un solo registro de decisiones y versiones evita que una pantalla antigua gobierne reglas nuevas. Responsabilidades: negocio decide políticas/acepta experiencia; desarrollo diseña/implementa/verifica; soporte instala/prueba equipos; empleados ensayan. La revisión de seguridad/continuidad y la recuperación se repiten antes de la primera operación real. El cronograma se estima después de E1 con capacidad y volúmenes conocidos.
