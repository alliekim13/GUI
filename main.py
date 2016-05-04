from PyQt4.QtCore import *
from PyQt4 import QtGui
import csv
import datetime
import design2
import sys
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
	self.ax1f1.plot(np.random.rand(100))
	print "Initializing..."    
	self.actionProject_Settings.triggered.connect(self.openDialog)
	self.dialog = PopupDialog()
	self.dialog.pushButton.clicked.connect(self.selectFile)
	self.dialog.buttonBox.accepted.connect(self.save_settings)
	self.timer = QTimer()
	self.logTimer = QTimer()
	self.timer.timeout.connect(self.read)
	self.logTimer.timeout.connect(self.logEnd)
	self.buttonState = False
	self.addmpl(self.fig1)
	self.logValid = False

    def openDialog(self):
	print "Opening dialog box"
	self.dialog.exec_()

    def selectFile(self):
	print "Selecting file..."
	self.dialog.lineEdit_4.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

    def save_settings(self):
	print "Saving data..."
	self.fileName = self.dialog.lineEdit.text()
	self.fileName += ".csv"
	self.logRate = self.dialog.lineEdit_2.text()
	self.logDuration = self.dialog.lineEdit_3.text()
	self.filePath = self.dialog.lineEdit_4.text()
	if not self.checkData():
	    print "Data invalid"
	    self.logValid = False
	    self.fileName = ""
	    self.logRate = ""
	    self.logRate = ""
	    self.logDuration = ""
	    self.filePath = ""
	    self.show_saveSettingsError()
	else:
	    self.logValid = True
	    self.outputFilepath = os.path.join(str(self.filePath), str(self.fileName))
	    print self.outputFilepath
	self.debug_settings()
    
    def debug_settings(self):
	print "Filename: " + self.fileName
	print "Log rate: " + self.logRate
	print "Log duration: " + self.logDuration
	print "File path: " + self.filePath
    
    def checkData(self):
	flag = True
	print "In check data"
	self.errorStr = ""
	if not self.fileName:
	    self.errorStr += "Enter a file name!\n"
	    flag = False
	if not self.filePath:
	    self.errorStr += "Enter a file path!\n"
	    flag = False
	if not self.isNumber(str(self.logRate)):
	    print "Log rate invalid\n"
	    self.errorStr += "Enter a number for sample rate!\n"
	    flag = False
	if not self.isNumber(str(self.logDuration)):
	    print "Log duration invalid\n"
	    self.errorStr += "Enter a number for log duration!\n"
	    flag = False
	return flag

    def show_saveSettingsError(self):
	error = QtGui.QErrorMessage()
	error.showMessage(self.errorStr)
	error.exec_()

    def addmpl(self, fig):
	#print self.outputFilepath
	self.canvas = FigureCanvas(fig)
	self.mplvl.addWidget(self.canvas)
	self.canvas.draw()
 
    def start_log(self):
	if self.buttonState is False:
	    self.buttonState = True
	    self.startButton.setText("Stop")
	    self.timer.start(int(self.logRate)*1000)
	    self.logTimer.start(int(self.logDuration)*1000)
	elif self.buttonState is True:
	    self.buttonState = False
	    self.startButton.setText("Start")
	    self.timer.stop()
	    self.logTimer.stop()
	'''
	#controls logging using timer
	self.start_time = datetime.datetime.now()
	#enter logging rate in this statement
	self.timer.start(int(self.logRate)*1000)
	self.logTimer.start(int(self.logDuration)*1000)
	'''

    def logEnd(self):
	self.timer.stop()
	self.buttonState = False
	self.startButton.setText("Start")

    def read(self):
	#function that gets called when qtimer expires
	#replace this line with code to do readouts
	reading = random.random()
	print reading
	self.lcdNumber_2.display(reading)
	self.dataloglist.addItem(str(reading))
	dt = datetime.datetime.now()
	dt.strftime("%Y-%m-%d %H:%M:%S.%f")
	row = [dt, reading]
	with open (str(self.outputFilepath), 'a') as f:
	    writer = csv.writer(f)
	    writer.writerow(row)
	f.close()
	'''
	except:
	    print ValueError
	    print "Need a valid file path!"
	'''
	#self.timer.start(100)

    def new_project(self):
	print "Start a new project"

    def browse_folder(self):
	self.listWidget.clear()
	directory = QtGui.QFileDialog.getExistingDirectory(self, "Pick a folder")
	if directory:
	    for file_name in os.listdir(directory):
		self.listWidget.addItem(file_name)

    def isNumber(self, teststr):
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
