from schema import Schema, Or, Use, And, Optional

patientschema = Schema({
    Optional("nombre"):
        And(Use(str), error="Parámetro 'nombre' es inválido"),
    Optional("apellido_paterno"):
        And(Use(str), error="Parámetro 'apellido_paterno' es inválido"),
    Optional("apellido_materno"):
        And(Use(str), error="Parámetro 'apellido_materno' es inválido"),
    Optional("fecha_nacimiento"):
        And(Use(str), error="Parámetro 'fecha_nacimiento' es inválido"),
    Optional("genero"):
        And(Use(str), error="Parámetro 'genero' es inválido"),
    "curp":
        And(Use(str), error="Parámetro 'curp' es inválido"),
    Optional("email"):
        And(Use(str), error="Parámetro 'email' es inválido"),
    Optional("telefono"):
        And(Use(str), error="Parámetro 'telefono' es inválido"),
    Optional("ocupacion"):
        And(Use(str), error="Parámetro 'ocupación' es inválido"),
    Optional("estado_civil"):
        And(Use(str), error="Parámetro 'estado_civil' es inválido"),
    Optional("enfermedades_recientes"):
        And(Use(str), error="Parámetro 'enfermedades_recientes' es inválido"),
    Optional("medicamentos"):
        And(Use(str), error="Parámetro 'medicamentos' es inválido"),
    Optional("enfermedades_cronicas"):
        And(Use(list), error="Parámetro 'enfermedades_cronicas' es inválido"),
    Optional("enfermedades_hereditarias"):
        And(Use(str), error="Parámetro 'enfermedades_hereditarias' es inválido")
})