from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.controller.pedidosController import get_pedidos, create_pedido, get_pedidos_by_id, get_pedidos_by_user_id, \
        get_pedidos_by_fecha, get_pedidos_by_user, delete_pedido, edit_pedido

from src.middleware.middleware_auth import admin_required, token_required

pedidos_routes = Blueprint("pedidos_routes", __name__)


@pedidos_routes.route("/pedidos", methods=["GET"])
@admin_required
def handle_getPedidos():
    return get_pedidos()


@pedidos_routes.route("/pedidos", methods=["POST"])
@jwt_required()
def handle_createPedido():
    return create_pedido()

@pedidos_routes.route("/pedidos/id/<int:id>", methods=["GET"])
def handle_getPedidoById(id):
    return get_pedidos_by_id(id)

@pedidos_routes.route("/pedidos/user", methods=["GET"])
@jwt_required()
def handle_getPedidoByUserJwt():
    return get_pedidos_by_user()



@pedidos_routes.route("/pedidos/user/<int:id>", methods=["GET"])
def handle_getPedidoByUser(id):
    return get_pedidos_by_user_id(id)


@pedidos_routes.route("/pedidos/fecha/<fecha>", methods=["GET"])
def handle_getPedidoByFecha(fecha):
    return get_pedidos_by_fecha(fecha)

@pedidos_routes.route("/pedidos/<int:id>", methods=["DELETE"])
def handle_deletePedido(id):
    return delete_pedido(id)


@pedidos_routes.route("/pedidos/<int:id>", methods=["PUT"])
@jwt_required()
def handle_editPedido(id):
    return edit_pedido(id)