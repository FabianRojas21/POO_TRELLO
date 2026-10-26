# Proyecto-TRELLO
PROYECTO TRELLO

## Actualizacion de la base de datos

El proyecto utiliza MySQL. Si ya ejecutaste `datos/sql/Borrado_logico.sql`, ejecuta
`datos/sql/Restauracion_papelera.sql` una sola vez para agregar los marcadores que
permiten restaurar listas y tarjetas sin recuperar elementos eliminados por separado.

Para habilitar el borrado logico de usuarios, etiquetas y comentarios en una base
existente, ejecuta una sola vez `datos/sql/Borrado_logico_entidades.sql`.

La aplicacion solicita inicio de sesion por ID de usuario y contrasena. En una base
existente sin la columna de contrasena, ejecuta una sola vez
`datos/sql/Autenticacion.sql`. La contrasena se guarda en texto plano solo como
solucion temporal para el proyecto de clase; no reutilices contrasenas reales.

La primera cuenta configurada se crea como jefe de proyecto. El jefe puede administrar
la aplicacion y crear usuarios con rol de jefe o trabajador. Los trabajadores solo
pueden consultar proyectos en los que participan y trabajar con sus tarjetas y comentarios.
