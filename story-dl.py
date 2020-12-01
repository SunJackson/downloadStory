#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QFileDialog, QMessageBox
import os
import sys
import base64


from story_dl.downloadStory import Ui_MainWindow
from story_dl.function import check_path_exists
from story_dl.handlerProcess import getSearchResultThread, downloadStoryHandler

download_png_base64 = b'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'
download_png_base64_decode = base64.b64decode(download_png_base64)
windows_icon_base64 = b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABILAAASCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAigAAAP8AAAD2AAAA9gAAAPYAAAD2AAAA9gAAAPYAAAD2AAAA9gAAAPYAAAD2AAAA9gAAAPYAAAD2AAAA9gAAAPYAAAD2AAAA9gAAAPYAAAD2AAAA9gAAAP8AAACKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACMAAAA1AAAAEoAAABDAAAAQwAAAEMAAABDAAAAQwAAAEMAAABDAAAAQwAAAEMAAABDAAAAQwAAAEMAAABDAAAAQwAAAEMAAABDAAAAQwAAAEMAAABKAAAA1AAAAIwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFQAAABUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwAAACzAAAAswAAABwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAcAAAAtAAAAP8AAAD/AAAAtAAAABwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAALYAAADQAAAAxAAAAMQAAADQAAAAtgAAAB0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAAAAAAAAAAAABwAAAC2AAAA0QAAADIAAACaAAAAmgAAADIAAADRAAAAtgAAAB0AAAAAAAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAcAAAAtgAAANEAAAAzAAAAAAAAAJwAAACcAAAAAAAAADIAAADRAAAAtgAAABwAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAwAAAJkAAADSAAAANAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAADQAAADSAAAAmAAAAAIAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAABAAAAOwAAACsAAAAAAAAAAAAAAAAAAACcAAAAnAAAAAAAAAAAAAAAAAAAACoAAAA6AAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwAAACcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI0AAADEAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkAAADEAAAAjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAAAMQAAAAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACcAAAAnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAAMQAAACNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNAAAAxAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwAAACcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAxAAAAI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIwAAADnAAAAkgAAAI4AAACOAAAAjgAAAIwAAAA5AAAAAAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAAAAAAAA5AAAAjAAAAI4AAACOAAAAjgAAAJIAAADnAAAAjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZwAAAMQAAADEAAAAxAAAAMQAAADEAAAAwwAAAFMAAAAAAAAAAAAAAAAAAACcAAAAnAAAAAAAAAAAAAAAAAAAAFMAAADDAAAAxAAAAMQAAADEAAAAxAAAAMQAAABnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAAAACQAAAAkAAAAJAAAACQAAAAkAAAAIAAAAAgAAAAAAAAAAAAAAAAAAAJwAAACcAAAAAAAAAAAAAAAAAAAAAgAAAAgAAAAJAAAACQAAAAkAAAAJAAAACQAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACcAAAAnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwAAACcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACcAAAAnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwAAACcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnAAAAJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACVAAAAlQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADEAAAAyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8AAAD/AAAA/x//+P8f//j/H//4/x//+P8f//j/H//4/x/n+P8fw/j/H4H4/x8A+P8eAHj/HCQ4/xhmGP8Y5xj/H+f4/x/n+P8f5/j/H+f4/wDnAP8A5wD/AOcA///n////5////+f////n////5////+f////n////5////+f/8='
windows_icon_base64_decode = base64.b64decode(windows_icon_base64)


class emitting_str(QtCore.QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


def get_filse_path(filename):
    # 方法一（如果要将资源文件打包到app中，使用此法）
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path = os.path.join(bundle_dir, filename)
    if os.path.exists(path):
        return path
    else:
        return os.path.join('files', filename)
    # 方法二获取路径可以，但如果打包资源好像不行。
    # path = os.path.join(os.path.dirname(sys.argv[0]), filename)


class ControlBoard(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)
        self.set_default()
        self.search_name = ''
        self.download_stop_flag = False
        self.is_proxy = self.checkBoxProxy.isChecked()
        self.thread_num = int(self.spinBoxThread.text()) or 1
        sys.stdout = emitting_str(textWritten=self.output_written)
        sys.stderr = emitting_str(textWritten=self.output_written)
        self.parse_novel_source_res = []

    def set_default(self):
        self.setFixedSize(self.width(), self.height())
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        windows_icon =  QtGui.QPixmap()
        windows_icon.loadFromData(windows_icon_base64_decode)
        icon = QtGui.QIcon()
        icon.addPixmap(windows_icon, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        download_png = QtGui.QPixmap()
        download_png.loadFromData(download_png_base64_decode)
        self.label.setPixmap(download_png)
        self.pushButton.clicked.connect(self.open_file)
        self.startDownload.clicked.connect(self.start_download)
        self.stopDownload.clicked.connect(self.stop_download)
        self.search.clicked.connect(self.start_search)
        self.searchType.addItems(['全部', 'baidu', 'so'])
        self.savePath.setText(os.path.join(os.getcwd(), 'download'))
        self.inputSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBarDownload.setProperty("value", 0)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(4, 400)
        if self.stopDownload.isEnabled():
            self.stopDownload.setEnabled(False)
        if self.startDownload.isEnabled():
            self.startDownload.setEnabled(False)

    def open_file(self):
        open_file_dir = QFileDialog.getExistingDirectory()
        if open_file_dir:
            self.savePath.setText(open_file_dir)

    def show_message(self, message):
        QMessageBox.warning(self, "警告", message, QMessageBox.Cancel)

    def output_written(self, text):
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
        search_stats = res.get('search_stats', -1)
        if error_message:
            self.show_message(error_message)
            return
        self.parse_novel_source_res.append(res)
        row = res.get('row', 0)
        if self.tableWidget.rowCount() != row and search_stats == 1:
            self.tableWidget.setRowCount(row)

        if search_stats == 1:
            is_parse_index = res.get('is_parse_index', 0)

            if res.get('is_parse', 0):
                checkBox = QTableWidgetItem('【√已解析】{}'.format(res.get('title', '未知')))
            else:
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
            print('搜索到 {} 条结果'.format(is_parse_index + 1))
        elif search_stats == 0:
            print('搜索完成，请选择下载！')
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
        if not self.stopDownload.isEnabled():
            self.stopDownload.setEnabled(True)
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
        self.tableWidget.clearContents()
        self.GSRT.result_dict_signal.connect(self.set_item_table_widget)
        # 启动线程
        self.GSRT.start()
        if not self.startDownload.isEnabled():
            self.startDownload.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.show()
    sys.exit(app.exec_())
