#!/usr/bin/env python
# *-* coding: utf-8 *-*
# @File     : main.py
# @Project  : zmq_demo
# @Time     : 2020/7/13 上午10:39
# @Author   : shi


import sys
from PyQt5.QtWidgets import QApplication, QTableView
from freezeTableWidget import freezeWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTextStream, QFile


def readFile(file, model):
    fd = open(file, 'r')
    line = fd.readline()
    content = line.split(',')
    model.setHorizontalHeaderLabels(content)
    row = 0
    while True:
        line = fd.readline()
        if not line:
            break
        if not line.startswith('#') and line.__contains__(','):
            content = line.split(',')
            for col in range(len(content)):
                # yield row, col, QStandardItem(content[col])
                model.setItem(row, col, QStandardItem(content[col]))
            row += 1
    fd.close()


def qtRead(file, model):
    fd = QFile(file)
    if fd.open(QFile.ReadOnly):
        stream = QTextStream(fd)
        line = stream.readLine()
        con = line.split(',')
        model.setHorizontalHeaderLabels(con)
        row = 0
        while not stream.atEnd():
            line = stream.readLine()
            if not line.startswith('#') and line.__contains__(','):
                con = line.split(',')
                for col in range(len(con)):
                    item = QStandardItem(con[col])
                    model.setItem(row, col, item)
                row += 1
    fd.close()


def main():
    app = QApplication(sys.argv)
    model = QStandardItemModel()
    # [model.setItem(c[0], c[1], c[2]) for c in readFile('grades.txt', model)]
    # readFile('grades.txt', model)
    qtRead('grades.txt', model)
    tableView = freezeWidget.FreezeTableWidget(model)
    tableView.init()
    tableView.setWindowTitle('Frozen Widget')
    tableView.resize(560, 680)
    tableView.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
