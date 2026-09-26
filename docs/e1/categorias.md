# Categorías e informe — 26/09/2026

Inventario → Artículos / Categorías. Categorías lista la jerarquía, descripción y cantidad de artículos en cada rama. El formulario solicita nombre, categoría superior opcional y descripción opcional. Sin superior crea una categoría principal; se permiten dos niveles adicionales. Identificadores automáticos. Los nombres no se repiten dentro del mismo nivel y superior, ignorando mayúsculas. Requiere permiso de crear productos.

Persistencia PostgreSQL en categories de kv, enlazada con types para conservar los códigos de 15 dígitos. Las principales conservan el segmento de dos dígitos; máximo 99. Se recuperaron sub1/sub2 existentes sin alterar precios ni existencias. Los productos nuevos seleccionan una categoría del árbol; el servicio obtiene la principal y las subcategorías. Se sincroniza a cada POS.

Ventas por categoría incluye pastel por defecto y barras, leyenda con top cinco, importes y porcentajes, y Otras categorías cuando hay más de cinco. Total basado en ventas netas del filtro; estado vacío si no hay ventas. La tabla y CSV permanecen disponibles. El reporte agrupa por categoría principal.

Verificación: 24 pruebas de integración aprobadas, incluida creación de jerarquía, rechazo de duplicados/padre inexistente/cuarto nivel, permisos y alta de producto con categoría y sincronización. Revisión en navegador del pastel, selector de barras, navegación y formulario. Sin errores de consola observados.

## Edición y eliminación

Cada fila ofrece Editar y Eliminar a quienes tienen permiso de crear productos. Edición de nombre y descripción, con actualización de nombres de categoría en los artículos de la rama. La categoría superior se conserva. Los informes usan el catálogo vigente; los comprobantes originales no cambian.

Eliminación con confirmación dentro del módulo: una categoría con hijas requiere eliminarlas primero. Si tiene artículos, el usuario elige una categoría destino; el servicio reasigna en la misma transacción antes de borrar. Se incluyen artículos inactivos. Se conservan códigos, precios, existencias, ventas y movimientos. Las categorías principales eliminadas no reutilizan su identificador en altas posteriores. Auditoría de edición y eliminación. El backend comprueba permisos, duplicados y relaciones.

Prueba adicional: renombrar una principal actualiza su producto descendiente, eliminar una usada sin destino falla, eliminar una principal con hijas falla, reasignación conserva código y existencias, permisos y códigos no reutilizados. Formularios comprobados en navegador sin modificar categorías del usuario.
