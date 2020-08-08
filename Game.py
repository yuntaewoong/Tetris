import pygame
import ConstValue
import TetriminoManager
import BoardManager
import pdb

class Game:
	'''
	멤버변수
	'''
	__clock = 0
	__screen = 0
	__tetriminoManager = 0
	__boardManager = 0
	__pressedKey = 0
	__pressedFrame = 0
	__gameFrame = 0
	'''
	멤버함수
	'''
	def Run(self):
		pygame.init()
		pygame.display.set_caption(ConstValue.CAPTION)
		self.__screen = pygame.display.set_mode((ConstValue.SCREEN_WIDTH, ConstValue.SCREEN_HEIGHT))
		self.__clock = pygame.time.Clock()
		self.__tetriminoManager = TetriminoManager.TetriminoManager()
		self.__boardManager = BoardManager.BoardManager() 
		self.__UpdateLoop()
	def __UpdateLoop(self):
		while True:
			self.__clock.tick(ConstValue.FRAMERATE)#초당 프레임수 설정
			self.__screen.fill((0,0,0))#화면 지우기
			self.__DrawingBackGround()#백그라운드 배경(변하지않는요소그리기)
			self.__tetriminoManager.PrintHoldTetrimino(self.__screen)
			self.__tetriminoManager.PrintTetriminoQueue(self.__screen)
			self.__tetriminoManager.PrintGhostTetrimino(self.__screen,self.__boardManager.GetBoard())
			self.__gameFrame = self.__gameFrame + 1#게임의 프레임수(자동 이동에 쓰임)
			self.__tetriminoManager.PrintPresentTetrimino(self.__screen)#현재 조작하는 테트리미노를 출력
			self.__boardManager.PrintBoard(self.__screen)#쌓여있는 Board를 출력
			self.__KeyboardInputProcess(self.__tetriminoManager.GetPresentMino(),self.__boardManager.GetBoard())#모든 키보드 입력처리
			self.__AutoMoveDown(self.__tetriminoManager.GetPresentMino(),self.__boardManager.GetBoard())#일정 프레임마다 자동으로 미노가 하강함
			self.__tetriminoManager.GetPresentMino().TetriminoUpdate(self.__boardManager.GetBoard())#현재 테트리미노의 세부정보 업데이트(__untilStackingFrame))
			self.__StackingIfPossible(self.__tetriminoManager.GetPresentMino(),self.__tetriminoManager,self.__boardManager)#스태킹 할수 있다면 함
			self.__boardManager.ClearLine()
			
			pygame.display.update()#화면 그린거 반영
	#테트리미노가 스태킹이 가능한상태라면 TetriminoManager에서는 현재 미노를 삭제후 다음미노를 보드에 출현시키고
	#BoardManager에서는 board에 현재 미노를 추가한다
	def __StackingIfPossible(self,presentTetrimino,tetriminoManager,boardManager):
		if presentTetrimino.IsStackingPossible(boardManager.GetBoard()):
			boardManager.StackingMino(presentTetrimino.GetLocation(),presentTetrimino.GetPrintInfo(),presentTetrimino.GetColor())#board에 추가
			tetriminoManager.DequeueTetrimino() #현재 블록을 tetriminoManager에서 삭제
			tetriminoManager.EnqueueTetrimino() #대기 블록을 하나 추가
	def __AutoMoveDown(self,presentTetrimino,presentBoard):
		if self.__gameFrame % ConstValue.AUTO_MOVE_DELAY_FRAME == 0:
			presentTetrimino.MoveDown(presentBoard)
	def __pressedKeyChecking(self,KEY):
		if self.__pressedKey == KEY:
				self.__pressedFrame = self.__pressedFrame + 1
		else:
			self.__pressedFrame = 0
	def __HardDrop(self,presentTetrimino,presentBoard):
		presentTetrimino.SetHardDrop()
		while presentTetrimino.IsMovingDownPossible(presentBoard) == True:
			presentTetrimino.MoveDown(presentBoard)
	def __KeyboardInputProcess(self,presentTetrimino,presentBoard):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					self.__pressedKey = pygame.K_DOWN
					presentTetrimino.MoveDown(presentBoard)
				elif event.key == pygame.K_RIGHT:
					self.__pressedKey = pygame.K_RIGHT
					presentTetrimino.MoveRight(presentBoard)
				elif event.key == pygame.K_LEFT:
					self.__pressedKey = pygame.K_LEFT
					presentTetrimino.MoveLeft(presentBoard)
				elif event.key == pygame.K_z:
					presentTetrimino.CounterClockwiseRotate(presentBoard)
				elif event.key == pygame.K_x:
					presentTetrimino.ClockwiseRotate(presentBoard)	
				elif event.key == pygame.K_c:
					self.__tetriminoManager.HoldTetrimino(presentTetrimino)
				elif event.key == pygame.K_SPACE:
					self.__HardDrop(presentTetrimino,presentBoard)
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			#soft drop
			self.__pressedKeyChecking(pygame.K_DOWN)
			if self.__pressedFrame % ConstValue.SOFT_DROP_DELAY_FRAME == 0:
					presentTetrimino.MoveDown(presentBoard)
		elif pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.__pressedKeyChecking(pygame.K_RIGHT)
			if self.__pressedFrame > ConstValue.SOFT_MOVE_LIMIT_FRAME and self.__pressedFrame % ConstValue.SOFT_MOVE_DELAY_FRAME == 0:
				presentTetrimino.MoveRight(presentBoard)
		elif pygame.key.get_pressed()[pygame.K_LEFT]:
			self.__pressedKeyChecking(pygame.K_LEFT)
			if self.__pressedFrame > ConstValue.SOFT_MOVE_LIMIT_FRAME and self.__pressedFrame % ConstValue.SOFT_MOVE_DELAY_FRAME == 0:
				presentTetrimino.MoveLeft(presentBoard)
		else:
			self.__pressedFrame = 0
	def __DrawingBackGround(self):
		#게임을 하는 메인 보드 뷰
		pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect(ConstValue.SCREEN_LEFT_SPACE,ConstValue.SCREEN_TOP_SPACE,ConstValue.SCREEN_BOARD_WIDTH,ConstValue.SCREEN_BOARD_HEIGHT))

		
		