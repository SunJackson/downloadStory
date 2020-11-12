#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui
import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QFileDialog, QMessageBox
import os

from story_dl.downloadStoryUI import Ui_MainWindow
from story_dl.function import check_path_exists
from story_dl.handlerProcess import getSearchResultThread, downloadStoryHandler


class EmittingStr(QtCore.QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class ControlBoard(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)

        self.set_default()
        self.search_name = ''
        self.download_stop_flag = False
        self.is_proxy = self.checkBoxProxy.isChecked()
        self.thread_num = int(self.spinBoxThread.text()) or 1
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.parse_novel_source_res = []

    def set_default(self):
        self.setFixedSize(self.width(), self.height())
        self.label.setPixmap(QtGui.QPixmap("./files/download.png"))
        self.pushButton.clicked.connect(self.open_file)
        self.startDownload.clicked.connect(self.start_download)
        self.stopDownload.clicked.connect(self.stop_download)
        self.search.clicked.connect(self.start_search)
        self.searchType.addItems(['全部', 'baidu', 'so'])
        self.savePath.setText(os.path.join(os.getcwd(), 'download'))
        self.inputSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBarDownload.setProperty("value", 0)

    def open_file(self):
        open_file_dir = QFileDialog.getExistingDirectory()
        if open_file_dir:
            self.savePath.setText(open_file_dir)

    def show_message(self, message):
        QMessageBox.warning(self, "警告", message, QMessageBox.Cancel)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def set_item_table_widget(self, res):
        """
        '搜索结果','源','章节数', '最新章节', '章节详情'
        :param data:
        :return:
        """
        error_message = res.get('error_message', {})
        if error_message:
            self.show_message(error_message)
            return
        self.parse_novel_source_res.append(res)
        row = res.get('row', 0)
        if self.tableWidget.rowCount() != row:
            self.tableWidget.setRowCount(row)
        is_parse_index = res.get('is_parse_index', 0)
        checkBox = QTableWidgetItem(res.get('title', '未知'))
        checkBox.setCheckState(Qt.Unchecked)
        self.tableWidget.setItem(is_parse_index, 0, checkBox)

        newItem = QTableWidgetItem(res.get('netloc', '未知'))
        self.tableWidget.setItem(is_parse_index, 1, newItem)

        newItem = QTableWidgetItem(str(len(res.get('result', []))))
        self.tableWidget.setItem(is_parse_index, 2, newItem)

        newItem = QTableWidgetItem(res.get('latest_chapter_name', '未知'))
        self.tableWidget.setItem(is_parse_index, 3, newItem)

        newItem = QTableWidgetItem('|'.join([x[0] for x in res.get('result', [])[:3] if res.get('result', [])]))
        self.tableWidget.setItem(is_parse_index, 4, newItem)
        QApplication.processEvents()

    def stop_download(self):
        self.DLSH.download_status =False
        self.DLSH.terminate()
        self.DLSH.wait()
        print("停止下载！")
        return None

    def download_process(self, res):
        status = res.get('status', None)
        if status:
            self.progressBarDownload.setProperty("value", float(status)*100)

    def start_download(self):
        self.is_proxy = self.checkBoxProxy.isChecked()
        self.thread_num = int(self.spinBoxThread.text()) or 1
        download_story_list = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 0)
            if item and item.checkState() == Qt.Checked:
                ouput_path = self.savePath.text()
                story_info = self.parse_novel_source_res[int(item.row())]
                netloc = story_info.get('netloc', '未知')
                chapter_res = story_info.get('result', [])
                check_path_exists(ouput_path)
                saved_path = os.path.join(ouput_path, '{}({}).txt'.format(self.search_name, netloc))
                if chapter_res:
                    msg = "总章节为 {};\n输入开始下载章节".format(len(chapter_res))
                    num, ok = QInputDialog.getInt(self, '下载章节确认', msg)
                    if ok and num >= 0:
                        if num > len(chapter_res):
                            self.show_message("输入章节数大于总数，请确认！")
                        else:
                            download_story_list.append([chapter_res[num:], saved_path])
        if download_story_list:
            self.DLSH = downloadStoryHandler(download_story_list, self.is_proxy, self.thread_num)
            # 启动线程
            self.DLSH.result_dict_signal.connect(self.download_process)
            self.DLSH.start()

    def start_search(self):
        self.search_name = self.inputSearch.text().strip()
        search_type = self.searchType.currentText()
        if not self.search_name:
            self.show_message('请输入小说名！')
            return None
        self.GSRT = getSearchResultThread(self.search_name, search_type)

        self.GSRT.result_dict_signal.connect(self.set_item_table_widget)
        # 启动线程
        self.GSRT.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.show()
    sys.exit(app.exec_())
