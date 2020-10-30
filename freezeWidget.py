#!/usr/bin/env python
# *-* coding: utf-8 *-*
# @File     : freezeTableWidget.py
# @Project  : zmq_demo
# @Time     : 2020/7/13 上午10:46
# @Author   : shi
import typing
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QItemSelectionModel, QItemSelection


class FreezeTableWidget(QTableView):

    def __init__(self, model=None):
        super(FreezeTableWidget, self).__init__()
        self.model = model
        self.frozenTableView = QTableView(self)
        self.horizontalView = QTableView(self)
        self._x = 0
        self._y = 0
        self._hei = 0
        self._wid = 0

    def init(self):
        self.setModel(self.model)
        self.frozenTableViewInit()
        self.horizontalViewInit()

        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.verticalScrollBar().valueChanged.connect(self.vConnectFv)
        self.horizontalScrollBar().valueChanged.connect(self.hScrollBarSet)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.fVConnectV)
        self.selectionModel().selectionChanged.connect(self.selectionSlot)

    def hScrollBarSet(self, a0: int):
        self.viewport().stackUnder(self.horizontalView)
        self.horizontalView.stackUnder(self.frozenTableView)
        self.horizontalView.horizontalScrollBar().setValue(a0)

    def vConnectFv(self, a0: int):
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.stackUnder(self.horizontalView)
        self.frozenTableView.verticalScrollBar().setValue(a0)

    def fVConnectV(self, a0: int):
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.stackUnder(self.horizontalView)
        self.verticalScrollBar().setValue(a0)

    def frozenTableViewInit(self):
        self.frozenTableView.setModel(self.model)
        self.frozenTableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.frozenTableView.horizontalHeader().setFixedHeight(self.horizontalHeader().height())

        self.viewport().stackUnder(self.frozenTableView)

        # QSS decorate
        self.frozenTableView.setStyleSheet('QTableView {'
                                           'border: none;'
                                           'background-color: #8EDE21;'
                                           'selection-background-color: #999}')
        self.frozenTableView.setSelectionModel(self.selectionModel())
        for col in range(1, self.model.columnCount()):
            self.frozenTableView.setColumnHidden(col, True)

        self.frozenTableView.setColumnWidth(0, self.columnWidth(0))
        self.frozenTableView.setRowHeight(0, self.rowHeight(0))
        self.frozenTableView.setRowHeight(1, self.rowHeight(1))
        self.frozenTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()

        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerPixel)

    def horizontalViewInit(self):
        self.horizontalView.setModel(self.model)
        self.horizontalView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalView.horizontalHeader().hide()
        self.horizontalView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalView.verticalHeader().setFixedWidth(self.verticalHeader().width())

        self.frozenTableView.stackUnder(self.horizontalView)

        self.horizontalView.setStyleSheet('QTableView {'
                                          'border: none;'
                                          'background-color: #8EDE21;'
                                          'selection-background-color: #999}')
        self.horizontalView.setSelectionModel(self.selectionModel())
        for row in range(2, self.model.rowCount()):
            self.horizontalView.setRowHidden(row, True)

        self.horizontalView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalView.show()

        self.updateFrozenTableGeometry()
        self.horizontalView.setHorizontalScrollMode(self.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        self.horizontalView.setColumnWidth(logicalIndex, newSize)
        if logicalIndex == 0:
            self.frozenTableView.setColumnWidth(0, newSize)
        self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)
        if not logicalIndex:
            self.horizontalView.setRowHeight(0, newSize)
        if logicalIndex == 1:
            self.horizontalView.setRowHeight(1, newSize)
        self.updateFrozenTableGeometry()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        QTableView.resizeEvent(self, e)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction: QAbstractItemView.CursorAction,
                   modifiers: typing.Union[QtCore.Qt.KeyboardModifiers,
                                           QtCore.Qt.KeyboardModifier]) -> QtCore.QModelIndex:
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        if cursorAction == QAbstractItemView.MoveLeft and current.column() > 0 \
                and self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(0):
            newSize = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() \
                      - self.frozenTableView.columnWidth(0)
            self.horizontalScrollBar().setValue(newSize)
        if cursorAction == QAbstractItemView.MoveUp and current.row() > 0 \
                and self.visualRect(current).topLeft().y() < self.horizontalView.rowHeight(0):
            newSize = self.verticalScrollBar().value() + self.visualRect(current).topLeft().y() \
                      - self.horizontalView.rowHeight(0) - self.horizontalView.rowHeight(1)
            self.verticalScrollBar().setValue(newSize)
        return current

    def scrollTo(self, index: QtCore.QModelIndex, hint: QAbstractItemView.ScrollHint = ...) -> None:
        if index.column() > 0:
            QTableView.scrollTo(self, index, hint)
        if index.row() > 0:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                         self.frameWidth(), self.columnWidth(0),
                                         self.viewport().height() + self.horizontalHeader().height())
        self.horizontalView.setGeometry(self.frameWidth(), self.frameWidth() + self.horizontalHeader().height(),
                                        self.viewport().width() + self.verticalHeader().width(),
                                        self.rowHeight(0) + self.rowHeight(1))

    def selectionSlot(self, selected: QItemSelection, deSelected: QItemSelection):
        index = self.selectionModel().selectedIndexes()
        self._x = index[0].row()
        self._y = index[0].column()
        for i in index:
            self._hei = i.row()
            self._wid = i.column()

        self._hei -= self._x - 1
        self._wid -= self._y - 1
