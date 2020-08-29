#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/7/13 22:37
# @Author : shi
# @Project: tableWidget
# @File   : main.py


from freezeWidget.freezeTableWidget import FreezeTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
import sys


def qtRead(file, model):
    fd = QFile(file)
    try:
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
                    [model.setItem(row, col, QStandardItem(con[col])) for col in range(len(con))]
                    row += 1
    except Exception as e:
        print(str(e))

    fd.close()


def readData(file, model):
    with open(file, 'r', encoding='utf-8') as fd:
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
                [model.setItem(row, col, QStandardItem(content[col])) for col in range(len(content))]
                # for col in range(len(content)):
                #     item = QStandardItem(content[col])
                #     # yield row, col, item
                #     model.setItem(row, col, item)
                row += 1
    fd.close()


if __name__ == '__main__':
    app = QApplication([])
    model = QStandardItemModel()
    # 添加数据
    # readData('grades.txt', model)
    qtRead('grades.txt', model)
    tableView = FreezeTableView(model)
    tableView.init()
    tableView.setWindowTitle('Frozen Widget')
    tableView.resize(560, 680)
    tableView.show()

    sys.exit(app.exec_())
