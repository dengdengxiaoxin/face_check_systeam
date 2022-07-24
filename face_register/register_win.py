from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import numpy as np
import cv2

from support import face_detect
from .ui_face_register import Ui_Dialog
from support import face_tools


class camera_show_thread(QtCore.QThread):
    img_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super(camera_show_thread, self).__init__()
        self.face_detect = face_detect()
        # self.cap= cv2.VideoCapture(0)
        self.flag = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened() and self.flag:
            flag, image = self.cap.read()
            show = cv2.resize(image, (640, 480))
            # show = self.face_detect.retrun_img(show)
            self.img_signal.emit(show)
        self.cap.release()

    def stop(self):
        self.flag = False


class register_window(QtWidgets.QDialog, Ui_Dialog):
    back_signal = pyqtSignal()
    quit_signal = pyqtSignal()

    def __init__(self):
        super(register_window, self).__init__()
        self.my_thread = camera_show_thread()
        self.mutex = threading.Lock()
        self.pre_image = np.ndarray
        self.save_image = np.ndarray
        self.face_tool = face_tools()
        self.setupUi(self)
        self.slot_init()
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_6.setEnabled(False)

    def slot_init(self):

        self.my_thread.img_signal.connect(self.show_img)
        self.pushButton.clicked.connect(self.quit)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.submit_info)
        self.pushButton_4.clicked.connect(self.preview_img)
        self.pushButton_5.clicked.connect(self.open_camera)
        self.pushButton_6.clicked.connect(self.close_camera)

    def show_img(self, frame):
        if self.my_thread.flag:
            frame = cv2.line(frame, (154, 0), (154, 479), (0, 0, 255), 2)
            frame = cv2.line(frame, (524, 0), (524, 479), (0, 0, 255), 2)
            show = frame
            self.mutex.acquire()
            self.pre_image = show[0:479, 159:519]
            self.mutex.release()
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        else:
            self.label.clear()

    def preview_img(self):
        self.mutex.acquire()
        self.save_image = self.pre_image
        frame = self.pre_image
        self.mutex.release()
        show = cv2.resize(frame, (180, 240))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.pushButton_3.setEnabled(True)

    def submit_info(self):
        name = self.lineEdit.text()
        class_no = self.lineEdit_2.text()
        no = self.lineEdit_3.text()
        self.mutex.acquire()
        frame = self.save_image
        self.mutex.release()
        # if len(name) and len(class_no) and (len(no) == 10):
        if len(name) and len(class_no) and len(no):
            self.face_tool.save_Face_local(name, class_no, no, frame)
            self.label_7.setStyleSheet("color:blue")
            self.label_7.setText("录入成功")

        else:
            self.label_7.setStyleSheet("color:red")
            self.label_7.setText("输入错误")

    def open_camera(self):
        self.my_thread.flag = True
        self.my_thread.start()
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def close_camera(self):
        self.my_thread.stop()
        self.label_2.clear()

        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(False)

    def back(self):
        if self.my_thread.isRunning():
            self.my_thread.stop()
        self.close()
        self.back_signal.emit()

    def quit(self):
        if self.my_thread.isRunning():
            self.my_thread.stop()
        self.close()
        self.quit_signal.emit()
