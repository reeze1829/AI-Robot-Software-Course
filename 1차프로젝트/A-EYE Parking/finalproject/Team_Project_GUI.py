from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from pathlib import Path
import os

class MainWindow(QWidget):
    capture_clicked = pyqtSignal()  # 화면 캡처(번호판 인식)
    logic_clicked = pyqtSignal()    # 함수 실행(DB 대조 및 안내)
    exit_clicked = pyqtSignal()     # 전체 종료

    def __init__(self):
        super().__init__()
        # 파일의 위치를 기준으로 경로 설정
        self._base_path = Path(__file__).parent
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("주차관리 시스템")
        self.setFixedSize(600, 800)
        self._set_background() #상단의 주차장 이미지 설정
        self._set_button() # 버튼들 설정(캡쳐, 함수 작동, 전체 종료)
        self._set_message_box() #하단의 자막 박스 설정

    def _set_background(self):
        self.bg_label = QLabel(self)
        map_path = (self._base_path / 'test10.png').as_posix()
        pixmap = QPixmap(map_path)

        if pixmap.isNull():
            print(f"이미지 로드 실패: {map_path}")

        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(50, 20, 500, 350)

    def _set_button(self):
        btn_style = "QPushButton { font-size: 16px; font-weight: bold; }"
        self.btn_cap = QPushButton("화면 캡쳐",self)
        self.btn_cap.setGeometry(50, 400, 150, 60)
        self.btn_cap.setStyleSheet(btn_style)
        self.btn_cap.clicked.connect(self.capture_clicked.emit)

        self.btn_run = QPushButton("함수 실행",self)
        self.btn_run.setGeometry(225, 400, 150, 60)
        self.btn_run.setStyleSheet(btn_style)
        self.btn_run.clicked.connect(self.logic_clicked.emit)

        self.btn_exit = QPushButton("전체 종료",self)
        self.btn_exit.setGeometry(400, 400, 150, 60)
        self.btn_exit.setStyleSheet(btn_style)
        self.btn_exit.clicked.connect(self.exit_clicked.emit)

    def _set_message_box(self):
        self.msg_label = QLabel("시스템 대기 중...",self)
        self.msg_label.setGeometry(50, 500, 500, 250)
        self.msg_label.setStyleSheet("""
            background-color: #000000;
            color: #FFFFFF;
            border: 2px solid #555555;
            padding: 20px;
        """)
        self.msg_label.setFont(QFont("맑은 고딕", 14))

    def update_message(self, text):
        self.msg_label.setText(text)
