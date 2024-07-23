def verificar_campos_extra(data, campos_esperados):

    campos_extra = set(data.keys()) - campos_esperados
    if campos_extra:
        mensaje_error = f"Campos adicionales no permitidos: {', '.join(campos_extra)}"
        return False, mensaje_error
    return True, None


def verificar_campos_extra_nif(data, campos_esperados):
    campos_esperados_set = set(campos_esperados)

    campos_esperados_set = set(campos_esperados)
    campos_extra = set(data.keys()) - campos_esperados_set
    if campos_extra:
        mensaje_error = f"Campos adicionales no permitidos: {', '.join(campos_extra)}"
        return False, mensaje_error
    return True, None