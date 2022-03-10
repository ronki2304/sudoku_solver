from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
import misc
import numpy as np


class worker(QObject):
	finished = pyqtSignal(int,int)
	progress = pyqtSignal(int,int,int)

	def run(self):
		self.total=0
		self.combi=0
		misc.log("long running")
		self.solve_sudoku1()
		self.finished.emit(self.total,self.combi)

	def solve_sudoku1(self):
		# first fill number with immutable one
		# then take on the first line the first empty one
		# increment one
		# check if the line is correct if not go to increment
		# check if the column is correct if not go to increment
		# check the square is correct if not go to increment
		# if increment <10 go to the next
		# if increment =10 go to the previous cell

		misc.log("fill with immutable one")
		immut = np.array(self.numbers).reshape(9, 9)

		# copy immut to the work one
		work = immut.copy()

		# coordonnée
		x = 0
		y = 0
		value = 1
		while (y < 9):

			while x < 9:
				misc.log("x:" + str(x) +" y:" + str(y))
				# check if it is an immutable one
				if (immut[y][x] != ""):
					misc.log("immuttable so skip")
					x += 1
					continue
				misc.log("not an immutable")
				# compute value
				while (value < 10):
					self.combi+=1
					# check line
					misc.log("check line")
					misc.log(" value is " + str(value))
					if str(value) in work[y]:
						misc.log("value present in the line next one")
						value += 1
					else:
						misc.log("value not present in the line")
						#work[y][x] = str(value)
						#self.progress.emit(x,y,value)
						
						
						
						#--------------------Columns------------------------
						#misc.log("now check column")
						
						
						if(str(value) in work[:, x]):
							misc.log("value present in the column")
							value += 1
						else:
							misc.log("value not present in the line")
							misc.log("now check column")

						#-------------------Square--------------------------

							if (str(value) not in work[(y//3)*3:(y//3)*3+3,(x//3)*3:(x//3)*3+3]):
								misc.log("everything is fine take value")
								work[y][x] = str(value)
								self.progress.emit(x,y,value)
								value = 1
								self.total+=1
								x += 1
								break
							else:
								value+=1
					
				# check if we need to go back
				if value==10:
					work[y][x] =""
					self.progress.emit(x,y,"")
					#compute how many cell go back we can face to a immutables
					x=x-1
					if (x<0):
						y=y-1
						x=8
						#rewind as much as possible
					while immut[y][x]!="":
						x=x-1
						if (x<0):
							y=y-1
							x=8
					try:
						value=int(work[y][x])
					except:
						misc.log("x: "+ str(x)+" y: "+str(y))
						misc.log(work)
						return
					continue
					
			y+=1
			x=0


	