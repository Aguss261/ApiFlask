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



def validar_hamburguesa(hamburguesas):
    required_fields = ["id", "nombre", "price", "descripcion", "imgUrl", "ingredientes"]
    ingredientes_fields = ["huevo", "lechuga", "tomate", "cebolla", "bacon", "pepino"]

    for hamburguesa in hamburguesas:

        if not all(field in hamburguesa for field in required_fields):
            missing_fields = [field for field in required_fields if field not in hamburguesa]
            print(f"Campos requeridos faltantes en hamburguesa: {missing_fields}")
            return False

        ingredientes = hamburguesa.get("ingredientes", {})
        if not all(field in ingredientes for field in ingredientes_fields):
            missing_ingredientes = [field for field in ingredientes_fields if field not in ingredientes]
            print(f"Campos de ingredientes faltantes en hamburguesa: {missing_ingredientes}")
            return False

    return True