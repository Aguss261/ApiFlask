from flask import Blueprint, request
from src.controller.userController import register, login

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def handle_register():
    return register()

@user_routes.route('/login', methods=['POST'])
def handle_login():
    return login()