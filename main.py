import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow

import reformat_core
import UI_untitled as gui
import picture


class mainform(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 美化参数d
        self.beautify()
        # 界面属性设置
        self._translate = QtCore.QCoreApplication.translate
        self.reformat = reformat_core.reformat_class()
        self.word_reformat = reformat_core.word_dispose()
        self.input_select.clicked.connect(self.open_file)
        self.output_select.clicked.connect(self.save_file)
        self.close_button.clicked.connect(self.close)
        self.mini.clicked.connect(self.showMinimized)
        self.begin.clicked.connect(self.format_begin)
        self.link_txwh.clicked.connect(self.link_Txwh)
        self.link_github.clicked.connect(self.link_Github)
        # 单选按钮选择时图片的切换函数调用
        self.format1.toggled.connect(self.qradio_state)
        # 设置默认选择的单选框
        self.word.setChecked(True)
        self.format1.setChecked(True)

    def beautify(self):
        # self.setWindowOpacity(0.96)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏顶栏
        self.setWindowTitle("YoudaoRe")  # 设置名称
        self.setStyleSheet("#MainWindow{background-color:white}")  # 背景色
        self.setWindowIcon(QIcon(":/images/icon.png"))  # 图标
        self.setFixedSize(self.width(), self.height())
        self.icon_label.setScaledContents(True)
        self.close_button.setStyleSheet('''QPushButton{background:#F76677;border-radius:10px;}
        QPushButton:hover{background:red;}''')
        self.mini.setStyleSheet('''QPushButton{background:#E5E5E5;border-radius:10px;}
        QPushButton:hover{background:#87F361;}''')
        self.input_select.setStyleSheet('''QPushButton{background:white;border:none;}''')
        self.output_select.setStyleSheet('''QPushButton{background:white;border:none;}''')
        self.begin.setStyleSheet('''QPushButton{background:#E5E5E5 url(:/images/begin.png);border-radius:35px;}
        QPushButton:pressed{background:#F6F6F6;}''')
        self.input.setStyleSheet('''QLineEdit{border:1px solid gray;border-radius:20px;padding:5px;}''')
        self.output.setStyleSheet('''QLineEdit{border:1px solid gray;border-radius:20px;padding:5px;}''')
        self.groupBox.setStyleSheet('''QGroupBox{border:1px solid gray;border-radius:12px;}''')
        self.groupBox_2.setStyleSheet('''QGroupBox{border:1px solid gray;border-radius:12px;}''')
        self.link_txwh.setStyleSheet('''QPushButton{background:white;border:none;}
        QPushButton:hover{background:#F6F6F6;}''')
        self.link_github.setStyleSheet('''QPushButton{background:white;border:none;}
        QPushButton:hover{background:#F6F6F6;}''')

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def qradio_state(self):
        if self.format1.isChecked():
            self.sample_show.setPixmap(QtGui.QPixmap(":/images/sample.png"))
        else:
            self.sample_show.setPixmap(QtGui.QPixmap(":/images/sample2.png"))

    def open_file(self):
        # 文本编辑框显示路径
        self.openfile_name = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', '', 'txt files(*.txt)')
        self.input.setText(self._translate("MainWindow", self.openfile_name[0]))     

    def save_file(self):
        # 文本编辑框显示路径
        if self.buttonGroup_2.checkedId() == 3:
            self.savefile_name = QtWidgets.QFileDialog.getSaveFileName(self, '保存文件', '', 'Docs(*.docx)')
        else:
            self.savefile_name = QtWidgets.QFileDialog.getSaveFileName(self, '保存文件', '', 'txt files(*.txt)')
        self.output.setText(self._translate("MainWindow", self.savefile_name[0]))

    def link_Txwh(self):
        QDesktopServices.openUrl(QtCore.QUrl("http://txwh.blog.cn"))

    def link_Github(self):
        QDesktopServices.openUrl(QtCore.QUrl("https://github.com/TaXue-DuBa"))

    def format_begin(self):
        # 调用文件转换函数
        self.reformat.switch_file(self.input.text())
        # 获取单选按钮的ID号进行判断用户选择了什么选项
        if self.select_format.checkedId() == 1 and self.buttonGroup_2.checkedId() == 3:
            self.word_reformat.word_create()
            self.reformat.reformat(self.input.text(), self.output.text())
            self.word_reformat.word_write(self.output.text())
        if self.select_format.checkedId() == 1 and self.buttonGroup_2.checkedId() == 4:
            self.reformat.reformat(self.input.text(), self.output.text())
            self.reformat.reformat_done()
        if self.select_format.checkedId() == 2 and self.buttonGroup_2.checkedId() == 3:
            self.word_reformat.word_create()
            self.reformat.reformat_second(self.input.text(), self.output.text())
            self.word_reformat.word_write_second(self.output.text())
        if self.select_format.checkedId() == 2 and self.buttonGroup_2.checkedId() == 4:
            self.reformat.reformat_second(self.input.text(), self.output.text())
            self.reformat.reofrmat_done_second()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = mainform()
    ui.show()
    sys.exit(app.exec_())
