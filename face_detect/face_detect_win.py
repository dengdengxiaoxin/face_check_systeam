import cv2
import numpy as np
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from .face_detect import Ui_Dialog
from support.face_detect import face_detect
import datetime

class detect_thread(QtCore.QThread):
    img_show_signal = pyqtSignal(np.ndarray)
    detect_result_signal = pyqtSignal(str, str, str, np.ndarray)

    def __init__(self):
        super(detect_thread, self).__init__()
        self.face_detect = face_detect()
        self.flag = True
        self.result_send_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened() and self.flag:
            flag, image = cap.read()
            show = cv2.resize(image, (640, 480))
            name, class_no, no, face_img = self.face_detect.retrun_img(show)
            self.img_show_signal.emit(show)
            if (name != "Unknown") and self.result_send_flag:
                self.detect_result_signal.emit(name, class_no, no, face_img)
        cap.release()

    def stop(self):
        self.flag = False


class delay_thread(QtCore.QThread):
    delay_end_signal = pyqtSignal()

    def __init__(self):
        super(delay_thread, self).__init__()
        self.flag = False

    def run(self):
        if self.flag:
            time.sleep(2)
            self.flag = False
            self.delay_end_signal.emit()

    def stop(self):
        self.flag = False


class face_detect_window(QtWidgets.QDialog, Ui_Dialog):
    exit_signal = pyqtSignal()
    register_signal = pyqtSignal()
    check_result_signal = pyqtSignal(list)
    check_signal = pyqtSignal()

    def __init__(self):
        super(face_detect_window, self).__init__()
        self.detect_thread = detect_thread()
        self.delay_thread = delay_thread()
        self.known_names = []
        self.known_class_nos = []
        self.known_nos = []

        self.setupUi(self)
        self.slot_init()

        time_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setText(time_text)

    def slot_init(self):

        self.detect_thread.img_show_signal.connect(self.show_img)
        self.detect_thread.detect_result_signal.connect(self.show_detect_result)
        self.delay_thread.delay_end_signal.connect(self.result_clear)
        self.pushButton.clicked.connect(self.open_camera)
        self.pushButton_2.clicked.connect(self.close_camera)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_4.clicked.connect(self.register_face)
        self.pushButton_5.clicked.connect(self.result)

    def show_img(self, frame):
        if self.detect_thread.flag:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def show_detect_result(self, name, class_no, no, face_img):
        # if name != "Unknown" and name not in self.known_names:
        if (name != "Unknown") and self.detect_thread.flag:
            if name not in self.known_names:
                self.known_names.append(name)
                self.known_class_nos.append(class_no)
                self.known_nos.append(no)

                self.lineEdit.setText(name)
                self.lineEdit_2.setText(class_no)
                self.lineEdit_3.setText(no)
                pre_img = cv2.resize(face_img, (180, 240))
                # show_1 = cv2.cvtColor(pre_img, cv2.COLOR_BGR2RGB)
                show = pre_img
                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
                self.label_9.setAlignment(Qt.AlignCenter)
                self.label_9.setPixmap(QtGui.QPixmap.fromImage(showImage))
                self.label.setStyleSheet("color:blue")
                self.label.setAlignment(Qt.AlignCenter)
                self.label.setText("签到成功")

                self.delay_thread.flag = True
                self.delay_thread.start()

            elif not self.delay_thread.flag:
                self.lineEdit.setText(name)
                self.lineEdit_2.setText(class_no)
                self.lineEdit_3.setText(no)
                pre_img = cv2.resize(face_img, (180, 240))
                # show_1 = cv2.cvtColor(pre_img, cv2.COLOR_BGR2RGB)
                show = pre_img
                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
                self.label_9.setAlignment(Qt.AlignCenter)
                self.label_9.setPixmap(QtGui.QPixmap.fromImage(showImage))
                self.label.setStyleSheet("color:blue")
                self.label.setAlignment(Qt.AlignCenter)
                self.label.setText("已签到成功，请勿重复")
                self.delay_thread.flag = True
                self.delay_thread.start()

        # else:
        #     self.lineEdit.clear()
        #     self.lineEdit_2.clear()
        #     self.lineEdit_3.clear()
        #     self.label.clear()
        #     self.label_9.clear()

    def open_camera(self):
        self.detect_thread.flag = True
        self.detect_thread.start()

        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)

    def close_camera(self):
        self.detect_thread.stop()

        self.label.clear()
        self.label_2.clear()
        self.label_7.clear()
        self.label_9.clear()

        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)

    def result_clear(self):
        self.label.clear()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.label_7.clear()
        self.label_9.clear()

    def exit(self):
        self.detect_thread.stop()
        self.close()
        self.label_2.clear()
        self.exit_signal.emit()

    def register_face(self):
        self.detect_thread.stop()
        self.label_2.clear()
        self.close()
        self.register_signal.emit()

    def result(self):
        self.detect_thread.stop()
        self.label_2.clear()
        self.close()
        self.check_result_signal.emit(self.known_names)
        self.check_signal.emit()