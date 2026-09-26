# Etapa E0 · Diseño de Frida Blancas México

> Actualización 25/09/2026: el usuario revisó y aceptó los recorridos de E0. Las decisiones posteriores y el laboratorio están en [E1](../e1/README.md). El texto siguiente conserva la situación de entrega original de E0.

Versión 1.0, 23/09/2026. Base: requisitos v2 de 18/09/2026 y plan de desarrollo v1.

**Estado: entregables preparados para revisión del negocio.** E0 no equivale a autorización de E1 ni a un POS operativo. Los acuerdos confirmados del PDF se conservan; las elecciones pendientes siguen abiertas. La primera sustitución mantiene TODOS los módulos del plan.

## Qué revisar primero

1. Abrir [el prototipo navegable](../../prototype/e0/index.html). Elegir Administración o Punto de venta. La franja superior identifica siempre los datos ficticios. Se puede reiniciar la demostración.
2. Leer [flujos, estados y pantallas](02-flujos-y-pantallas.md). Revisar especialmente liquidación/entrega, correcciones y operación desconectada.
3. Revisar [indicadores y decisiones](03-reglas-y-decisiones.md). Contiene alternativas, recomendaciones explícitamente propuestas y ejemplos; no presupone aprobación del usuario.
4. Consultar [modelo de datos y contratos](04-modelo-y-contratos.md) y [revisión técnica de la base existente](05-revision-prototipo.md).
5. Usar [matriz por identificador](01-matriz-requisitos.md) y [tareas ordenadas](06-tareas-y-puerta-e1.md) para continuar el desarrollo.

## Entregables E0

| Plan | Resultado | Estado |
| --- | --- | --- |
| E0.1 | Matriz con texto de cada requisito, página, pantalla, tarea, dependencias, decisión y pruebas A01-A30; datos reutilizables en requisitos.json | Preparado; cobertura verificada automáticamente |
| E0.2 | Flujos normales, excepciones, estados y prohibiciones de venta, caja, órdenes, cambios y correcciones | Diseñado; revisión del negocio pendiente |
| E0.3 | Diccionario de indicadores, ejemplos numéricos y registro de D01-D24 con propuestas | Reglas base documentadas; propuestas no aprobadas |
| E0.4 | Modelo lógico, relaciones, invariantes, transacciones y contrato de sincronización propuesto | Diseño; sin migraciones aplicadas |
| E0.5 | Prototipo POS/dashboard con venta, caja, apartados, reparaciones, filtros y detalle | Navegable; simulación en memoria |
| E0.6 | Revisión estática del esquema, funciones, pruebas y utilidades existentes | Terminada en alcance estático; no prueba dinámica de PostgreSQL |

## Qué demuestra el prototipo

La organización de pantallas, navegación lateral, filtros, tarjetas, gráfica, tablas y panel de detalle; separación entre administración y POS; diferencia entre venta/cobro/entrega; flujo de carrito, pago y caja; ciclo básico de órdenes y avisos por desconexión simulada. Se prueban ejemplos con importes simples, sin redondeos ambiguos.

No hay autenticación real, permisos fiables, base de datos, persistencia, terminal bancaria, sincronización entre computadoras ni impresión física. Los roles son modos de demostración. Cerrar/recargar restablece los datos; el interruptor de internet solo simula restricciones visuales. El código del prototipo es desechable como base de producción: sirve de referencia de experiencia, no de prueba de E1.

## Cómo abrirlo

Puede abrirse directamente `prototype/e0/index.html`, sin instalar paquetes. Para la vista en navegador local: `python3 -m http.server 8765 --bind 127.0.0.1 --directory prototype/e0` desde la raíz del proyecto. Solo expone la carpeta de la demostración al equipo local. No publicar toda la raíz del proyecto, que contiene respaldos y configuración.

## Fuentes y seguimiento

- Fuente funcional: `output/pdf/Requerimientos_POS_Frida_Blancas_Mexico_v2.pdf`, 40 páginas. La matriz conserva los identificadores agrupados tal como están impresos; no inventa IDs omitidos.
- Fuente de etapas y pruebas: `docs/Plan_desarrollo_POS_Frida_Blancas_v1.md`.
- Código revisado: migraciones 001-003, `database/manage.py`, pruebas de base/restauración, README y modelo v0.1. Los archivos existentes y sus datos no se cambiaron.
- Control de cambios: estos nuevos archivos constituyen E0 v1.0. Futuras decisiones deben añadir fecha y autor en `03-reglas-y-decisiones.md` y regenerar lo afectado. No se realizó commit ni se configuró un repositorio remoto.
- Validación entregada: [reporte de verificación](07-verificacion.md). Distingue cobertura documental, pruebas del prototipo y lo que exige equipos reales.

**Puerta G0:** pendiente de revisar pantallas y decidir los puntos iniciales listados en `06-tareas-y-puerta-e1.md`. El desarrollo independiente puede continuar; los módulos afectados por una decisión abierta no deben considerarla aprobada por omisión.
