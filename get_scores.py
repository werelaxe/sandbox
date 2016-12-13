#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from urllib.request import urlopen

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore


url = 'http://anytask.urgu.org/course/statistics/45'


def get_score():
	response = urlopen(url)
	content = response.read().decode()
	return re.findall("Surname name.*?<span class=\"label label-info\">(\d*)</span>", content, re.DOTALL)[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())
