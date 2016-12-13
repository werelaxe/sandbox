#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from urllib.request import urlopen

import sys

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

url = 'http://anytask.urgu.org/course/statistics/45'


def get_score():
    response = urlopen(url)
    content = response.read().decode()
    return re.findall("<b>КН-101</b>(.*?)</table>", content, re.DOTALL)[0]


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.statusBar().showMessage('Ready')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        width = 600
        height = 500
        self.setGeometry(300, 300, width, height)
        lbl1 = QLabel(get_score(), self)
        lbl1.setGeometry(0, 0, width, height)
        lbl1.move(0, 0)
        lbl1.mouseMoveEvent = self.mouseMoveEvent
        lbl1.mouseReleaseEvent = self.mouseReleaseEvent
        lbl1.setText("Kek")
        self.label = lbl1

        self.timer = QBasicTimer()
        self.timer.start(10000, self)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def timerEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        self.offset = None

    def update(self, *__args):
        self.label.setText(get_score())

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except Exception as e:
            pass  # print(e)


if __name__ == '__main__':
    # print(get_score())
    try:
        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)