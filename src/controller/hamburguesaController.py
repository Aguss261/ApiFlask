import json

import mysql
from flask import Blueprint, request, jsonify

from src.service.hamburguesaService import HamburguesaService

hamburguesa_service = HamburguesaService()


def get_hamburguesas():
    try:
        devolver = hamburguesa_service.getAllHamburguesas()
        if devolver is None:
            return jsonify({"Error": "Error buscando las hamburguesas"}), 500
        return jsonify(devolver), 200
    except Exception as e:
        print(f"Error en la API al obtener las hamburguesas: {str(e)}")
        return jsonify({"Error": "Error interno al obtener las hamburguesas"}), 500


def create_hamburguesa():
    data = request.json


    campos_esperados = ["nombre", "price", "descripcion", "imgUrl", "ingredientes"]

    es_valido, mensaje_error = verificar_campos_extra(data, campos_esperados)

    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    nombre = data.get('nombre')
    price = data.get('price')
    descripcion = data.get('descripcion')
    imgUrl = data.get('imgUrl')
    ingredientes = data.get('ingredientes')

    if not nombre or not price or not descripcion or not imgUrl or not ingredientes:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    success, result = hamburguesa_service.create_hamburguesa(nombre, price, descripcion, imgUrl, ingredientes)

    if success:
        return jsonify({"message": "Hamburguesa agregada correctamente"}), 201
    else:
        return jsonify({"error": "No se pudo agregar la hamburguesa"}), 500






def editHamburguesa(id):
    data = request.json

    if not data:
        return jsonify({"Error": "No hay Data"}), 400

    nombre = data.get('nombre')
    price = data.get('price')
    descripcion = data.get('descripcion')
    imgUrl = data.get('imgUrl')
    ingredientes = data.get('ingredientes')

    result = hamburguesa_service.edit_hamburguesa(id, nombre, price, descripcion, imgUrl, ingredientes)

    if result:
        return jsonify({"message": "Hamburguesa editada correctamente"}), 202
    else:
        return jsonify({"error": "No se pudo editar correctamente la hamburguesa"}), 500


def delete_hamburguesa(id):
    if not isinstance(id,int) or id <= 0:
        return jsonify({"error": "invalidad ID"}), 400

    devolver = hamburguesa_service.delete_hamburguesa(id)

    if "error" in devolver:
        return jsonify(devolver), 400
    return jsonify(devolver), 200


def get_hamburguesa_by_id(id):
    if not isinstance(id,int) or id <= 0:
        return jsonify({"error": "invalidad ID"}), 400

    try:
        # Llamada al servicio para obtener la hamburguesa
        devolver = hamburguesa_service.get_hamburguesa_by_id(id)

        # Verificación del resultado devuelto por el servicio
        if "error" in devolver:
            return jsonify(devolver), 404  # Cambiado a 404 para 'no encontrado'
        return jsonify(devolver), 200

    except Exception as e:
        # Manejo de excepciones no esperadas
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


def get_hamburguesa_by_price(price):
    if not isinstance(price, (int,float)) or price <= 0:
        return jsonify({"error": "precio invalido"}), 400

    try:
        devolver = hamburguesa_service.get_hamburguesa_by_price(price)

        # Verificación del resultado devuelto por el servicio
        if "error" in devolver:
            return jsonify(devolver), 404  # Cambiado a 404 para 'no encontrado'
        return jsonify(devolver), 200

    except Exception as e:
        # Manejo de excepciones no esperadas
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



def get_hamburguesa_by_name(nombre):
    if not isinstance(nombre,str):
        return jsonify({"error": "nombre invalido"}), 400

    try:
        devolver = hamburguesa_service.get_hamburguesa_by_name(nombre)

        if "error" in devolver:
            return jsonify(devolver), 404
        return jsonify(devolver), 200

    except IndexError as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Internal server Error"}), 500


def verificar_campos_extra(data, campos_esperados):
    campos_esperados_set = set(campos_esperados)

    campos_esperados_set = set(campos_esperados)
    campos_extra = set(data.keys()) - campos_esperados_set
    if campos_extra:
        mensaje_error = f"Campos adicionales no permitidos: {', '.join(campos_extra)}"
        return False, mensaje_error
    return True, None