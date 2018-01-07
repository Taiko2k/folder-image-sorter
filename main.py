#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2018 Taiko2k captain.gxj@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# The purpose of this program is to sort images into folders

import sys
import shutil
import os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QFileDialog, QShortcut, QCheckBox, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QEvent
import qdarkgraystyle


class Ix:

    def __init__(self):

        self.current_paths = []
        self.current = None
        self.current_raw = None
        self.current_scaled = None
        self.previous = " "
        self.history = []
        self.allow_delete = False

        self.target = str(Path.home())
        p_home = os.path.join(self.target, "Pictures")
        if os.path.isdir(p_home):
            self.target = p_home

        self.w = 0
        self.h = 0

    def tab(self):

        text = ex.line.text()
        if text == "":
            ex.line.setText(self.previous)
        else:
            for item in self.history:
                if item[:len(text)] == text and len(item) > len(text):
                    ex.line.setText(item)
                    break


ix = Ix()


class ALineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):
        if (event.type() == QEvent.KeyPress) and (event.key() == Qt.Key_Tab):
            ix.tab()
            return True
        if ix.allow_delete:
            if (event.type() == QEvent.KeyPress) and (event.key() == Qt.Key_Delete):
                ex.delete()
                return True

        return QLineEdit.event(self, event)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.w = 1
        self.h = 1

        self.setGeometry(300, 300, 980, 470)
        self.setWindowTitle('Folder Image Sorter')
        self.setAcceptDrops(True)

        self.l1 = QLabel("Folder name", self)
        self.l1.move(80, 20)

        self.line = ALineEdit(self)
        self.line.setFrame(False)
        self.line.resize(200, 33)
        self.line.move(80, 50)
        self.line.returnPressed.connect(self.enter)

        self.directory_button = QPushButton(self)
        self.directory_button.setText("Set working directory")
        self.directory_button.resize(160, 33)
        self.directory_button.move(80, 130)
        self.directory_button.pressed.connect(self.open_direc)


        self.previous_button = QPushButton(self)
        self.previous_button.setText("Previous")
        self.previous_button.resize(80, 25)
        self.previous_button.move(80, 370)
        self.previous_button.pressed.connect(self.previous)

        self.next_button = QPushButton(self)
        self.next_button.setText("Next")
        self.next_button.resize(80, 25)
        self.next_button.move(80 + 80 + 15, 370)
        self.next_button.pressed.connect(self.next)

        self.shortcut = QShortcut(QKeySequence("Ctrl+Delete"), self)
        self.shortcut.activated.connect(self.delete)

        self.del_toggle = QCheckBox("Allow quick delete", self)
        self.del_toggle.move(80, 260)
        self.del_toggle.resize(160, 33)
        self.del_toggle.stateChanged.connect(self.toggle_del)

        self.show()

    def toggle_del(self, state):
        if state == 0:
            ix.allow_delete = False
        else:
            ix.allow_delete = True

    def previous(self):

        if ix.current is not None and ix.current > 0:
            ix.current -= 1
            ix.current_scaled = None
            ix.current_raw = None

        # self.line.setFocus()
        self.update()

    def next(self):

        if ix.current is not None and ix.current < len(ix.current_paths) - 1:
            ix.current += 1
            ix.current_scaled = None
            ix.current_raw = None

        # self.line.setFocus()
        self.update()

    def delete(self):

        if ix.current is None:
            return

        os.remove(ix.current_paths[ix.current])
        del ix.current_paths[ix.current]

        ix.current_scaled = None
        ix.current_raw = None
        if not ix.current_paths:
            ix.current = None
        self.update()

    def open_direc(self):
        old = ix.target
        ix.target = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(ix.target)
        if ix.target == "":
            ix.target = old
        self.line.setFocus()
        self.update()

    def enter(self):

        if ix.current is not None:

            name = self.line.text()
            if name != "" and ix.target != "":
                if name in ix.history:
                    ix.history.remove(name)
                ix.history.insert(0, name)
                ix.previous = name
                source = ix.current_paths[ix.current]

                target = os.path.join(ix.target, name)
                if not os.path.exists(target):
                    os.makedirs(target)

                full_target = os.path.join(target, os.path.basename(source))

                if not os.path.isfile(full_target):
                    ix.current_paths[ix.current] = full_target

                    print(source)
                    print(target)
                    shutil.move(source, target)
                else:
                    print("File already exists")

            if len(ix.current_paths) > ix.current + 1:
                ix.current += 1
                ix.current_scaled = None
                ix.current_raw = None

            self.line.clear()
            self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print("DROP")
            ix.current = 0
            if os.path.isfile(f):
                if f not in ix.current_paths:
                    ix.current_paths.append(f)
        self.update()

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)

        col = QColor(20, 20, 20)
        qp.setPen(col)

        self.w, self.h = self.size().width(), self.size().height()

        # qp.setBrush(QColor(20, 20, 20))
        # qp.drawRect(0, 0, self.w, self.h)
        #
        # self.drawText(event, qp)

        if ix.current is not None:
            if ix.current_raw is None:
                ix.current_raw = QPixmap(ix.current_paths[ix.current])
                ix.w = ix.current_raw.rect().width()
                ix.h = ix.current_raw.rect().height()

                ix.current_scaled = ix.current_raw.scaled(int(self.w * 0.6), int(self.h * 0.85), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if ix.current_scaled is not None:
            qp.drawPixmap(int(self.w * 0.38) + int((int(self.w * 0.6) - ix.current_scaled.rect().width()) / 2),
                          int(self.h * 0.05), ix.current_scaled)

        qp.setPen(QColor(210, 210, 210))
        font = QFont('Noto Sans', 11)
        #font.setBold(True)
        qp.setFont(font)

        line = str(ix.w) + " x " + str(ix.h)
        if ix.current is not None:
            qp.drawText(self.w - 150, self.h - 20, line)
            qp.drawText(self.w - 550, self.h - 20, os.path.basename(ix.current_paths[ix.current]))

        qp.drawText(80, 200, ix.target)



        if ix.current is not None:
            qp.drawText(80, 350, "On " + str(ix.current + 1) + " of " + str(len(ix.current_paths)))
        else:
            qp.drawText(500, 220, "1. Select a working directory where folders will be made.")
            qp.drawText(500, 180, "2. Drag and drop files to add to queue.")
            qp.drawText(500, 260, "3. For each image enter a folder name.")

        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    ex = Example()
    sys.exit(app.exec_())
