from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget,QHBoxLayout, QVBoxLayout, QPushButton, QStatusBar, QLineEdit
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt6.QtGui import QIntValidator
# only needed for access to command line
import sys
import misc
from background import worker
import numpy as np


# subclass QMainWindow to customize your application's main window


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		layout = QGridLayout()
		self.word_length = 9

		self.numbers = ["5", "3", "", "", "7", "", "", "", "",
						"6", "", "", "1", "9", "5", "", "", "",
						"", "9", "8", "", "", "", "", "6", "",
						"8", "", "", "", "6", "", "", "", "3",
						"4", "", "", "8", "", "3", "", "", "1",
						"7", "", "", "", "2", "", "", "", "6",
						"", "6", "", "", "", "", "2", "8", "",
						"", "", "", "4", "1", "9", "", "", "5",
						"", "", "", "", "8", "", "", "7", "9"]

		#self.numbers=["" for i in range(self.word_length*9)]

		self.positions = [(i, j) for i in range(self.word_length) for j in range(9)]
		
		for position, number in zip(self.positions, self.numbers):
			stylesheet = self.formatCell(position, "red")

			ql = QLineEdit(number)
			ql.setMaxLength(1)
			ql.setAlignment(Qt.AlignmentFlag.AlignCenter)

			ql.setStyleSheet(stylesheet)
			ql.setValidator(QIntValidator())
			layout.addWidget(ql, *position)

		layout.setHorizontalSpacing(0)
		layout.setVerticalSpacing(0)

		self.widget = QWidget()
		self.widget.setLayout(layout)

		vlayout = QVBoxLayout()

		vlayout.addWidget(self.widget)
		hlayout = QHBoxLayout()
		self.button = QPushButton("solve")
		self.button.clicked.connect(self.solve_sudoku)

		
		hlayout.addWidget(self.button)

		buttonClear=QPushButton("Clear") 
		buttonClear.clicked.connect(self.clear_grid)
		hlayout.addWidget(buttonClear)
		bwidget=QWidget()
		bwidget.setLayout(hlayout)
		
		vlayout.addWidget(bwidget)
		widget1 = QWidget()
		widget1.setLayout(vlayout)
		self.statusBar = QStatusBar()
		self.setStatusBar(self.statusBar)
		
		self.setCentralWidget(widget1)
	
	def clear_grid(self):
		for position in self.positions:
			self.widget.layout().itemAtPosition(*position).widget().setText("")
			self.widget.layout().itemAtPosition(*position).widget().setStyleSheet(self.formatCell(position, "red"))

	def formatCell(self, position, color):
		stylesheet = "background: white; color: "+color+"; border: 2px solid; border-color: grey;"
		if position[0] % 3==0:
			stylesheet += " border-top-color: blue;"
		if position[0] % 3==2:
			stylesheet += "border-bottom-color: blue;"		

		if position[1] %3 == 0:
			stylesheet += " border-left-color: blue;"
		if position[1] % 3 == 2:
			stylesheet += " border-right-color:blue; "
		return stylesheet

	def solve_sudoku(self):
		
		#step 1: compute numbers
		self.numbers=[]
		for position in self.positions:
			self.numbers.append(self.widget.layout().itemAtPosition(*position).widget().text())

		self.button.setEnabled(False)
		#for lay in self.widget.layout():
		#	self.numbers.append(lay.widget().text)
		# Step 2: Create a QThread object
		self.thread = QThread()
		# Step 3: Create a worker object
		self.worker = worker()
		self.worker.numbers = self.numbers
		# Step 4: Move worker to the thread
		self.worker.moveToThread(self.thread)
		# Step 5: Connect signals and slots
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.worker.finished.connect(self.endReport)
		self.thread.finished.connect(self.thread.deleteLater)
		self.worker.progress.connect(self.reportProgress)
		# Step 6: Start the thread
		self.thread.start()

	def endReport(self,totalTry,totalCombi):
		self.button.setEnabled(True)
		self.statusBar.showMessage("total try : "+ str(totalTry)+" total computed : "+str(totalCombi))
	
	def reportProgress(self,x,y,number):
		self.widget.layout().itemAtPosition(y,x).widget().setText(str(number))
		self.widget.layout().itemAtPosition(y,x).widget().setStyleSheet(self.formatCell((y,x), "blue"))
						
		
# You need one (and only one QApplication instance per application.
# Pass in sys.argv to allow command  leine arguement for your app.
# If you know you won't use command line arguments QApplication([])


app = QApplication(sys.argv)

# create a Qt widget, which will be our window

window = MainWindow()
window.show()  # IMPORTANT!!!!!!  Windows are hidden by default

# Start the event loop

app.exec()


# your app won't reach here until you  exit and the loop has stopped
