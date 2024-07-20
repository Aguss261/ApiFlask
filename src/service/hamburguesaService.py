import json

from MySQLdb import MySQLError
from flask import jsonify

from src.database.conexion import get_mysql_connection
from src.models.hamburguesa import Hamburguesa
import mysql.connector


class HamburguesaService:
    def __init__(self):
        self.connection = get_mysql_connection()

    def getAllHamburguesas(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * from Hamburguesa"
            cursor.execute(sql_query)
            devolver = cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error buscando las hamburguesas: {error}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
        return devolver


    def create_hamburguesa(self, nombre, price, descripcion, imgUrl, ingredientes):
        if not self.validar_ingredientes(ingredientes):
            return False, {"error": "Ingredientes inválidos"}

        try:
            cursor = self.connection.cursor()
            sql_query = "INSERT INTO hamburguesa (nombre, price, descripcion, imgUrl, ingredientes) VALUES (%s, %s, %s, %s, %s)"
            ingredientes_json = json.dumps(ingredientes)  # Convertir dict a JSON string
            cursor.execute(sql_query, (nombre, price, descripcion, imgUrl, ingredientes_json))
            self.connection.commit()

            if cursor.rowcount > 0:
                return True, {"message": "Hamburguesa creada correctamente"}
            else:
                return False, {"error": "No se pudo crear la hamburguesa"}

        except mysql.connector.Error as error:
            print(f"Error al agregar la hamburguesa: {error}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def delete_hamburguesa(self, id):
        try:

            cursor = self.connection.cursor()
            sql_query = "DELETE FROM hamburguesa WHERE id = %s"
            cursor.execute(sql_query, (id,))
            self.connection.commit()
            if cursor.rowcount == 0:
                cursor.close()
                return {"error": "Hamburguesa no encontrada"}, 404
            cursor.close()
            return {"Mensaje": "Hamburguesa eliminada con exito"}
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}

    def get_hamburguesa_by_id(self, id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * FROM hamburguesa WHERE id = %s"
            cursor.execute(sql_query, (id,))
            devolver = cursor.fetchone()
            if devolver is None:
                return {"error": "Hamburguesa no encontrada"}, 404
            return devolver
        except mysql.connector.Error as error:
            print(f"Error buscando la hamburguesa: {error}")
            return {"error": "Error interno del servidor"}, 500
        finally:
            if cursor is not None:
                cursor.close()

    def get_hamburguesa_by_name(self, nombre):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * FROM hamburguesa WHERE nombre LIKE %s"
            like_pattern = f"%{nombre}%"
            cursor.execute(sql_query, (like_pattern,))
            devolver = cursor.fetchall()
            if devolver is None:
                return {"error": "Hamburguesa no encontrada"}, 404
            return devolver
        except mysql.connector.Error as error:
            print(f"Error buscando la hamburguesa: {error}")
            return {"error": "Error interno del servidor"}, 500
        finally:
            if cursor is not None:
                cursor.close()


    def get_hamburguesa_by_price(self, price):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * FROM hamburguesa where price < %s"
            cursor.execute(sql_query, (price,))
            devolver = cursor.fetchall()

            if not devolver:
                return {"error": "No existen hamburguesas por menos de ese precio"}, 404

            return devolver

        except mysql.connector.Error as error:
            print(f"Error buscando la hamburguesa: {error}")
            return {"error": "Error interno del servidor"}, 500
        finally:
            if cursor is not None:
                cursor.close()


    def edit_hamburguesa(self, id, nombre, price, descripcion, imgUrl, ingredientes):
        cursor = None  # Inicializar el cursor fuera del bloque try
        try:
            error, is_valid = self.validar_hamburguesa(id, nombre, price, descripcion, imgUrl, ingredientes)
            if not is_valid:
                return False

            cursor = self.connection.cursor()
            sql_query = """
                        UPDATE hamburguesa
                        SET nombre = %s, price = %s, descripcion = %s, imgUrl = %s, ingredientes = %s
                        WHERE id = %s
                    """
            cursor.execute(sql_query, (nombre, price, descripcion, imgUrl, json.dumps(ingredientes), id))
            self.connection.commit()

            if cursor.rowcount == 0:
                return False

            return True

        except MySQLError as error:
            print(f"Error actualizando la hamburguesa: {error}")
            return False

        finally:
            if cursor:
                cursor.close()

    def validar_ingredientes(self, ingredientes):
        required_fields = ["bacon", "huevo", "pepino", "tomate", "cebolla", "lechuga"]

        # Verificar si todos los ingredientes requeridos están presentes
        for field in required_fields:
            if field not in ingredientes:
                return False

        # Verificar si hay ingredientes adicionales no permitidos
        for field in ingredientes:
            if field not in required_fields:
                return False

        return True

    def validar_hamburguesa(self, id, nombre, price, descripcion, imgUrl, ingredientes):
        if not isinstance(id, int) or id <= 0:
            return {"error": "Id invalida"}, False
        if not isinstance(nombre, str) or not nombre:
            return {"error": "Nombre invalido"}, False
        if not isinstance(price, (int, float)) or price <= 0:
            return {"error": "Precio invalido"}, False
        if not isinstance(descripcion, str) or not descripcion:
            return {"error": "Descripcion invalida"}, False
        if not isinstance(imgUrl, str) or not imgUrl:
            return {"error": "Imagen url invalida"}, False

        required_keys = ["bacon", "huevo", "pepino", "tomate", "cebolla", "lechuga"]
        if not isinstance(ingredientes, dict) or not all(key in ingredientes for key in required_keys):
            return {"error": "Invalid ingredients"}, False

        return {}, True

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("La conexión MySQL está cerrada")
