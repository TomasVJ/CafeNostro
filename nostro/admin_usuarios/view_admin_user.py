#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from admin_user import Ui_AdminUsers
import controller_admin_user
import sys
import view_formulario_usuario


class AdminUsers(QtGui.QWidget):
    """
    Clase AdminUsers encargada de mostrar una tabla con todos los usuarios
    actualmente registrados en la base de datos.
    """

    __header_table__ = ((u"ID", 20),
                        (u"Nombres", 200),
                        (u"Apellidos", 200),
                        (u"Rut", 120),
                        (u"Tipo", 100))

    __type_users__ = ((u"Administrador"),
                      (u"Garzón"))

    def __init__(self, parent=None):
        'Constructor de la clase'
        QtGui.QWidget.__init__(self)
        self.ui = Ui_AdminUsers()
        self.ui.setupUi(self)
        self.setFocus()
        self.set_model_table()
        self.set_source_model(self.load_users(self))
        self.ui.tableUsers.verticalHeader().setVisible(False)
        self.ui.tableUsers.setColumnHidden(0, True)
        self.connect_actions()

    def connect_actions(self):
        """Conectar botones con su respectiva accion"""
        self.ui.editar_button.clicked.connect(self.action_btn_editar)
        self.ui.nuevo_button.clicked.connect(self.action_btn_nuevo)
        self.ui.eliminar_button.clicked.connect(self.action_btn_eliminar)

    def reload_data_table(self):
        """Recarga los datos en la tabla (actualiza la vista)"""
        self.set_source_model(self.load_users(self))

    def action_btn_nuevo(self):
        """Metodo para lanzar el formulario de creacion del nuevo usuario"""
        self.nuevoUsuarioWindow = view_formulario_usuario.FormularioUsuario()
        self.nuevoUsuarioWindow.reloadT.connect(self.reload_data_table)
        self.nuevoUsuarioWindow.exec_()

    def action_btn_editar(self):
        """
        Método que es llamado cuando el usuario del programa presiona 
        en el boton 'editar'.
        Crea una nueva instancia de FormularioUsuario en caso de que haya 
        seleccionado un usuario.
        """
        index = self.ui.tableUsers.currentIndex()
        if index.row() == -1:  # No se ha seleccionado producto
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Debe seleccionar un usuario.")
            msgBox.exec_()
            return False
        else:
            self.editUsuarioWindow = view_formulario_usuario.FormularioUsuario(
                self.id)
            self.editUsuarioWindow.reloadT.connect(self.reload_data_table)
            self.editUsuarioWindow.exec_()
            # self.load_users(self)

    def action_btn_eliminar(self):
        """
        Método que es llamado cuando el usuario del programa presiona en el 
        boton 'eliminar'.
        Elimina el usuario seleccionado de la base de datos.
        """
        index = self.ui.tableUsers.currentIndex()
        if index.row() == -1:  # No se ha seleccionado producto
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setWindowTitle(u"Error")
            msgBox.setText(u"Debe seleccionar un usuario.")
            msgBox.exec_()
            return False
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setStandardButtons(
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            msgBox.setWindowTitle(u"Advertencia")
            msgBox.setText(
                u"¿Esta seguro de querer eliminar el usuario seleccionado?")
            press = msgBox.exec_()
            if press == QtGui.QMessageBox.Ok:
                usuario = controller_admin_user.UpdateStatusUsuario(self.id, 0)
                self.reload_data_table()
            else:
                return False

    def load_users(self, parent):
        """
        Carga la información de la base de datos en la tabla.
        Obtiene desde la base de datos a traves del controlador
        la información completa de la tabla.
        Crea un model para adjuntar los datos a la grilla y luego
        lo retorna para utilizarlo en setSourceModel.
        """
        self.typeModelClass = parent

        usuarios = controller_admin_user.getUsuarioStatus(1)
        row = len(usuarios)

        model = QtGui.QStandardItemModel(row, len(self.__header_table__))

        for i, data in enumerate(usuarios):
            row = [data.id_usuario, 
                   data.nombre, 
                   data.apellido, 
                   data.rut, 
                   data.tipo]
            for j, field in enumerate(row):
                index = model.index(i, j, QtCore.QModelIndex())
                if j is 4:
                    # print self.__type_users__[field]
                    model.setData(index, self.__type_users__[field])
                else:
                    model.setData(index, field)

        modelSel = self.ui.tableUsers.selectionModel()
        modelSel.currentChanged.connect(self.tabla_cell_selected)

        return model

    def tabla_cell_selected(self, index, indexp):
        """
        Método que es llamado cuando el usuario cambia la seleccion actual
        de la tabla 'tableUsers'.
        Se guarda en la variable global 'id' el id del usuario seleccionado.
        """
        model = self.ui.tableUsers.model()
        index = self.ui.tableUsers.currentIndex()
        self.id = model.index(index.row(), 0, QtCore.QModelIndex()).data()

    def set_model_table(self):
        """Define el módelo de la grilla para trabajarla."""
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.ui.tableUsers.setModel(self.proxyModel)

    def set_source_model(self, model):
        """
        Actualiza constantemente el origen de los datos para siempre tenerlos
        al día así pudiendo buscar y mostrar solo algunos datos.
        Además asigna el tamaño de las columnas a las grillas respectivas.
        """
        self.proxyModel.setSourceModel(model)

        self.ui.tableUsers.horizontalHeader().setResizeMode(
            1, self.ui.tableUsers.horizontalHeader().Stretch)
        self.ui.tableUsers.horizontalHeader().setResizeMode(
            2, self.ui.tableUsers.horizontalHeader().Stretch)

        for col, h in enumerate(self.__header_table__):
            model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
            self.ui.tableUsers.setColumnWidth(col, h[1])

        self.ui.tableUsers.sortByColumn(0, QtCore.Qt.AscendingOrder)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = AdminUsers()
    myapp.show()
    sys.exit(app.exec_())
