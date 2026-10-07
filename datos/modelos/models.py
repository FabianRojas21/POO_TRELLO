from peewee import *
from datos.conexion import conectar


Database = conectar()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = Database

class Proyecto(BaseModel):
    codigo_proyecto = CharField(max_length=20, unique=True)
    fecha_fin = DateField(null=True)
    fecha_inicio = DateField()
    id_proyecto = AutoField()
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'PROYECTO'

class Tablero(BaseModel):
    fecha_creacion = DateField(constraints=[SQL("DEFAULT curdate()")])
    id_proyecto = ForeignKeyField(column_name='id_proyecto', field='id_proyecto', model=Proyecto, on_delete='CASCADE', unique=True)
    id_tablero = AutoField()
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'TABLERO'

class Lista(BaseModel):
    id_lista = AutoField()
    id_tablero = ForeignKeyField(column_name='id_tablero', field='id_tablero', model=Tablero, on_delete='CASCADE')
    nombre = CharField(max_length=100)
    orden = IntegerField()

    class Meta:
        table_name = 'LISTA'

class Tarjeta(BaseModel):
    descripcion = TextField(null=True)
    estado = CharField(constraints=[SQL("DEFAULT 'pendiente'")], max_length=50)
    fecha_limite = DateField(null=True)
    id_lista = ForeignKeyField(column_name='id_lista', field='id_lista', model=Lista, on_delete='CASCADE')
    id_tarjeta = AutoField()
    titulo = CharField(max_length=150)

    class Meta:
        table_name = 'TARJETA'

class Usuario(BaseModel):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    rol = CharField(max_length=50)

    class Meta:
        table_name = 'USUARIO'

class AsignacionTarjeta(BaseModel):
    id_tarjeta = ForeignKeyField(column_name='id_tarjeta', field='id_tarjeta', model=Tarjeta, on_delete='CASCADE')
    id_usuario = ForeignKeyField(column_name='id_usuario', field='id_usuario', model=Usuario, on_delete='CASCADE')

    class Meta:
        table_name = 'ASIGNACION_TARJETA'
        indexes = (
            (('id_tarjeta', 'id_usuario'), True),
        )
        primary_key = CompositeKey('id_tarjeta', 'id_usuario')

class Comentario(BaseModel):
    fecha = DateField(constraints=[SQL("DEFAULT curdate()")])
    id_comentario = AutoField()
    id_tarjeta = ForeignKeyField(column_name='id_tarjeta', field='id_tarjeta', model=Tarjeta, on_delete='CASCADE')
    id_usuario = ForeignKeyField(column_name='id_usuario', field='id_usuario', model=Usuario, on_delete='CASCADE')
    texto = TextField()

    class Meta:
        table_name = 'COMENTARIO'

class Etiqueta(BaseModel):
    color = CharField(max_length=20)
    id_etiqueta = AutoField()
    nombre = CharField(max_length=50)

    class Meta:
        table_name = 'ETIQUETA'

class ProyectoUsuario(BaseModel):
    id_proyecto = ForeignKeyField(column_name='id_proyecto', field='id_proyecto', model=Proyecto, on_delete='CASCADE')
    id_usuario = ForeignKeyField(column_name='id_usuario', field='id_usuario', model=Usuario, on_delete='CASCADE')

    class Meta:
        table_name = 'PROYECTO_USUARIO'
        indexes = (
            (('id_proyecto', 'id_usuario'), True),
        )
        primary_key = CompositeKey('id_proyecto', 'id_usuario')

class TarjetaEtiqueta(BaseModel):
    id_etiqueta = ForeignKeyField(column_name='id_etiqueta', field='id_etiqueta', model=Etiqueta, on_delete='CASCADE')
    id_tarjeta = ForeignKeyField(column_name='id_tarjeta', field='id_tarjeta', model=Tarjeta, on_delete='CASCADE')

    class Meta:
        table_name = 'TARJETA_ETIQUETA'
        indexes = (
            (('id_tarjeta', 'id_etiqueta'), True),
        )
        primary_key = CompositeKey('id_tarjeta', 'id_etiqueta')

