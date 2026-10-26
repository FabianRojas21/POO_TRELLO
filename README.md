# Proyecto-TRELLO
PROYECTO TRELLO

## Actualizacion de la base de datos

El proyecto utiliza MySQL. Si ya ejecutaste `datos/sql/Borrado_logico.sql`, ejecuta
`datos/sql/Restauracion_papelera.sql` una sola vez para agregar los marcadores que
permiten restaurar listas y tarjetas sin recuperar elementos eliminados por separado.

Para habilitar el borrado logico de usuarios, etiquetas y comentarios en una base
existente, ejecuta una sola vez `datos/sql/Borrado_logico_entidades.sql`.
