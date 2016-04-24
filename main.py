from PyQt4.QtCore import *
from PyQt4 import QtGui
import sys
import design2
import projectsettings
import os
import random
import time
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
	FigureCanvasQTAgg as FigureCanvas,
	NavigationToolbar2QT as NavigationToolbar)
import numpy as np
#Ui_MainWindow, QMainWindow = loadUiType('window.ui')

class PopupDialog(QtGui.QDialog, projectsettings.Ui_Dialog):
    def __init__(self, parent=None):
	super(PopupDialog, self).__init__(parent)
	self.setupUi(self)

class ErrorDialog(QtGui.QErrorMessage):
    def __init__(self, parent=None):
	super(ErrorDialog, self).__init__(parent)
	self.setupUi(self)

class ExampleApp(QtGui.QMainWindow, design2.Ui_MainWindow):
    def __init__(self, parent=None):
	super(ExampleApp, self).__init__(parent)
	self.setupUi(self)
	self.actionNew.triggered.connect(self.new_project)
	self.startButton.clicked.connect(self.start_log)
	self.fig1 =Figure()
	self.ax1f1 = self.fig1.add_subplot(111)
	print "Initializing..."    
	self.actionProject_Settings.triggered.connect(self.openDialog)
	self.dialog = PopupDialog()
	self.dialog.pushButton.clicked.connect(self.selectFile)
	self.dialog.buttonBox.accepted.connect(self.save_data)
	self.timer = QTimer()
	self.timer.timeout.connect(self.read)
	self.buttonState = False
    def openDialog(self):
	print "Opening dialog box"
	self.dialog.exec_()

    def selectFile(self):
	print "Selecting file..."
	self.dialog.lineEdit_4.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

    def save_data(self):
	print "Saving data..."
	self.fileName = self.dialog.lineEdit.text()
	self.logRate = self.dialog.lineEdit_2.text()
	self.logDuration = self.dialog.lineEdit_3.text()
	self.filePath = self.dialog.lineEdit_4.text()
	print "Filename: " + self.fileName
	print "Log rate: " + self.logRate
	print "Log duration: " + self.logDuration
	print "File path: " + self.filePath
	if not self.checkData():
	    print "Data invalid"

    def checkData(self):
	flag = True
	print "In check data"
	self.errorStr = ""
	if not self.fileName:
	    self.errorStr += "Enter a file name!\n"
	    flag = False
	if not isNumber(repr(self.logRate)):
	    print "Log rate invalid\n"
	    self.errorStr += "Enter a number for sample rate!\n"
	    flag = False
	if not self.isNumber(repr(self.logDuration)):
	    print "Log duration invalid\n"
	    self.errorStr += "Enter a number for log duration!\n"
	    flag = False
	if flag is False:
	    self.show_saveDataError()
	    return False
	else:
	    return True

    def show_saveDataError(self):
	error = QtGui.QErrorMessage()
	error.showMessage(self.errorStr)
	error.exec_()

    def addmpl(self, fig):
	self.canvas = FigureCanvas(fig)
	self.mplvl.addWidget(self.canvas)
	self.canvas.draw()

    def start_log(self):
	if self.buttonState is False:
	    self.timer.start(100)
	    self.startButton.setText("Stop")
	    self.buttonState = True
	else:
	    self.timer.stop()
	    print "Stop!"
	    self.buttonState = False
	    self.startButton.setText("Start")

    def read(self):
	#replace this line with code to do readouts
	reading = random.random()
	print reading
	self.lcdNumber.display(reading)
	#self.startButton.setText("Stop")

    def get_value(self):
	#this function will get the values of the readings 
	print "Getting values"

    def new_project(self):
	print "Start a new project"

    def browse_folder(self):
	self.listWidget.clear()
	directory = QtGui.QFileDialog.getExistingDirectory(self, "Pick a folder")
	if directory:
	    for file_name in os.listdir(directory):
		self.listWidget.addItem(file_name)

def isNumber(teststr):
    try:
	float(teststr)
    except ValueError:
	return False
    return True

def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
