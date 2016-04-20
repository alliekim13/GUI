from PyQt4.QtCore import *
from PyQt4 import QtGui
import sys
import design2
import projectsettings
import os
import random
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

class ExampleApp(QtGui.QMainWindow, design2.Ui_MainWindow):
    def __init__(self, parent=None):
	super(ExampleApp, self).__init__(parent)
	self.setupUi(self)
	self.actionNew.triggered.connect(self.new_project)
	self.startButton.clicked.connect(self.read)
	self.fig1 =Figure()
	self.ax1f1 = self.fig1.add_subplot(111)
	print "Initializing..."    
	self.actionProject_Settings.triggered.connect(self.openDialog)

    def openDialog(self):
	print "Opening dialog box"
	self.dialog = PopupDialog()
	self.dialog.exec_()
	print "Setup Ui"
	

    def save_data(self):
	print "Saving data..."

    def addmpl(self, fig):
	self.canvas = FigureCanvas(fig)
	self.mplvl.addWidget(self.canvas)
	self.canvas.draw()

    def read(self):
	print "Reading serial"
	reading = random.random()
	self.lcdNumber.display(reading)
	self.startButton.setText("Stop")

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
   

def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
