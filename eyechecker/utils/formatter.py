def format_person(params):
    """
    Function that formats a person to be inserted in the database
    """
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
    """
    Function that formats a patient to be inserted in the database
    """
    return {
        'id_persona': params['id_persona'],
        'curp': params['curp'],
        'id_ocupacion': params['ocupacion'],
        'id_estado_civil': params['estado_civil'],
        'enfermedades_recientes': params['enfermedades_recientes'],
        'medicamentos': params['medicamentos'],
        'enfermedades_cronicas': params['enfermedades_cronicas'],
        'enfermedades_hereditarias': params['enfermedades_hereditarias'],
        'id_doctor': params['id_doctor']
    }


def format_doctor(params):
    """
    Function that formats a doctor to be inserted in the database
    """
    return {
        'id_persona': params['id_persona'],
        'organizacion': params['organizacion'],
        'cedula': params['cedula'],
        'horario': params['horario']
    }


def format_account(params):
    """
    Function that formats an account to be inserted in the database
    """
    return{
        'id_doctor': params['id_doctor'],
        'usuario': params['usuario'],
        'password': params['password']
    }


def format_eye_analysis(original, eye_key, micros, hemorrhages, exudates, conclusion):
    return {
        eye_key: {
            'original': original,
            'micros': micros,
            'hemorrhages':hemorrhages,
            'exudates': exudates,
            'conclusion': conclusion}}


def format_appointment(appointment):
    return {
        'id_cita': appointment.id,
        'id_paciente': appointment.id_paciente,
        'id_persona': appointment.id_persona,
        'estado_cita': appointment.estado_cita,
        'fecha_agendada': appointment.fecha_agendada.strftime('%Y-%m-%d'),
        'hora_agendada': appointment.fecha_agendada.strftime('%H:%M'),
        'nombre': appointment.nombre,
        'fecha_creacion': appointment.fecha_creacion.strftime('%Y-%m-%d')
    }


def format_appointments(appointments):
    return [format_appointment(appointment) for appointment in appointments]


def format_analysis(analysis):
    return [{'id': reporte.id, 
             'url': reporte.url_reporte, 
             'fecha_creacion': reporte.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
             'comentarios': reporte.comentarios} for reporte in analysis]