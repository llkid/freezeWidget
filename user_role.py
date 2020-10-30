#!/usr/bin/env python
# *-* coding: utf-8 *-*
# @File     : user_role.py
# @Project  : zmq_demo
# @Time     : 2020/7/22 上午10:00
# @Author   : shi


import sys
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex


class Model(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(Model, self).__init__(parent)

        self._data = [[['%d - %d' % (i, j), False] for j in range(10)] for i in range(10)]

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            data, changed = self._data[index.row()][index.column()]

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self._data[0])

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = [value.toString(), True]
            self.dataChanged.emit(index, index)
            return True
        return False

    def data(self, index: QModelIndex, value: typing.Any, role: int = ...) -> any:
        if index.isValid():
            data, changed = self._data[index.row()][index.column()]

            if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
                return data

            if role == QtCore.Qt.BackgroundRole and changed:
                return QtGui.QBrush(QtCore.Qt.darkBlue)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t = QtWidgets.QTableView()
    m = Model(t)
    t.setModel(m)
    t.show()

    sys.exit(app.exec_())
