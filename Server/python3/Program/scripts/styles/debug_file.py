def titulo_log(nombre_archivo, fecha_hora):
    """Genera un título con el nombre del archivo y la fecha/hora."""
    return f"=== {nombre_archivo} - {fecha_hora.strftime('%Y-%m-%d %H:%M:%S')} ===\n"

def separador_log():
    """Genera un separador bonito."""
    return "-" * 50

def formato_paso(paso):
    """Formatea el título de un paso."""
    return f"\nPaso {paso}:"

def formato_parametros(parametros):
    """Formatea los parámetros de una función."""
    return "  Parámetros:\n" + "\n".join([f"    {key}: {value}" for key, value in parametros.items()])

def formato_respuesta(respuesta):
    """Formatea la respuesta de una función."""
    return f"  Respuesta: {respuesta}"