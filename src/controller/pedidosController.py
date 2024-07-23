import datetime
import json

import jwt
import mysql
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from src.utils.validator_body import verificar_campos_extra

from src.service.pedidosService import PedidosService

pedidos_service = PedidosService()

def get_pedidos():
    try:
        pedidos = pedidos_service.getAllPedidos()
        if pedidos is None:
            return jsonify({"Error": "Error buscando los pedidos"}), 500
        return jsonify(pedidos), 200
    except Exception as e:
        print(f"Error en la API al obtener los pedidos: {str(e)}")
        return jsonify({"Error": "Error interno al obtener los pedidos"}), 500


def get_pedidos_by_id(id):

    if not isinstance(id,int) or id <= 0:
        return jsonify({"error": "invalidad ID"}), 400
    try:
        pedido = pedidos_service.get_pedido_by_id(id)
        if pedido is None:
            return jsonify({"Error": "Error buscando el pedido"}), 500
        return jsonify(pedido), 200
    except Exception as e:
        print(f"Error en la API al obtener el pedido: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el pedido"}), 500


def get_pedidos_by_user_id(user_id):

    if not isinstance(user_id,int) or user_id <= 0:
        return jsonify({"Error": "invalidad ID"}), 400

    try:
        pedido = pedidos_service.get_pedido_by_user_id(user_id)
        if pedido is None:
            return jsonify({"Error": "Error buscando el pedido"}), 500
        return jsonify(pedido), 200
    except Exception as e:
        print(f"Error en la API al obtener el pedido: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el pedido"}), 500


def get_pedidos_by_fecha(fecha):


    try:
        pedido = pedidos_service.get_pedido_by_fecha(fecha)
        if pedido is None:
            return jsonify({"Error": "Error buscando el pedido"}), 500
        return jsonify(pedido), 200
    except Exception as e:
        print(f"Error en la API al obtener el pedido: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el pedido"}), 500


def get_pedidos_by_user():

    try:
        user_id = get_jwt_identity()
        if user_id is None:
            return jsonify({"Error": "Id Inexsistente"}), 500
        pedido = pedidos_service.get_pedido_by_user(user_id)
        if pedido is None:
            return jsonify({"Error": "Error buscando el pedido"}), 500
        return jsonify(pedido), 200
    except Exception as e:
        print(f"Error en la API al obtener el pedido: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el pedido"}), 500


def create_pedido():
    data = request.get_json()

    campos_esperados = {"direccion", "hamburguesas", "price"}

    es_valido, mensaje_error = verificar_campos_extra(data, campos_esperados)
    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    direccion = data.get("direccion")
    hamburguesas_json = data.get("hamburguesas")

    if not direccion or not isinstance(hamburguesas_json, list) or not hamburguesas_json:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    user_id = get_jwt_identity()

    success, result = pedidos_service.create_pedido(user_id, direccion, hamburguesas_json)

    if success:
        return jsonify(result), 201
    else:
        return jsonify(result), 500


def delete_pedido(pedido_id):
    if not isinstance(pedido_id,int) or pedido_id <= 0:
        return jsonify({"error": "invalidad ID"}), 400

    devolver = pedidos_service.delete_pedido(pedido_id)

    if "error" in devolver:
        return jsonify(devolver), 400
    return jsonify(devolver), 200


def edit_pedido(pedido_id):
    data = request.get_json()

    campos_esperados = {"direccion", "hamburguesas", "price"}

    es_valido, mensaje_error = verificar_campos_extra(data, campos_esperados)
    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    direccion = data.get("direccion")
    hamburguesas = data.get("hamburguesas")


    if not direccion or not isinstance(hamburguesas, list) or not hamburguesas:
        return jsonify({"error": "El campo 'Faltan datos requeridos"}), 400

    user_id = get_jwt_identity()

    success, result = pedidos_service.edit_pedido(pedido_id,user_id, direccion, hamburguesas)

    if success:
        return jsonify(result), 201
    else:
        return jsonify(result), 500



def obtenerPriceTotal(hamburguesas):
    total = 0
    if isinstance(hamburguesas, list):
        for hamburguesa in hamburguesas:
            total += hamburguesa.get("price", 0)
    elif isinstance(hamburguesas, dict):
        total += hamburguesas.get("price", 0)
    return total



