import os

from flask import Flask
from flask_jwt_extended import JWTManager

from routes.userRoutes import user_routes
from routes.hamburguesaRoutes import hamburguesas_routes
from routes.pedidosRoutes import pedidos_routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')

jwt = JWTManager(app)

app.register_blueprint(user_routes, url_prefix='/api')
app.register_blueprint(hamburguesas_routes, url_prefix='/api/')
app.register_blueprint(pedidos_routes, url_prefix="/api/")

if __name__ == '__main__':
    app.run(debug=True)
