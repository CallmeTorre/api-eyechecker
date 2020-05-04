from datetime import datetime

from schema import Schema, Or, Use, And, Optional

patientschema = Schema({
    Optional("id"):
        Use(str, error="Parámetro 'id' es inválido"),
    Optional("nombre"):
        Use(str, error="Parámetro 'nombre' es inválido"),
    Optional("apellido_paterno"):
        Use(str, error="Parámetro 'apellido_paterno' es inválido"),
    Optional("apellido_materno"):
        Use(str, error="Parámetro 'apellido_materno' es inválido"),
    Optional("fecha_nacimiento"):
        Use(str, error="Parámetro 'fecha_nacimiento' es inválido"),
    Optional("email"):
        Use(str, error="Parámetro 'email' es inválido"),
    Optional("telefono_celular"):
        Use(str, error="Parámetro 'telefono_celular' es inválido"),
    Optional("genero"):
        Use(str, error="Parámetro 'genero' es inválido"),
    Optional("curp"):
        Use(str, error="Parámetro 'curp' es inválido"),
    Optional("ocupacion"):
        Use(str, error="Parámetro 'ocupación' es inválido"),
    Optional("estado_civil"):
        Use(str, error="Parámetro 'estado_civil' es inválido"),
    Optional("enfermedades_recientes"):
        Use(str, error="Parámetro 'enfermedades_recientes' es inválido"),
    Optional("medicamentos"):
        Use(str, error="Parámetro 'medicamentos' es inválido"),
    Optional("enfermedades_cronicas"):
        Use(list, error="Parámetro 'enfermedades_cronicas' es inválido"),
    Optional("enfermedades_hereditarias"):
        Use(str, error="Parámetro 'enfermedades_hereditarias' es inválido"),
    Optional("id_doctor"):
        Use(str, error="Parámetro 'id_doctor' es inválido")
})

doctorschema = Schema({
    Optional("id"):
        Use(str, error="Parámetro 'id' es inválido"),
    Optional("nombre"):
        Use(str, error="Parámetro 'nombre' es inválido"),
    Optional("apellido_paterno"):
        Use(str, error="Parámetro 'apellido_paterno' es inválido"),
    Optional("apellido_materno"):
        Use(str, error="Parámetro 'apellido_materno' es inválido"),
    Optional("fecha_nacimiento"):
        Use(str, error="Parámetro 'fecha_nacimiento' es inválido"),
    Optional("email"):
        Use(str, error="Parámetro 'email' es inválido"),
    Optional("telefono_celular"):
        Use(str, error="Parámetro 'telefono_celular' es inválido"),
    Optional("genero"):
        Use(str, error="Parámetro 'genero' es inválido"),
    Optional("organizacion"):
        Use(str, error="Parámetro 'organizacion' es inválido"),
    Optional("cedula"):
        Use(list, error="Parámetro 'cedula' es inválido"),
    Optional("horario"):
        Use(str, error="Parámetro 'horario' es inválido"),
    Optional("usuario"):
        Use(list, error="Parámetro 'usuario' es inválido"),
    Optional("password"):
        Use(str, error="Parámetro 'password' es inválido")
})

patientlistschema = Schema({
    "nombre":
        Use(str, error="Parámetro 'nombre' es inválido"),
    "curp":
        Use(str, error="Parámetro 'curp' es inválido"),
    "id_doctor":
       Use(str, error="Parámetro 'id_doctor' es inválido")
})

resetpasswordschema = Schema({
    "usuario":
        Use(str, error="Parámetro 'usuario' es inválido"),
    Optional("password"):
        Use(str, error="Parámetro 'password' es inválido")
})

analysisschema = Schema({
    "id":
        Use(str, error="Parámetro 'id' es inválido"),
    "id_medico":
        Use(str, error="Parámetro 'id_medico' es inválido")
}, ignore_extra_keys=True)

appointmentschema = Schema({
    Optional("id"):
        Use(str, error="Parámetro 'id' es inválido"),
    Optional("id_doctor"):
        Use(str, error="Parámetro 'id_doctor' es inválido"),
    Optional("id_paciente"):
        Use(str, error="Parámetro 'id_paciente' es inválido"),
    Optional("fecha_agendada"):
        And(Use(str),
            lambda xs: True if ((datetime.strptime(xs, '%Y-%m-%d %H:%M')) and (datetime.strptime(xs, '%Y-%m-%d %H:%M') > datetime.now())) else False,
            error="Parámetro 'fecha_agendada' es inválido"),
    Optional("fecha"):
        And(Use(str),
            error="Parámetro 'fecha' es inválido"),
    Optional("estado_cita"):
        Use(int, error="Parámetro 'estado_cita' es inválido")
})

loginschema = Schema({
    "usuario":
        Use(str, error="Parámetro 'usuario' es inválido"),
    "password":
        Use(str, error="Parámetro 'password' es inválido")
})

listanalysisschema = Schema({
    "id":
        Use(str, error="Parámetro 'id' es inválido"),
})

getanalysisschema = Schema({
    "url":
        Use(str, error="Parámetro 'url' es inválido"),
})

commentschema = Schema({
    "id_reporte":
        Use(str, error="Parámetro 'id_reporte' es inválido"),
    "comentario":
        Use(str, error="Parámetro 'comentario' es inválido")
})