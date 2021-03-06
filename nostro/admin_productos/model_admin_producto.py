#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Modelo.
Accede a la base de datos, tiene la habilidad de crear, modificar y eliminar registros de ella.
"""

import MySQLdb


def connect():
    conex = MySQLdb.connect("localhost", "root", "", "cafe_nostro")
    return conex


def obtenerObjetoProductos(data):
    """
    Recibe como parametro la tupla recibida desde la BD y retorna una lista 
    de objetos con todos los datos de los productos.
    """
    listaP = list()
    for i,row in enumerate(data):
        listaP.append(Producto(row[0],row[1],row[
            2],row[3],row[4],row[5],row[6],row[7]))
    return listaP


def obtenerObjetoCategorias(data):
    """
    Recibe como parametro la tupla recibida desde la BD y retorna una lista 
    de objetos con todos los datos de las categorias.
    """
    listaC = list()
    for i, row in enumerate(data):
        listaC.append(Categoria(row[0], row[1], row[2], row[3]))
    return listaC


class Producto(object):
    """
    Clase que representa a la tabla Producto.
    Una instancia de esta clase representa una fila.
    La instancia (objeto) puede estar en la BD o no.
    """
    __tablename__ = "producto"
    id_producto = None  # Primary Key
    nombre = ""
    descripcion = ""
    precio_neto = ""
    precio_bruto = ""
    status = ""
    id_categoria = ""
    codigo = ""

    def __init__(
            self,
            id_producto=None,
            nombre="",
            descripcion="",
            precio_neto="",
            precio_bruto="",
            status="",
            id_categoria="",
            codigo=""):

        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_neto = precio_neto
        self.precio_bruto = precio_bruto
        self.status = status
        self.id_categoria = id_categoria
        self.codigo = codigo

    def UpdateDataProducto(cls):
        """
        Interacciona con la base de datos a travez de una query que actualiza
        todos los campos de un producto, especificando su id.
        """
        conex = connect()
        conn = conex.cursor()

        query = "UPDATE producto SET nombre = %s, descripcion = %s, precio_neto = %s, precio_bruto =  %s , status = %s, idCategoria = %s, codigo = %s WHERE idProducto = %s"
        conn.execute(query,
                     (cls.nombre,
                      cls.descripcion,
                      cls.precio_neto,
                      cls.precio_bruto,
                      cls.status,
                      cls.id_categoria,
                      cls.codigo,
                      cls.id_producto))
        conex.commit()
        conn.close()

    def UpdateStatusProducto(cls):
        """
        Interacciona con la base de datos a travez de una query que actualiza 
        el estado de un Producto, especificando su id.
        """
        conex = connect()
        conn = conex.cursor()
        query = "UPDATE producto SET status = %s WHERE idProducto = %s"
        conn.execute(query,
                     (int(cls.status),
                      cls.id_producto))
        conex.commit()
        conn.close()

    def AddDataProducto(cls):
        """
        Agrega un nuevo producto a la base de datos, rellenando todos sus 
        campos.
        """
        conex = connect()
        conn = conex.cursor()
        query = "INSERT INTO producto(nombre, descripcion, precio_neto, precio_bruto, status, idCategoria, codigo) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        conn.execute(query,
                     (cls.nombre,
                      cls.descripcion,
                      cls.precio_neto,
                      cls.precio_bruto,
                      cls.status,
                      cls.id_categoria,
                      cls.codigo))
        conex.commit()
        conn.close()

    def getProductoId(cls):
        """
        Retorna el producto (objeto) que corresponde a la id especificada.
        """
        conex = connect()
        conn = conex.cursor()
        query = "SELECT * FROM producto WHERE idProducto = {}".format(
            cls.id_producto)
        conn.execute(query)
        Producto = conn.fetchall()
        conn.close()
        return obtenerObjetoProductos(Producto)

    def hayProductoCodigo(cls):
        """
        Retorna el producto (objeto) que corresponda al codigo especificado.
        """
        conex = connect()
        conn = conex.cursor()
        query = "SELECT * FROM producto WHERE codigo = %s"
        conn.execute(query,[cls.codigo])
        Producto = conn.fetchall()
        conn.close()
        return obtenerObjetoProductos(Producto)

    def getProductoCategoria(cls):
        """
        Retorna los productos pertenecientes a una categoria especifica.
        """
        conex = connect()
        conn = conex.cursor()
        query = "SELECT * FROM producto WHERE idCategoria = {} and status = 1".format(
            cls.id_categoria)
        conn.execute(query)
        Producto = conn.fetchall()
        conn.close()
        return obtenerObjetoProductos(Producto)

    def getProductoCodigo(cls):
        """
        Retorna los productos que, en su código, contengan la palabra
        entregada en cls.codigo. 
        """
        conex = connect()
        conn = conex.cursor()
        query = "SELECT * FROM producto WHERE codigo like %s and status = 1"
        conn.execute(query,[cls.codigo])
        Producto = conn.fetchall()
        conn.close()
        return obtenerObjetoProductos(Producto)

    def deleteProducto(cls):
        """
        Elimina un producto especificando su id.
        """
        conex = connect()
        conn = conex.cursor()
        query = "DELETE FROM producto WHERE idProducto = {}".format(
            cls.id_producto)
        conn.execute(query)
        conex.commit()
        conn.close()

    @classmethod
    def all(cls):
        """
        Método utlizado para obtener la colección completa de filas
        en la tabla Producto.
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocarlo desde la clase
        """
        query = "SELECT * FROM {}".format(
            cls.__tablename__)

        try:
            conex = connect()
            conn = conex.cursor()
            conn.execute(query)
            data = conn.fetchall()
            return obtenerObjetoProductos(data)

        except MySQLdb.Error as e:
            print "Error al obtener los Productos:", e.args[0]
            return None

        conn.close()

    def getProductoStatus(cls):
        """
        Método utlizado para obtener los Productos que compartan un valor de id_status.
        """
        query = "SELECT * FROM producto WHERE status = {}".format(
            cls.status)

        try:
            conex = connect()
            conn = conex.cursor()
            conn.execute(query)
            data = conn.fetchall()
            return obtenerObjetoProductos(data)

        except MySQLdb.Error as e:
            print "Error al obtener los Productos:", e.args[0]
            return None

        conn.close()


class Categoria(object):
    """
    Clase que representa a la tabla categoria.
    Una instancia de esta clase representa una fila.
    La instancia (objeto) puede estar en la BD o no.
    """
    __tablename__ = "categoria"
    id_categoria = None  # Primary Key
    nombre = ""
    descripcion = ""
    preparada_en = ""

    def __init__(
            self,
            id_producto=None,
            nombre="",
            descripcion="",
            categoria=""):

        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria

    @classmethod
    def getCategorias(cls):
        """
        Método utlizado para obtener todas las filas de la tabla categoria
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocarlo desde la clase
        """
        query = "SELECT * FROM categoria"

        try:
            conex = connect()
            conn = conex.cursor()
            conn.execute(query)
            data = conn.fetchall()
            return obtenerObjetoCategorias(data)

        except MySQLdb.Error as e:
            print "Error al obtener las categorias", e.args[0]
            return None

        conn.close()

    @classmethod
    def getNombresCategorias(cls):
        """
        Método utlizado para obtener todos los nomrbes de las categorias ingresadas
        Este método al ser de clase no necesita una instancia (objeto)
        Sólo basta con invocarlo desde la clase
        """
        query = "SELECT * FROM categoria"

        try:
            conex = connect()
            conn = conex.cursor()
            conn.execute(query)
            data = conn.fetchall()
            return obtenerObjetoCategorias(data)

        except MySQLdb.Error as e:
            print "Error al obtener las categorias", e.args[0]
            return None

        conn.close()
