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

							square0 = [work[0][0],work[0][1],work[0][2],
							work[1][0],work[1][1],work[1][2],
							work[2][0],work[2][1],work[2][2]]
							square1=[work[0][3],work[0][4],work[0][5],
							work[1][3],work[1][4],work[1][5],
							work[2][3],work[2][4],work[2][5]]
							square2=[work[0][6],work[0][7],work[0][8],
							work[1][6],work[1][7],work[1][8],
							work[2][6],work[2][7],work[2][8]]


							square3 = [work[3][0],work[3][1],work[3][2],
							work[4][0],work[4][1],work[4][2],
							work[5][0],work[5][1],work[5][2]]
							square4=[work[3][3],work[3][4],work[3][5],
							work[4][3],work[4][4],work[4][5],
							work[5][3],work[5][4],work[5][5]]
							square5=[work[3][6],work[3][7],work[3][8],
							work[4][6],work[4][7],work[4][8],
							work[5][6],work[5][7],work[5][8]]


							square6 = [work[6][0],work[6][1],work[6][2],
							work[7][0],work[7][1],work[7][2],
							work[8][0],work[8][1],work[8][2]]
							square7=[work[6][3],work[6][4],work[6][5],
							work[7][3],work[7][4],work[7][5],
							work[8][3],work[8][4],work[8][5]]
							square8=[work[6][6],work[6][7],work[6][8],
							work[7][6],work[7][7],work[7][8],
							work[8][6],work[8][7],work[8][8]]

							if (x<3 and y<3 and str(value) not in square0 or
								x<3 and y>=3 and y < 6 and str(value) not in square3 or
								x<3 and y>=6 and str(value) not in square6 or
								x>=3 and x<6 and y<3 and str(value) not in square1 or
								x>=3 and x<6 and y>=3 and y<6 and str(value) not in square4 or
								x>=3 and x<6 and y>=6 and str(value) not in square7 or
								x>=6 and y<3 and str(value) not in square2 or
								x>=6 and y>=3 and y<6 and str(value) not in square5 or
								x>=6 and y>=6 and str(value) not in square8):
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


	