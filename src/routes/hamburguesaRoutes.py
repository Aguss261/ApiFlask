from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.controller.hamburguesaController import get_hamburguesas, create_hamburguesa, delete_hamburguesa, \
    get_hamburguesa_by_id, editHamburguesa, get_hamburguesa_by_name, get_hamburguesa_by_price
from src.middleware.middleware_auth import admin_required, token_required

hamburguesas_routes = Blueprint("hamburguesa_routes", __name__)

@hamburguesas_routes.route("/hamburguesas", methods=["GET"])
def handle_getHamburguesas():
    return get_hamburguesas()

@hamburguesas_routes.route("/hamburguesas", methods=["POST"])
def handle_createHamburguesas():
    return create_hamburguesa()

@hamburguesas_routes.route("/hamburguesas/<int:id>", methods=["DELETE"])
def handle_deleteHamburguesas(id):
    return delete_hamburguesa(id)



@hamburguesas_routes.route("/hamburguesas/id/<int:id>", methods=["GET"])
def handle_getHamburguesasById(id):
    return get_hamburguesa_by_id(id)


@hamburguesas_routes.route("/hamburguesas/price/<float:price>", methods=["GET"])
@token_required
def handle_getHamburguesaByPrice(price):
    return get_hamburguesa_by_price(price)


@hamburguesas_routes.route("/hamburguesas/<int:id>", methods=["PUT"])
@admin_required
def handle_editHamburguesa(id):
    return editHamburguesa(id)


@hamburguesas_routes.route("/hamburguesas/nombre/<nombre>", methods=["GET"])
def handle_getHamburguesaByNombre(nombre):
    return get_hamburguesa_by_name(nombre)