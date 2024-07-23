from src.database.conexion import get_mysql_connection
from src.models.user import User
import mysql.connector
from mysql.connector import Error
import bcrypt


class UserService:
    def __init__(self):
        self.connection = get_mysql_connection()

    def create_user(self, username, email, password, direccion):
        try:
            cursor = self.connection.cursor()

            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insertar usuario en tabla usuario
            query = ("INSERT INTO usuario (username, email, password_hash, direccion) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (username, email, password_hash, direccion))
            self.connection.commit()

            user_id = cursor.lastrowid


            default_role_id = 9
            insert_query = ("INSERT INTO usuario_roles (usuario_id, rol_id) "
                            "VALUES (%s, %s)")
            cursor.execute(insert_query, (user_id, 9))
            self.connection.commit()

            cursor.close()
            return user_id

        except Error as e:
            print(f"Error al crear usuario: {e}")
            return None

    def get_user_by_username(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT u.id, u.username, u.email, u.password_hash, u.direccion, ur.rol_id
                FROM usuario u
                JOIN usuario_roles ur ON u.id = ur.usuario_id
                WHERE u.username = %s
            """
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                result['rol_id'] = result.pop('rol_id')
                return User(**result)
            return None
        except Error as e:
            print(f"Error al obtener usuario por nombre de usuario: {e}")
            return None
        finally:
            cursor.close()

    def get_user_by_id(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT u.*, ur.rol_id
                FROM usuario u
                JOIN usuario_roles ur ON u.id = ur.usuario_id
                WHERE u.id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return User(**result) if result else None
        except Error as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("La conexión MySQL está cerrada")
