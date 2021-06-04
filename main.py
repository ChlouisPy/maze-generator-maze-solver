"""
Maze generator - Maze solver

Main window to configure the generation of the labyrinth and configure the pathfinder
made with PyQT5 Designer

GitHub : ChlouisPy
Twitter : @Chlouis_Py
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import pickle
import os


class StartGenerate:
    def setup_gui(self, START_GENERATE) -> None:
        """
        This function will setup component of the window
        :return None
        """
        START_GENERATE.setObjectName("START_GENERATE")
        START_GENERATE.resize(500, 412)

        self.centralwidget = QtWidgets.QWidget(START_GENERATE)
        self.centralwidget.setObjectName("centralwidget")

        # title
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 472, 45))
        self.label.setStyleSheet("font: 87 24pt \"Segoe UI Black\";")
        self.label.setObjectName("label")

        # break line
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 120, 471, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # label for maze size x
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 89, 17))
        self.label_2.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.label_2.setObjectName("label_2")

        # entry for maze size x
        self.MAZE_SIZE_X = QtWidgets.QSpinBox(self.centralwidget)
        self.MAZE_SIZE_X.setGeometry(QtCore.QRect(140, 150, 91, 22))
        self.MAZE_SIZE_X.setMinimum(3)
        self.MAZE_SIZE_X.setMaximum(5000)
        self.MAZE_SIZE_X.setProperty("value", 25)
        self.MAZE_SIZE_X.setObjectName("MAZE_SIZE_X")

        # label for maze size y
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(260, 150, 89, 17))
        self.label_3.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.label_3.setObjectName("label_3")

        # entry for maze size y
        self.MAZE_SIZE_Y = QtWidgets.QSpinBox(self.centralwidget)
        self.MAZE_SIZE_Y.setGeometry(QtCore.QRect(360, 150, 91, 22))
        self.MAZE_SIZE_Y.setMinimum(3)
        self.MAZE_SIZE_Y.setMaximum(5000)
        self.MAZE_SIZE_Y.setProperty("value", 25)
        self.MAZE_SIZE_Y.setObjectName("MAZE_SIZE_Y")

        # break line
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(230, 140, 31, 61))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # configuration label
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(180, 70, 127, 30))
        self.label_4.setStyleSheet("font: 16pt \"Segoe UI\";")
        self.label_4.setObjectName("label_4")

        # check box for instant maze
        self.INSTANT_PATH = QtWidgets.QCheckBox(self.centralwidget)
        self.INSTANT_PATH.setGeometry(QtCore.QRect(20, 280, 131, 21))
        self.INSTANT_PATH.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.INSTANT_PATH.setObjectName("INSTANT_PATH")

        # check box for best path
        self.BEST_PATH = QtWidgets.QCheckBox(self.centralwidget)
        self.BEST_PATH.setGeometry(QtCore.QRect(190, 280, 113, 21))
        self.BEST_PATH.setAutoFillBackground(False)
        self.BEST_PATH.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.BEST_PATH.setChecked(True)
        self.BEST_PATH.setObjectName("BEST_PATH")

        # check box for path search
        self.PATH_SEARCH = QtWidgets.QCheckBox(self.centralwidget)
        self.PATH_SEARCH.setGeometry(QtCore.QRect(350, 280, 126, 21))
        self.PATH_SEARCH.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.PATH_SEARCH.setChecked(True)
        self.PATH_SEARCH.setTristate(False)
        self.PATH_SEARCH.setObjectName("PATH_SEARCH")

        # break line
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(10, 310, 471, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        # button to start generation
        self.START_GENERATION = QtWidgets.QPushButton(self.centralwidget)
        self.START_GENERATION.setGeometry(QtCore.QRect(190, 340, 111, 25))
        self.START_GENERATION.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.START_GENERATION.setObjectName("START_GENERATION")
        # add command
        self.START_GENERATION.clicked.connect(self.start)

        # break line
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(10, 250, 471, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")

        # label for
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 210, 89, 17))
        self.label_5.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.label_5.setObjectName("label_5")

        self.MAZE_SEED = QtWidgets.QSpinBox(self.centralwidget)
        self.MAZE_SEED.setGeometry(QtCore.QRect(110, 210, 341, 22))
        self.MAZE_SEED.setMinimum(1)
        self.MAZE_SEED.setMaximum(2147483647)
        self.MAZE_SEED.setProperty("value", random.randint(1, 2147483647))
        self.MAZE_SEED.setDisplayIntegerBase(10)
        self.MAZE_SEED.setObjectName("MAZE_SEED")
        START_GENERATE.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(START_GENERATE)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        START_GENERATE.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(START_GENERATE)
        self.statusbar.setObjectName("statusbar")
        START_GENERATE.setStatusBar(self.statusbar)

        self.retranslate(START_GENERATE)
        QtCore.QMetaObject.connectSlotsByName(START_GENERATE)

    def retranslate(self, START_GENERATE) -> None:
        """
        This function will add test in the winodw
        :param START_GENERATE:
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        START_GENERATE.setWindowTitle(_translate("START_GENERATE", "Maze generator - Maze solver configuration"))
        self.label.setText(_translate("START_GENERATE", "Maze generator - Maze Solver"))
        self.label_2.setText(_translate("START_GENERATE", "Maze size in x :"))
        self.label_3.setText(_translate("START_GENERATE", "Maze size in y :"))
        self.label_4.setText(_translate("START_GENERATE", "Configuration"))
        self.INSTANT_PATH.setText(_translate("START_GENERATE", "Instant pathfinding"))
        self.BEST_PATH.setText(_translate("START_GENERATE", "Show best path"))
        self.PATH_SEARCH.setText(_translate("START_GENERATE", "Show path search"))
        self.START_GENERATION.setText(_translate("START_GENERATE", "Start generate"))
        self.label_5.setText(_translate("START_GENERATE", "Maze seed"))

    def start(self) -> None:
        """
        This function will start the maze solver program
        :return None
        """
        # get the configuration for maze

        maze_size_x = self.MAZE_SIZE_X.value()
        maze_size_y = self.MAZE_SIZE_Y.value()
        seed = self.MAZE_SEED.value()
        instant_path = self.INSTANT_PATH.isChecked()
        best_path = self.BEST_PATH.isChecked()
        path_search = self.PATH_SEARCH.isChecked()

        START_GENERATE.close()

        # due to a conflict between pyqt5 and matplotlib i must write in a file the argument
        # start a new python for the maze window that will get the information for the configuration
        # of the maze

        conf: tuple = (maze_size_x,
                       maze_size_y,
                       seed,
                       instant_path,
                       best_path,
                       path_search)

        with open("conf.pkl", "wb") as f:
            pickle.dump(conf, f, pickle.HIGHEST_PROTOCOL)
            f.close()

        os_name = os.name
        if os_name == "nt":
            os.system("start python maze_window.py")
        else:
            os.system("python3 maze_window.py")

        sys.exit(app.exec_())


if __name__ == "__main__":
    # create the application
    app = QtWidgets.QApplication(sys.argv)
    START_GENERATE = QtWidgets.QMainWindow()
    # create class
    ui = StartGenerate()
    # setup the window
    ui.setup_gui(START_GENERATE)
    # start the window
    START_GENERATE.show()
    # exit window
    sys.exit(app.exec_())
