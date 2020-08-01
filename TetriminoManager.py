
import pygame #그래픽 표현

import Tetrimino
import ConstValue
import random

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
			return
		self.__tetriminoBag = [Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION),Tetrimino.Smino(Tetrimino.tetriminoState.O,ConstValue.FIRSTLOCATION)]
		random.shuffle(self.__tetriminoBag)

	def EnqueueTetrimino(self):
		self.__tetriminoQueue.append(self.__tetriminoBag[0])
		del self.__tetriminoBag[0]

		self.ResetBag()#만약 가방에 있는걸 다쓰면 가방을 초기화
		