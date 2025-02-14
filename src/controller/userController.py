import bcrypt
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from src.service.userService import UserService
from src.utils.jwt_utils import generate_token
from src.utils.validator_body import verificar_campos_extra_nif

user_service = UserService()

def register():
    data = request.get_json()

    campos_esperados = ["username", "email", "password", "direccion"]

    es_valido, mensaje_error = verificar_campos_extra_nif(data, campos_esperados)

    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    direccion = data.get('direccion')


    if not username or not password or not password or not direccion:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    if user_service.get_user_by_username(username):
        return jsonify({'message': 'El usuario ya existe elija otro Username'}), 400

    user_id = user_service.create_user(username, email, password, direccion)
    if user_id:
        token = generate_token(user_id)
        return jsonify({'token': token}), 201
    return jsonify({'message': 'Error al crear el usuario'}), 500

def login():
    data = request.get_json()

    campos_esperados = ["username", "password"]

    es_valido, mensaje_error = verificar_campos_extra_nif(data, campos_esperados)

    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password :
        return jsonify({"error": "Faltan datos requeridos"}), 400

    user = user_service.get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Credenciales invalidas'}), 401



def get_users():
    try:
        usuarios = user_service.get_users()
        if usuarios is None:
            return jsonify({"Error": "Error buscando los usuarios"}), 500
        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Error en la API al obtener los usuarios: {str(e)}")
        return jsonify({"Error": "Error interno al obtener los usuarios"}), 500



#lo busco atraves del jwt
def get_user_by_jwt():

    try:
        user_id = get_jwt_identity()
        if user_id is None:
            return jsonify({"Error": "Id Inexsistente"}), 500
        devolver = user_service.get_user_by_id(user_id)
        if devolver is None:
            return jsonify({"Error": "Error buscando el usuario"}), 500
        return jsonify(devolver), 200
    except Exception as e:
        print(f"Error en la API al obtener el usuario: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el usuario"}), 500



def get_user_by_id(user_id):

    try:
        if user_id is None:
            return jsonify({"Error": "Id Inexsistente"}), 500
        devolver = user_service.get_user_by_id(user_id)
        if devolver is None:
            return jsonify({"Error": "Error no existe un usuario con esa ID"}), 500
        return jsonify(devolver.to_dict()), 200
    except Exception as e:
        print(f"Error en la API al obtener el usuario: {str(e)}")
        return jsonify({"Error": "Error interno al obtener el usuario"}), 500

