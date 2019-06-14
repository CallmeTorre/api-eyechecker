from schema import Schema, Or, Use, And, Optional

newpatientschema = Schema({
    "nombre":
        And(Use(str), error="Parametro 'nombre' es invalido"),
    Optional("segundo_nombre"):
        And(Use(str), error="Paramatro 'segundo_nombre' es invalido"),
    "apellido_paterno":
        And(Use(str), error="Parametro 'apellido_paterno' es invalido"),
    "apellido_materno":
        And(Use(str), error="Parametro 'apellido_materno' es invalido"),
    "edad":
        And(Use(int), error="Parametro 'edad' es invalido"),
    "sexo":
        And(Use(str), error="Parametro 'sexo' es invalido"),
    "email":
        And(Use(str), error="Parametro 'email' es invalido")
})


patientindexschema = Schema({
    "nombre":
        And(Use(str), error="Parametro 'nombre' es invalido"),
    "apellido_paterno":
        And(Use(str), error="Parametro 'apellido_paterno' es invalido"),
    "email":
        And(Use(str), error="Parametro 'email' es invalido"),
    "orderBy":
        And(Use(str), error="Parametro 'orderBy' es invalido")
})