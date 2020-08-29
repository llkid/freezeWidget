#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/7/13 21:46
# @Author : shi
# @Project: tableWidget
# @File   : freezeTableWidget.py


import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView, QAbstractSlider
from PyQt5.QtCore import Qt, QModelIndex


class FreezeTableView(QTableView, QAbstractSlider):

    def __init__(self, model):
        super(FreezeTableView, self).__init__()
        self.model = model
        self.frozenTableView = QTableView(self)
        self.horizontalView = QTableView(self)
        self.up = True

    def init(self):
        self.setModel(self.model)
        self.frozenTableInit()
        self.horizontalViewInit()

        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.verticalScrollBar().valueChanged.connect(self.vConnectFV)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.fVConnectV)
        self.horizontalScrollBar().valueChanged.connect(self.hConnectH)

    def vConnectFV(self, a0: int):
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.stackUnder(self.horizontalView)
        self.frozenTableView.verticalScrollBar().setValue(a0)

    def fVConnectV(self, a0: int):
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.stackUnder(self.horizontalView)
        self.verticalScrollBar().setValue(a0)

    def hConnectH(self, a0: int):
        self.viewport().stackUnder(self.horizontalView)
        self.horizontalView.stackUnder(self.frozenTableView)
        self.horizontalView.horizontalScrollBar().setValue(a0)

    def frozenTableInit(self):
        self.frozenTableView.setModel(self.model)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.horizontalHeader().setFixedHeight(self.horizontalHeader().height())
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.setStyleSheet('QTableView {'
                                           'border: none;'
                                           'background-color: #8EDE21;'
                                           'selection-background-color: #999}')
        self.frozenTableView.setSelectionModel(self.selectionModel())
        [self.frozenTableView.setColumnHidden(col, True) for col in range(1, self.model.columnCount())]
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()

        self.updateFrozenTableGeometry()
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)

    def horizontalViewInit(self):
        self.horizontalView.setModel(self.model)
        self.horizontalView.horizontalHeader().hide()
        self.horizontalView.setFocusPolicy(Qt.NoFocus)
        self.horizontalView.verticalHeader().setFixedWidth(self.verticalHeader().width())
        self.horizontalView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.frozenTableView.stackUnder(self.horizontalView)
        self.horizontalView.setStyleSheet('QTableView { border: none;'
                                          'background-color: #8EDE21;'
                                          'selection-background-color: #999}')
        self.horizontalView.setSelectionModel(self.selectionModel())
        [self.horizontalView.setRowHidden(row, True) for row in range(1, self.model.rowCount())]
        self.horizontalView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalView.show()

        self.updateFrozenTableGeometry()
        self.horizontalView.setHorizontalScrollMode(self.ScrollPerPixel)

    def updateFrozenTableGeometry(self):
        self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                         self.frameWidth(), self.columnWidth(0),
                                         self.viewport().height() + self.horizontalHeader().height())
        self.horizontalView.setGeometry(self.frameWidth(), self.frameWidth() + self.horizontalHeader().height(),
                                        self.viewport().width() + self.verticalHeader().width(), self.rowHeight(0))

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        self.horizontalView.setColumnWidth(logicalIndex, newSize)
        if not logicalIndex:
            self.frozenTableView.setColumnWidth(0, newSize)
        self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)
        if not logicalIndex:
            self.horizontalView.setRowHeight(0, newSize)
        self.updateFrozenTableGeometry()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        QTableView.resizeEvent(self, e)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index: QtCore.QModelIndex, hint: QAbstractItemView.ScrollHint = ...) -> None:
        if index.column() > 0 or index.row() > 0:
            QTableView.scrollTo(self, index, hint)

    def moveCursor(self, cursorAction: QAbstractItemView.CursorAction,
                   modifiers: typing.Union[QtCore.Qt.KeyboardModifiers,
                                           QtCore.Qt.KeyboardModifier]) -> QtCore.QModelIndex:
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        if cursorAction == QAbstractItemView.MoveLeft and current.column() > 0 \
                and self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(0):
            newValue = self.verticalScrollBar().value() + self.visualRect(current).topLeft().x() \
                       - self.frozenTableView.columnWidth(0)
            self.horizontalScrollBar().setValue(newValue)
        if cursorAction == QAbstractItemView.MoveUp and current.row() > 0 \
                and self.visualRect(current).topLeft().y() < self.horizontalView.rowHeight(0):
            newValue = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().y() \
                       - self.horizontalView.rowHeight(0)
            self.verticalScrollBar().setValue(newValue)

        return current
