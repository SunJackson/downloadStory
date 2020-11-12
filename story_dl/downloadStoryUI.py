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
        MainWindow.setObjectName("小说下载工具(by SunJackson)")
        MainWindow.setEnabled(True)
        MainWindow.resize(1150, 750)
        MainWindow.setMaximumSize(QtCore.QSize(1150, 750))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(False)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(500, 30, 141, 111))
        self.label.setText("")

        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 170, 1081, 501))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBoxProxy = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBoxProxy.setObjectName("checkBoxProxy")
        self.horizontalLayout_3.addWidget(self.checkBoxProxy)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.spinBoxThread = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBoxThread.setMinimum(1)
        self.spinBoxThread.setMaximum(100)
        self.spinBoxThread.setObjectName("spinBoxThread")
        self.horizontalLayout_3.addWidget(self.spinBoxThread)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.savePath = QtWidgets.QLineEdit(self.layoutWidget)
        self.savePath.setObjectName("savePath")
        self.horizontalLayout_3.addWidget(self.savePath)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.progressBarDownload = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBarDownload.setProperty("value", 24)
        self.progressBarDownload.setObjectName("progressBarDownload")
        self.horizontalLayout_3.addWidget(self.progressBarDownload)
        self.startDownload = QtWidgets.QPushButton(self.layoutWidget)
        self.startDownload.setObjectName("startDownload")
        self.horizontalLayout_3.addWidget(self.startDownload)
        self.stopDownload = QtWidgets.QPushButton(self.layoutWidget)
        self.stopDownload.setObjectName("stopDownload")
        self.horizontalLayout_3.addWidget(self.stopDownload)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小说下载工具(by SunJackson)"))
        self.search.setText(_translate("MainWindow", "搜索"))
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
        self.checkBoxProxy.setText(_translate("MainWindow", "使用代理"))
        self.label_2.setText(_translate("MainWindow", "线程数："))
        self.label_3.setText(_translate("MainWindow", "存储路径："))
        self.pushButton.setText(_translate("MainWindow", "打开"))
        self.label_4.setText(_translate("MainWindow", "下载进度："))
        self.startDownload.setText(_translate("MainWindow", "选中下载"))
        self.stopDownload.setText(_translate("MainWindow", "停止"))