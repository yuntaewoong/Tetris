
import pygame #그래픽 표현
import copy
import Tetrimino
import ConstValue
import random

import pdb

class TetriminoManager:
	__tetriminoQueue = []
	__tetriminoBag = []
	__holdTetrimino = 0
	def __init__(self):
		self.ResetBag()
		for i in range(0,ConstValue.NUMOFVISUALMINOQUEUE+1):
			self.EnqueueTetrimino()
	#__tetriminoBag이 비어있을때만 호출
	#가방을 재정립함
	def ResetBag(self):
		if self.__tetriminoBag:
			return #가방이 안비었으면 실행 x
		self.__tetriminoBag = [Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Zmino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Lmino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Jmino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Tmino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Omino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Imino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION)]

		random.shuffle(self.__tetriminoBag)
	#manager밖에서 테트리미노를 조작할수있게함
	def GetPresentMino(self):
		return self.__tetriminoQueue[0]
	def DequeueTetrimino(self):
		del self.__tetriminoQueue[0]
	def EnqueueTetrimino(self):
		self.__tetriminoQueue.append(self.__tetriminoBag[0])
		del self.__tetriminoBag[0]
		self.ResetBag()#만약 가방에 있는걸 다쓰면 가방을 초기화
	def HoldTetrimino(self,tetrimino):
		#홀드된 미노가 없을때
		if self.__holdTetrimino == 0:
			self.__holdTetrimino = copy.deepcopy(tetrimino)
			self.__holdTetrimino.SetIsHoldPossible(False)
			self.DequeueTetrimino()
			self.EnqueueTetrimino()
		#홀드된 미노가 있을때
		else:
			if self.__tetriminoQueue[0].GetIsHoldPossible():
				temp = self.__holdTetrimino
				self.__holdTetrimino = copy.deepcopy(tetrimino)
				temp.SetIsHoldPossible(False)
				temp.SetLocation(ConstValue.FIRSTLOCATION[0],ConstValue.FIRSTLOCATION[1])
				self.__tetriminoQueue[0] = temp
	#인자 location에 해당하는 실제 화면의 좌표를 return
	def __Location2Screen(self,location):
		return (
			ConstValue.SCREEN_LEFT_SPACE + location[1] * ConstValue.SCREEN_MINO_WIDTH,
			ConstValue.SCREEN_TOP_SPACE + location[0] * ConstValue.SCREEN_MINO_HEIGHT
		)
	#__tetriminoQueue에서 0번 인덱스에 있는 미노는 보드에 프린트되는 미노임
	#보드의 미노를 프린트하는 함수
	def PrintPresentTetrimino(self,screen):
		centerLocation = self.__tetriminoQueue[0].GetLocation()
		printList = self.__tetriminoQueue[0].GetPrintInfo()
		topLeftLocation = (centerLocation[0] - len(printList)//2 , centerLocation[1] - len(printList[0])//2)
		for i in range(0,len(printList)):
			for j in range(0,len(printList[i])):
				if printList[i][j] == 1:
					pygame.draw.rect(screen,self.__tetriminoQueue[0].GetColor(),pygame.Rect(self.__Location2Screen((topLeftLocation[0]+i-2,topLeftLocation[1]+j-ConstValue.EXTRABOARDWIDTH//2)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
	#대기열에 있는 미노를 프린트하는 함수
	def PrintTetriminoQueue(self,screen):
		for i in range(1,ConstValue.NUMOFVISUALMINOQUEUE+1):
			#배경
			pygame.draw.rect(screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_RIGHT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2 + ConstValue.SCREEN_BOARD_WIDTH+ ConstValue.SCREEN_LEFT_SPACE,i * ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE + (i-1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))
			#테트리미노
			printInfo = self.__tetriminoQueue[i].GetPrintInfo()
			for z in range(0,len(printInfo)):
				for k in range(0,len(printInfo[z])): 
					if printInfo[z][k] == 1:
						pygame.draw.rect(screen,self.__tetriminoQueue[i].GetColor(),pygame.Rect((ConstValue.SCREEN_RIGHT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2 + ConstValue.SCREEN_BOARD_WIDTH+ ConstValue.SCREEN_LEFT_SPACE + k * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4 ,i * ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE + (i-1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT + (z+1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4))

	def PrintHoldTetrimino(self,screen):
		#홀드해놓은 미노를 표시하는 뷰
		pygame.draw.rect(screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_LEFT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2,ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))
		if self.__holdTetrimino != 0:
			printInfo = self.__holdTetrimino.GetPrintInfo()
			for z in range(0,len(printInfo)):
				for k in range(0,len(printInfo[z])): 
					if printInfo[z][k] == 1:
						pygame.draw.rect(screen,self.__holdTetrimino.GetColor(),pygame.Rect((ConstValue.SCREEN_LEFT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2+ k * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4,ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE  + (z+1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT/4))
	def PrintGhostTetrimino(self,screen,board):
		#하드드롭시 떨어질 위치에 ghostmino출력
		ghostTetrimino = copy.deepcopy(self.__tetriminoQueue[0])
		while ghostTetrimino.IsMovingDownPossible(board):
			ghostTetrimino.MoveDown(board)
		ghostCenterLocation = ghostTetrimino.GetLocation()
		printList = ghostTetrimino.GetPrintInfo()
		topLeftLocation = (ghostCenterLocation[0] - len(printList)//2 , ghostCenterLocation[1] - len(printList[0])//2)
		for i in range(0,len(printList)):
			for j in range(0,len(printList[i])):
				if printList[i][j] == 1:
					pygame.draw.rect(screen,self.__tetriminoQueue[0].GetColor(),pygame.Rect(self.__Location2Screen((topLeftLocation[0]+i-2,topLeftLocation[1]+j-ConstValue.EXTRABOARDWIDTH//2)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)),1)

