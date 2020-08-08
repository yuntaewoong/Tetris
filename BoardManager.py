import ConstValue
import pygame

from enum import IntEnum
class BoardState(IntEnum):
	EMPTY = 0
	WALL = 1
	SFILLED = 2
	ZFILLED = 3
	TFILLED = 4
	LFILLED = 5
	JFILLED = 6
	OFILLED = 7
	IFILLED = 8
#tetrimino가 쌓인 부분을 관리2

class BoardManager:
	__board = []
	__clearedLines = 0
	def __init__(self):
		for i in range(0,ConstValue.BOARDHEIGHT + ConstValue.EXTRABOARDHEIGHT):
			self.__board.append([])
			for j in range(0,ConstValue.BOARDWIDTH + ConstValue.EXTRABOARDWIDTH):
				#마지막줄은 Wall로 막혀있음
				if i == ConstValue.BOARDHEIGHT + ConstValue.EXTRABOARDHEIGHT - 1:
					self.__board[i].append(BoardState.WALL)
				#마지막줄 제외한 줄들은 좌우 끝에 1개씩 wall가 있음
				else:
					if j == 0 or j == ConstValue.BOARDWIDTH + ConstValue.EXTRABOARDWIDTH-1:
						self.__board[i].append(BoardState.WALL)
					else:
						self.__board[i].append(BoardState.EMPTY)
	def GetBoard(self):
		return self.__board
	def GetClearedLines(self):
		return self.__clearedLines
	#board에 mino를 쌓음
	def StackingMino(self,centerLocation,printInfo,color):
		for i in range(0,len(printInfo)):
			for j in range(0,len(printInfo[i])):
				if printInfo[i][j] == 1:
					if color == ConstValue.IMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.IFILLED
					elif color == ConstValue.LMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.LFILLED
					elif color == ConstValue.JMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.JFILLED
					elif color == ConstValue.SMINO_COLOR:
						print((i+centerLocation[0]-len(printInfo)//2,j+centerLocation[1]-len(printInfo)//2))
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.SFILLED
					elif color == ConstValue.ZMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.ZFILLED
					elif color == ConstValue.TMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.TFILLED
					elif color == ConstValue.OMINO_COLOR:
						self.__board[i+centerLocation[0]-len(printInfo)//2][j+centerLocation[1]-len(printInfo)//2] = BoardState.OFILLED
	def __FindToDeleteRows(self):
		rowsToDelete = []
		for i in range(0,len(self.__board)):
			numOfFilledInRow = 0
			for j in range(0,len(self.__board[i])):
				if self.__board[i][j] != BoardState.EMPTY and self.__board[i][j] != BoardState.WALL:
					numOfFilledInRow = numOfFilledInRow + 1
			if numOfFilledInRow == ConstValue.BOARDWIDTH:
				rowsToDelete.append(i)
		return rowsToDelete
	def __DeleteLine(self,rowsTodelete):
		numOfDeletedLines = 0
		for i in rowsTodelete:
			del self.__board[i-numOfDeletedLines]#행을 지울때마다 원래index보다 하나씩 더 줄어든 인덱스를 지워야함
			numOfDeletedLines += 1 
		self.__clearedLines += numOfDeletedLines
	def __AddNewLinesOnTop(self,numOfLines):
		for i in range(0,numOfLines):
			newRow = []
			for i in range(0,ConstValue.BOARDWIDTH+ConstValue.EXTRABOARDWIDTH):
				if i == 0 or i == ConstValue.BOARDWIDTH+ConstValue.EXTRABOARDWIDTH - 1:
					newRow.append(BoardState.WALL)
				else:
					newRow.append(BoardState.EMPTY)
			self.__board.insert(0,newRow)
	def ClearLine(self):
		rowsToDelete = self.__FindToDeleteRows()	
		self.__DeleteLine(rowsToDelete)
		self.__AddNewLinesOnTop(len(rowsToDelete))
	#__board의 내용물을 출력함
	def PrintBoard(self,screen):
		for i in range(0,len(self.__board)):
			for j in range(0,len(self.__board[i])):
				if self.__board[i][j] == BoardState.IFILLED:
					pygame.draw.rect(screen,ConstValue.IMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.LFILLED:
					pygame.draw.rect(screen,ConstValue.LMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.JFILLED:
					pygame.draw.rect(screen,ConstValue.JMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.SFILLED:
					pygame.draw.rect(screen,ConstValue.SMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.ZFILLED:
					pygame.draw.rect(screen,ConstValue.ZMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.OFILLED:
					pygame.draw.rect(screen,ConstValue.OMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
				elif self.__board[i][j] == BoardState.TFILLED:
					pygame.draw.rect(screen,ConstValue.TMINO_COLOR,pygame.Rect(self.__Location2Screen((i,j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
	#인자 location에 해당하는 실제 화면의 좌표를 return
	def __Location2Screen(self,location):
		return (
			ConstValue.SCREEN_LEFT_SPACE + (location[1]-ConstValue.EXTRABOARDWIDTH/2) * ConstValue.SCREEN_MINO_WIDTH,
			ConstValue.SCREEN_TOP_SPACE + (location[0]-ConstValue.EXTRABOARDHEIGHT+1) * ConstValue.SCREEN_MINO_HEIGHT
			)