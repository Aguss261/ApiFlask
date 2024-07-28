import json
import datetime

from src.database.conexion import get_mysql_connection

import mysql.connector

from src.utils.validator_body import validar_hamburguesa


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

    def delete_pedido(self, pedido_id):
        try:
            cursor = self.connection.cursor()
            sql_query = "DELETE from pedidos where pedido_id = %s"
            cursor.execute(sql_query ,(pedido_id,))
            self.connection.commit()

            if cursor.rowcount == 0:
                cursor.close()
                return {"error": "Pedido no encontrado"}, 404
            cursor.close()
            return {"Mensaje": "Pedido eliminado con exito"}
        except Exception as e:
            self.connection.rollback()
            return {"error": str(e)}


    def edit_pedido(self, pedido_id, user_id, direccion, hamburguesas, state):
        cursor = None
        if not validar_hamburguesa(hamburguesas):
            return False, {"error": "Hamburguesa invalida"}
        try:
            cursor = self.connection.cursor()
            price = self.obtenerPriceTotal(hamburguesas)
            hamburguesas_json = json.dumps(hamburguesas)
            sql_query = """
            UPDATE pedidos
            SET direccion = %s, hamburguesas = %s, price = %s, state = %s
            WHERE pedido_id = %s and user_id = %s
            """
            cursor.execute(sql_query,(direccion,hamburguesas_json,price,state,pedido_id,user_id))
            self.connection.commit()

            if cursor.rowcount > 0:
                return True, {"message": "Hamburguesa editada correctamente"}
            else:
                return False, {"error": "No se pudo editar la hamburguesa"}

        except mysql.connector.Error as error:
            print(f"Error al editar la hamburguesa: {error}")
            return False, {"error": "Error en la base de datos"}
        finally:
            cursor.close()



    def create_pedido(self, user_id, direccion, hamburguesas):
        cursor = None
        if not validar_hamburguesa(hamburguesas):
            return False, {"error": "Hamburguesa invalida"}

        try:
            cursor = self.connection.cursor()
            price = self.obtenerPriceTotal(hamburguesas)
            state = "Pendiente"
            hora = datetime.datetime.now().strftime('%H:%M')
            fecha = datetime.datetime.now().strftime('%Y-%m-%d')


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





    def pasar_a_segundos(self, pedido):
        for key, value in pedido.items():
            if isinstance(value, datetime.timedelta):
                pedido[key] = value.total_seconds()

    def obtenerPriceTotal(self, hamburguesas):
        total = 0
        if isinstance(hamburguesas, list):
            for hamburguesa in hamburguesas:
                total += hamburguesa.get("price", 0)
        elif isinstance(hamburguesas, dict):
            total += hamburguesas.get("price", 0)
        return total