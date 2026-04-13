# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'teleop_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(334, 301)
        self.btn_up = QPushButton(Form)
        self.btn_up.setObjectName(u"btn_up")
        self.btn_up.setGeometry(QRect(120, 20, 91, 71))
        self.btn_right = QPushButton(Form)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(220, 110, 91, 71))
        self.btn_left = QPushButton(Form)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(20, 110, 91, 71))
        self.btn_down = QPushButton(Form)
        self.btn_down.setObjectName(u"btn_down")
        self.btn_down.setGeometry(QRect(120, 200, 91, 71))
        self.btn_stop = QPushButton(Form)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(120, 110, 91, 71))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_up.setText(QCoreApplication.translate("Form", u"Forward", None))
        self.btn_right.setText(QCoreApplication.translate("Form", u"Right", None))
        self.btn_left.setText(QCoreApplication.translate("Form", u"Left", None))
        self.btn_down.setText(QCoreApplication.translate("Form", u"Backward", None))
        self.btn_stop.setText(QCoreApplication.translate("Form", u"STOP", None))
    # retranslateUi

