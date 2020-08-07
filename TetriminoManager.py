
import pygame #그래픽 표현

import Tetrimino
import ConstValue
import random

import pdb

class TetriminoManager:
	__tetriminoQueue = []
	__tetriminoBag = []
	def __init__(self):
		self.ResetBag()
		for i in range(0,5):
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

		#pdb.set_trace()
		for i in range(0,len(printList)):
			for j in range(0,len(printList[i])):
				if printList[i][j] == 1:
					pygame.draw.rect(screen,self.__tetriminoQueue[0].GetColor(),pygame.Rect(self.__Location2Screen((topLeftLocation[0]+i-2,topLeftLocation[1]+j-ConstValue.EXTRABOARDWIDTH//2)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
