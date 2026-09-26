# Flujo de cambios

1. Definir una tarea con resultado esperado y criterios de aceptación. Consultar `docs/e0/` y el plan de etapas.
2. Crear una rama corta desde `main` (`feat/`, `fix/`, `docs/`).
3. Implementar un cambio acotado. Validar permisos en el servidor y conservar la trazabilidad de operaciones monetarias e inventario.
4. Ejecutar las pruebas pertinentes. Para cambios de cálculo, persistencia o permisos, incluir casos de error y reintento; para interfaz, recorrer el flujo y comprobarlo visualmente.
5. Actualizar documentación cuando cambien reglas, instalación o uso.
6. Revisar `git diff --cached` y `git status` antes de confirmar: jamás incluir secretos, bases, respaldos ni datos de clientes.
7. Registrar un commit descriptivo, subir la rama y revisar la entrega antes de integrar.

## Terminado significa

Criterios de aceptación cumplidos, pruebas pertinentes aprobadas, revisión visual cuando corresponde, errores y límites documentados y aprobación del negocio para cambios de reglas. No declarar listo para producción un laboratorio solo por tener pruebas verdes.

Las tareas de mantenimiento que cambien datos deben tener alcance explícito y respaldo. No utilizar scripts de pruebas o simulación contra producción.
