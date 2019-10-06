def format_person(params):
    return {
        'nombre': params['nombre'],
        'apellido_paterno': params['apellido_paterno'],
        'apellido_materno': params['apellido_materno'],
        'fecha_nacimiento': params['fecha_nacimiento'],
        'email': params['email'],
        'telefono_celular': params['telefono_celular'],
        'genero': params['genero']
    }


def format_patient(params):
    return {
        'id_persona': params['id_persona'],
        'curp': params['curp'],
        'id_ocupacion': params['ocupacion'],
        'id_estado_civil': params['estado_civil'],
        'enfermedades_recientes': params['enfermedades_recientes'],
        'medicamentos': params['medicamentos'],
        'enfermedades_cronicas': params['enfermedades_cronicas'],
        'enfermedades_hereditarias': params['enfermedades_hereditarias']
    }


def format_doctor(params):
    return {
        'id_persona': params['id_persona'],
        'organizacion': params['organizacion'],
        'cedula': params['cedula'],
        'horario': params['horario']
    }


def format_account(params):
    return{
        'id_persona': params['id_doctor'],
        'usuario': params['usuario'],
        'password': params['password']
    }