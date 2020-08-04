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
			self.__clock.tick(ConstValue.FRAMERATE)
			self.__screen.fill((0,0,0))#화면 지우기
			self.__DrawingBackGround()#백그라운드 배경(변하지않는요소그리기)
			
			
			
			self.__tetriminoManager.PrintPresentTetrimino(self.__screen)
			self.__boardManager.PrintBoard(self.__screen)
			
			self.__KeyboardInputProcess(self.__tetriminoManager.GetPresentMino(),self.__boardManager.GetBoard())
			
			pygame.display.update()#화면 그린거 반영



	def __pressedKeyChecking(self,KEY):
		if self.__pressedKey == KEY:
				self.__pressedFrame = self.__pressedFrame + 1
		else:
			self.__pressedFrame = 0
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
		print(self.__pressedFrame)
			
					
				
	
	def __DrawingBackGround(self):
		#게임을 하는 메인 보드 뷰
		pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect(ConstValue.SCREEN_LEFT_SPACE,ConstValue.SCREEN_TOP_SPACE,ConstValue.SCREEN_BOARD_WIDTH,ConstValue.SCREEN_BOARD_HEIGHT))

		#홀드해놓은 미노를 표시하는 뷰
		pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_LEFT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2,ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))

		#대기중인 테트리미노를 표시하는 뷰
		for i in range(1,ConstValue.NUMOFVISUALMINOQUEUE+1):
			pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_RIGHT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2 + ConstValue.SCREEN_BOARD_WIDTH+ ConstValue.SCREEN_LEFT_SPACE,i * ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE + (i-1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))