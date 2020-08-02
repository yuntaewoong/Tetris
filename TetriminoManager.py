
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
		self.__tetriminoBag = [Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.TetriminoState.O,ConstValue.FIRSTLOCATION)]

		random.shuffle(self.__tetriminoBag)

	def EnqueueTetrimino(self):
		self.__tetriminoQueue.append(self.__tetriminoBag[0])
		del self.__tetriminoBag[0]

		self.ResetBag()#만약 가방에 있는걸 다쓰면 가방을 초기화
	#location에 해당하는 실제 화면의 좌표를 return
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

		leftTopLocation = (centerLocation[0] - len(printList)//2 , centerLocation[1] - len(printList[0])//2)

		#pdb.set_trace()
		for i in range(0,len(printList)):
			for j in range(0,len(printList[i])):
				if printList[i][j] == 1:
					pygame.draw.rect(screen,ConstValue.SMINO_COLOR,pygame.Rect(self.__Location2Screen((leftTopLocation[0]+i,leftTopLocation[1]+j)),(ConstValue.SCREEN_MINO_WIDTH,ConstValue.SCREEN_MINO_HEIGHT)))
