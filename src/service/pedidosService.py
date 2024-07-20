import json
from datetime import timedelta

from MySQLdb import MySQLError
from flask import jsonify

from src.database.conexion import get_mysql_connection

import mysql.connector


class PedidosService:
    def __init__(self):
        self.connection = get_mysql_connection()

    def getAllPedidos(self):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * FROM pedidos"
            cursor.execute(sql_query)
            resultados = cursor.fetchall()

            for pedido in resultados:
                self.pasar_a_segundos(pedido)

            return resultados
        except mysql.connector.Error as error:
            print(f"Error buscando los pedidos: {error}")
            return None
        finally:
            if cursor:
                cursor.close()


    def get_pedido_by_id(self, id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * from pedidos where pedido_id = %s"
            cursor.execute(sql_query, (id,))
            resultado = cursor.fetchone()
            if resultado is None:
                return {"error": "Pedido no encontrado"}, 404


            self.pasar_a_segundos(resultado)

            return resultado
        except mysql.connector.Error as error:
            print(f"Error buscando el pedido: {error}")
            return None
        finally:
            if cursor:
                cursor.close()


    def get_pedido_by_user_id(self, user_id):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * from pedidos where user_id = %s"
            cursor.execute(sql_query, (user_id,))
            resultado = cursor.fetchall()
            if not resultado:
                return {"error": "Pedido no encontrado"}, 404

            for pedido in resultado:
                self.pasar_a_segundos(pedido)

            return resultado
        except mysql.connector.Error as error:
            print(f"Error buscando el pedido: {error}")
            return None
        finally:
            if cursor:
                cursor.close()


    def get_pedido_by_user(self, user_id):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * from pedidos where user_id = %s"
            cursor.execute(sql_query, (user_id,))
            resultado = cursor.fetchall()
            if not resultado:
                return {"error": "Pedido no encontrado"}, 404

            for pedido in resultado:
                self.pasar_a_segundos(pedido)

            return resultado
        except mysql.connector.Error as error:
            print(f"Error buscando el pedido: {error}")
            return None
        finally:
            if cursor:
                cursor.close()



    def get_pedido_by_fecha(self, fecha):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql_query = "SELECT * from pedidos where fecha = %s"
            cursor.execute(sql_query, (fecha,))
            resultado = cursor.fetchall()
            if not resultado:
                return {"error": "Pedido no encontrado"}, 404

            for pedido in resultado:
                self.pasar_a_segundos(pedido)

            return resultado
        except mysql.connector.Error as error:
            print(f"Error buscando el pedido: {error}")
            return None
        finally:
            if cursor:
                cursor.close()




    def create_pedido(self, user_id, direccion, price, state, hora, fecha, hamburguesas):
        if not self.validar_hamburguesa(hamburguesas):
            return False, {"error": "Hamburguesa invalida"}

        try:
            cursor = self.connection.cursor()
            sql_query = """
                INSERT INTO pedidos (user_id, direccion, price, state, hamburguesas, hora, fecha)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            hamburguesas_json = json.dumps(hamburguesas)
            cursor.execute(sql_query, (user_id, direccion, price, state, hamburguesas_json, hora, fecha))
            self.connection.commit()

            if cursor.rowcount > 0:
                return True, {"message": "Pedido creado correctamente"}
            else:
                return False, {"error": "No se pudo crear el pedido"}

        except mysql.connector.Error as error:
            print(f"Error al crear el pedido: {error}")
            return False, {"error": "Error en la base de datos"}
        finally:
            cursor.close()

    def validar_hamburguesa(self, hamburguesas):
        required_fields = ["id", "nombre", "price", "descripcion", "imgUrl", "ingredientes"]

        for hamburguesa in hamburguesas:
            for field in required_fields:
                if field not in hamburguesa:
                    print(f"Campo requerido faltante en hamburguesa: {field}")
                    return False


            ingredientes_fields = ["huevo", "lechuga", "tomate", "cebolla", "bacon", "pepino"]
            ingredientes = hamburguesa.get("ingredientes", {})
            for field in ingredientes_fields:
                if field not in ingredientes:
                    print(f"Campo de ingredientes faltante en hamburguesa: {field}")
                    return False

        return True

    def pasar_a_segundos(self, pedido):
        for key, value in pedido.items():
            if isinstance(value, timedelta):
                pedido[key] = value.total_seconds()
