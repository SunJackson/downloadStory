# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloadStory.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1150, 750)
        MainWindow.setMaximumSize(QtCore.QSize(1150, 750))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../files/bitbug_favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(520, 30, 141, 111))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("files/download.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 160, 1071, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputSearch = QtWidgets.QLineEdit(self.layoutWidget)
        self.inputSearch.setObjectName("inputSearch")
        self.horizontalLayout.addWidget(self.inputSearch)
        self.searchType = QtWidgets.QComboBox(self.layoutWidget)
        self.searchType.setEnabled(True)
        self.searchType.setEditable(False)
        self.searchType.setObjectName("searchType")
        self.horizontalLayout.addWidget(self.searchType)
        self.search = QtWidgets.QPushButton(self.layoutWidget)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 680, 1071, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBoxProxy = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBoxProxy.setObjectName("checkBoxProxy")
        self.horizontalLayout_3.addWidget(self.checkBoxProxy)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.spinBoxThread = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBoxThread.setMinimum(1)
        self.spinBoxThread.setMaximum(100)
        self.spinBoxThread.setObjectName("spinBoxThread")
        self.horizontalLayout_3.addWidget(self.spinBoxThread)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.savePath = QtWidgets.QLineEdit(self.layoutWidget1)
        self.savePath.setObjectName("savePath")
        self.horizontalLayout_3.addWidget(self.savePath)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.progressBarDownload = QtWidgets.QProgressBar(self.layoutWidget1)
        self.progressBarDownload.setProperty("value", 24)
        self.progressBarDownload.setObjectName("progressBarDownload")
        self.horizontalLayout_3.addWidget(self.progressBarDownload)
        self.startDownload = QtWidgets.QPushButton(self.layoutWidget1)
        self.startDownload.setObjectName("startDownload")
        self.horizontalLayout_3.addWidget(self.startDownload)
        self.stopDownload = QtWidgets.QPushButton(self.layoutWidget1)
        self.stopDownload.setObjectName("stopDownload")
        self.horizontalLayout_3.addWidget(self.stopDownload)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 200, 251, 471))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(310, 200, 811, 471))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(8)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.CustomDashLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setKerning(True)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.layoutWidget.raise_()
        self.textBrowser.raise_()
        self.tableWidget.raise_()
        self.label.raise_()
        self.layoutWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小说下载工具（by SunJackson）"))
        self.search.setText(_translate("MainWindow", "搜索"))
        self.checkBoxProxy.setText(_translate("MainWindow", "使用代理"))
        self.label_2.setText(_translate("MainWindow", "线程数："))
        self.label_3.setText(_translate("MainWindow", "存储路径："))
        self.pushButton.setText(_translate("MainWindow", "打开"))
        self.label_4.setText(_translate("MainWindow", "下载进度："))
        self.startDownload.setText(_translate("MainWindow", "选中下载"))
        self.stopDownload.setText(_translate("MainWindow", "停止"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "搜索结果"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "搜索源"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "总章节数"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "最新章节"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "章节详情"))