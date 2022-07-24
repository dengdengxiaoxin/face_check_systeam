import sys
from PyQt5 import QtWidgets

from face_register import register_window
from check_result import check_result_window
from face_detect import face_detect_window
from system_login import system_login_window

app = QtWidgets.QApplication(sys.argv)
MainWindow = system_login_window()
MainWindow1 = face_detect_window()
MainWindow2 = register_window()
MainWindow3 = check_result_window()
MainWindow.enter_signal.connect(MainWindow1.show)
MainWindow1.exit_signal.connect(MainWindow.show)
MainWindow1.register_signal.connect(MainWindow2.show)
MainWindow1.check_result_signal.connect(MainWindow3.get_result)
MainWindow1.check_signal.connect(MainWindow3.show)
MainWindow2.back_signal.connect(MainWindow1.show)
MainWindow2.quit_signal.connect(MainWindow.show)
MainWindow.setWindowTitle("app")
MainWindow.show()
sys.exit(app.exec_())
