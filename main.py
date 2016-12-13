import re
from urllib.request import urlopen
import sys
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

url = 'http://anytask.urgu.org/course/statistics/45'


def func_color(group):
    data = group.group(0)
    strings = group.group(0).split()
    score = -1
    name = "{} {}".format(strings[3], strings[4])
    try:
        if strings[11] != '</td>':
            score = int(re.findall('[0-9]+', strings[11])[0])
        is_andrew = False
    except Exception as e:
        score = int(re.findall("[0-9]+", strings[-1])[0])
        is_andrew = True
        name = "{} {}".format(strings[0], strings[1])
    if is_andrew:
        if score == -1:
            color = 'brown'
        elif score >= 40:
            color = 'green'
        else:
            color = 'red'
        return '<font color="' + color + '">' + name + '</font>' + data[len(name):]
    if score == -1:
        color = 'brown'
    elif score >= 40:
        color = 'green'
    else:
        color = 'red'
    return data[:32] + '<font color="' + color + '">' + name + '</font>' + data[32 + len(name):]


def get_score():
    response = urlopen(url)
    content = response.read().decode()
    content = re.sub('Шелудяков Андрей[^&]+?</span>', func_color, content)
    pre_score = re.findall("<b>КН-101</b>(.*?)<b>КН-102</b>", content, re.DOTALL)[0]
    final_score = re.sub('<td style="width: 28%;"([^&]+?)<tr>', func_color, pre_score)
    return final_score


class ScoresWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        width = 720
        height = 500
        self.setGeometry(300, 300, width, height)
        label = QLabel(get_score(), self)
        label.setGeometry(0, 0, width, height)
        label.move(0, 0)
        label.mouseMoveEvent = self.mouseMoveEvent
        label.mouseReleaseEvent = self.mouseReleaseEvent
        label.setText("Start")
        self.label = label
        self.timer = QBasicTimer()
        self.timer.start(60 * 1000, self)
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
        except AttributeError:
            pass  # it's alright


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scores_form = ScoresWidget()
    scores_form.update()
    sys.exit(app.exec_())
