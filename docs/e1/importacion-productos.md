# Importación de productos nuevos

Disponible en Administración > Artículos y en ambas sucursales > Inventario, con conexión y permisos `inventory_view` y `product_create`. En sucursal se mantiene el requisito de caja abierta para acceder a las operaciones.

Plantilla: https://docs.google.com/spreadsheets/d/1tGStyA0-kjpxpGFFLD01Lf4iDzMoy0v1v6L4Sux4dXo/edit

1. Copiar la plantilla, llenar una fila por producto nuevo (todas las filas con datos se importan; las vacías se omiten).
2. Descargar como Microsoft Excel (.xlsx). Conservar la hoja Productos y sus encabezados. También se admite CSV UTF-8 y TSV con las mismas columnas.
3. Seleccionar Importar productos nuevos y escribir una referencia única de recepción.
4. Revisar los productos, unidades y errores antes de confirmar.

La carga crea productos y sus existencias iniciales; no repone existencias de productos anteriores. Los códigos se asignan al confirmar. Las imágenes se pueden añadir posteriormente desde Editar producto en Administración.

Límites: 500 filas, 450 KB; valores sin fórmulas de celdas de Excel; ambas descripciones obligatorias. Material, categoría, proveedor y almacén se resuelven contra los catálogos vigentes. Las opciones de la plantilla reflejan el catálogo al crearla.

Toda la recepción se confirma en una transacción: un error impide el guardado parcial. Se detectan productos repetidos. Repetir la misma referencia y contenido, incluso desde otra sucursal, devuelve el ingreso previo sin duplicarlo. No hay sincronización automática con Google Sheets; se importa el archivo descargado.

Verificación: `lab/e1/.venv/bin/python -m unittest discover -s lab/e1/tests -p test_inventory_import.py`. Pruebas sobre base desechable: validación, rollback, concurrencia, idempotencia, permisos, Excel exportado de Google y HTTP desde Administración y ambas sucursales.

## Precio fijo o por fórmula

La columna Importar se eliminó. Todas las filas con datos se validan e importan; las vacías se omiten.

Las columnas Tipo de precio, Base de cálculo, Multiplicador y Terminación permiten guardar una regla propia por producto. En Fijo, se llena Precio de venta y se dejan vacías las otras tres columnas. En Fórmula, Precio de venta puede quedar vacío: el servidor calcula la vista previa y recalcula al confirmar.

- Costo: costo unitario × multiplicador, por ejemplo 300 × 2.77 = 831.
- Peso: peso en gramos × multiplicador (precio por gramo).
- Terminación 50: menor precio terminado en 50 que no sea inferior al resultado (831 → 850; 850 → 850; 850.01 → 950).
- Terminación 90: misma regla (831 → 890; 891 → 990).
- Sin redondeo: se redondea a centavos.

Precio en etiqueta es independiente. La regla se guarda en `price_mode` y `price_rule` del producto y se puede editar en Administración. Se recalcula al editar costo, peso o regla; no cambia comprobantes de ventas anteriores. No hay un precio por gramo global ni actualización automática de cotizaciones. Las fórmulas son parámetros del producto, no código ejecutable ni referencias a celdas.


## Proveedores y fechas

Inventario → Proveedores permite al administrador listar, registrar, editar y habilitar o deshabilitar proveedores desde el dashboard. Habilitado equivale a aprobado para nuevas asignaciones. Los proveedores existentes se consideran habilitados. Crear, reasignar e importar artículos valida el catálogo vigente de proveedores habilitados en el servidor. Deshabilitar uno conserva sus artículos e historial; se permiten otras ediciones de esos artículos sin reasignarlo. Las sucursales pueden seleccionar proveedores habilitados, pero no administrar el catálogo.

El catálogo muestra fecha de carga y última actividad. Editar producto también muestra última edición de datos y último movimiento. Las fechas se derivan del historial persistente de auditoría y movimientos confirmados: altas manuales/importadas, ediciones, ventas, cancelaciones y entradas. Los reintentos no cambian las fechas. No se inventan fechas para artículos antiguos sin registro. En una sucursal sin conexión, las fechas disponibles corresponden a la última sincronización.

Pruebas adicionales: `lab/e1/.venv/bin/python -m unittest discover -s lab/e1/tests -p test_product_metadata.py`.

## Mercancía recurrente

El botón Mercancía recurrente abre una lista de artículos existentes. Busca por descripción corta, larga o código, añade productos y captura cantidades, almacén y referencia. Las coincidencias aparecen únicamente al buscar y se limitan a 20 por consulta. Añadir de nuevo un artículo aumenta su cantidad en la misma fila.

El borrador se guarda automáticamente en localStorage, separado por identificador de usuario y punto de acceso. Sobrevive a cerrar sesión, recargar o cerrar el navegador en ese perfil. No se comparte entre equipos; borrar los datos del navegador borra el borrador. No se modifican existencias hasta revisar y confirmar.

La confirmación requiere conexión y permisos de inventario y creación/ingreso de mercancía, también desde ambas sucursales. Hasta 500 productos se registran en una transacción, sin cambios de código, precio o costo. Una fila inválida revierte todo el ingreso. El identificador persistido permite reintentar una petición de resultado desconocido sin duplicar unidades; mientras está pendiente, la lista queda bloqueada para preservar el contenido del reintento.

Pruebas: `lab/e1/.venv/bin/python -m unittest discover -s lab/e1/tests -p test_recurrent_inventory.py`.
