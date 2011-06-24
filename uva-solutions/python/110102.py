#!/usr/bin/python
#Solution to Minesweeper
#URL: http://www.programming-challenges.com/pg.php?page=downloadproblem&probid=110102&format=html
#Author: Sidharth Shah

result = []

def init(r,c):
	"""
	Initialized empty grid
	"""
	for i in range(r):
		temp = []
		for j in range(c):
			temp.append(0)
		result.append(temp)
		
def update_count(x,y,r,c):
	"""
	Update the count while checking for overflow and underflow
	"""
	if((x-1) >= 0 and (y+1) < c):
		result[x-1][y+1] += 1
			
	if((x-1) >= 0):
		result[x-1][y] += 1
	
	
	if((x-1) >= 0 and (y-1) >= 0):
		result[x-1][y-1] += 1
	
	if((x+1) < r and (y+1) < c):
		result[x+1][y+1] += 1
	
	if((x+1) < r):
		result[x+1][y] += 1

	if((x+1) < r and (y-1) >= 0):
		result[x+1][y-1] += 1
	
	if((y -1) >= 0):
		result[x][y-1] += 1
	
	if((y + 1) < c):
		result[x][y+1] +=1 

def minesweep(r,c,board):
	"""
	This is used to solve minesweep 
	"""
	init(r,c)
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == "*":
				update_count(i,j,r,c)
	
	fresult = [] 
	
	for i in range(len(board)):
		temp = []
		for j in range(len(board[i])):
			if board[i][j] == "*":
				temp.append("*")
			else:
				temp.append(str(result[i][j]))
		fresult.append(temp)
	
	
	for i in range(len(fresult)):
		print "".join(fresult[i])
		
if __name__ == "__main__":
	file = open("110102-input.txt")	
	eachLine = file.readline()
	i = 0 
	board = [] 
	r,c = 0,0
	while eachLine:
		eachLine = eachLine.strip()
		
		if(i == 0):
			if len(board) != 0:				
				minesweep(r,c,board)
			r,c = map(int,eachLine.split())
			board = []
			i = r
		else:
			i -= 1
			board.append(eachLine) 
			
		eachLine = file.readline()
	minesweep(r,c,board)
