# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(518, 533)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lbl_name_x = QLabel(self.centralwidget)
        self.lbl_name_x.setObjectName(u"lbl_name_x")
        self.lbl_name_x.setGeometry(QRect(10, 20, 81, 41))
        self.lbl_name_theta = QLabel(self.centralwidget)
        self.lbl_name_theta.setObjectName(u"lbl_name_theta")
        self.lbl_name_theta.setGeometry(QRect(10, 80, 81, 41))
        self.lbl_name_y = QLabel(self.centralwidget)
        self.lbl_name_y.setObjectName(u"lbl_name_y")
        self.lbl_name_y.setGeometry(QRect(10, 50, 81, 41))
        self.lbl_pos_y = QLabel(self.centralwidget)
        self.lbl_pos_y.setObjectName(u"lbl_pos_y")
        self.lbl_pos_y.setGeometry(QRect(90, 50, 81, 41))
        self.lbl_pos_x = QLabel(self.centralwidget)
        self.lbl_pos_x.setObjectName(u"lbl_pos_x")
        self.lbl_pos_x.setGeometry(QRect(90, 20, 81, 41))
        self.lbl_theta = QLabel(self.centralwidget)
        self.lbl_theta.setObjectName(u"lbl_theta")
        self.lbl_theta.setGeometry(QRect(90, 80, 81, 41))
        self.btn_open_teleop = QPushButton(self.centralwidget)
        self.btn_open_teleop.setObjectName(u"btn_open_teleop")
        self.btn_open_teleop.setGeometry(QRect(10, 124, 111, 31))
        self.btn_reset = QPushButton(self.centralwidget)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setGeometry(QRect(10, 162, 111, 31))
        self.btn_spawn = QPushButton(self.centralwidget)
        self.btn_spawn.setObjectName(u"btn_spawn")
        self.btn_spawn.setGeometry(QRect(10, 200, 111, 31))
        self.btn_go_to_goal = QPushButton(self.centralwidget)
        self.btn_go_to_goal.setObjectName(u"btn_go_to_goal")
        self.btn_go_to_goal.setGeometry(QRect(10, 352, 111, 31))
        self.btn_get_distance = QPushButton(self.centralwidget)
        self.btn_get_distance.setObjectName(u"btn_get_distance")
        self.btn_get_distance.setGeometry(QRect(10, 238, 111, 31))
        self.btn_start_maze = QPushButton(self.centralwidget)
        self.btn_start_maze.setObjectName(u"btn_start_maze")
        self.btn_start_maze.setGeometry(QRect(10, 389, 111, 31))
        self.input_goal_x = QLineEdit(self.centralwidget)
        self.input_goal_x.setObjectName(u"input_goal_x")
        self.input_goal_x.setGeometry(QRect(60, 277, 61, 31))
        self.input_goal_y = QLineEdit(self.centralwidget)
        self.input_goal_y.setObjectName(u"input_goal_y")
        self.input_goal_y.setGeometry(QRect(60, 315, 61, 31))
        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setGeometry(QRect(144, 470, 111, 31))
        self.progress_bar.setValue(24)
        self.lbl_mission_status = QLabel(self.centralwidget)
        self.lbl_mission_status.setObjectName(u"lbl_mission_status")
        self.lbl_mission_status.setGeometry(QRect(280, 464, 101, 41))
        self.text_log = QTextEdit(self.centralwidget)
        self.text_log.setObjectName(u"text_log")
        self.text_log.setGeometry(QRect(140, 18, 351, 441))
        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(370, 464, 121, 41))
        self.btn_cancel_action = QPushButton(self.centralwidget)
        self.btn_cancel_action.setObjectName(u"btn_cancel_action")
        self.btn_cancel_action.setGeometry(QRect(10, 426, 111, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(12, 285, 67, 17))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(12, 320, 67, 17))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbl_name_x.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac:X", None))
        self.lbl_name_theta.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac \uac01\ub3c4:", None))
        self.lbl_name_y.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac:Y", None))
        self.lbl_pos_y.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.lbl_pos_x.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.lbl_theta.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.btn_open_teleop.setText(QCoreApplication.translate("MainWindow", u"\uc218\ub3d9 \uc870\uc885", None))
        self.btn_reset.setText(QCoreApplication.translate("MainWindow", u"\uc6d4\ub4dc \ub9ac\uc14b", None))
        self.btn_spawn.setText(QCoreApplication.translate("MainWindow", u"\ub79c\ub364 \uc18c\ud658", None))
        self.btn_go_to_goal.setText(QCoreApplication.translate("MainWindow", u"\ubaa9\ud45c\ub85c \uc774\ub3d9", None))
        self.btn_get_distance.setText(QCoreApplication.translate("MainWindow", u"\uac70\ub9ac \uacc4\uc0b0", None))
        self.btn_start_maze.setText(QCoreApplication.translate("MainWindow", u"\ubbf8\ub85c \ubbf8\uc158 \uc2dc\uc791", None))
        self.lbl_mission_status.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30 \uc911...", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"\uae34\uae09\uc815\uc9c0", None))
        self.btn_cancel_action.setText(QCoreApplication.translate("MainWindow", u"\ubbf8\uc158 \ucde8\uc18c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ubaa9\ud45c X", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ubaa9\ud45c Y", None))
    # retranslateUi

