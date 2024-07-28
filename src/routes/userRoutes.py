from flask import Blueprint
from flask_jwt_extended import jwt_required


from src.controller.userController import register, login, get_users, get_user_by_jwt, get_user_by_id
from src.middleware.middleware_auth import admin_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def handle_register():
    return register()

@user_routes.route('/login', methods=['POST'])
def handle_login():
    return login()


@user_routes.route('/usuarios', methods=['GET'])
def handle_getUsers():
    return get_users()


@user_routes.route('/usuario', methods=['GET'])
@jwt_required()
def handle_getUsers_by_jwt():
    return get_user_by_jwt()


@user_routes.route('/usuario/<int:id>', methods=['GET'])
@admin_required
def handle_getUsers_by_id(id):
    return get_user_by_id(id)