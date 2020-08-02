import pygame
import ConstValue
import TetriminoManager

class Game:
	'''
	멤버변수
	'''
	__x = 0
	__clock = 0
	__screen = 0
	__tetriminoManager = 0
	'''
	멤버함수
	'''
	def Run(self):
		pygame.init()
		pygame.display.set_caption(ConstValue.CAPTION)
		self.__screen = pygame.display.set_mode((ConstValue.SCREEN_WIDTH, ConstValue.SCREEN_HEIGHT))
		self.__x = 10
		self.__clock = pygame.time.Clock()
		self.__tetriminoManager = TetriminoManager.TetriminoManager()
		self.__UpdateLoop()

	def __UpdateLoop(self):
		while True:
			self.__clock.tick(ConstValue.FRAMERATE)
			self.__screen.fill((0,0,0))#화면 지우기
			self.__DrawingBackGround()#백그라운드 배경(변하지않는요소그리기)
			
			self.__tetriminoManager.PrintPresentTetrimino(self.__screen)

			pygame.display.update()#화면 그린거 반영
	def __DrawingBackGround(self):
		#게임을 하는 메인 보드 뷰
		pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect(ConstValue.SCREEN_LEFT_SPACE,ConstValue.SCREEN_TOP_SPACE,ConstValue.SCREEN_BOARD_WIDTH,ConstValue.SCREEN_BOARD_HEIGHT))

		#홀드해놓은 미노를 표시하는 뷰
		pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_LEFT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2,ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))

		#대기중인 테트리미노를 표시하는 뷰
		for i in range(1,ConstValue.NUMOFVISUALMINOQUEUE+1):
			pygame.draw.rect(self.__screen,ConstValue.BOARD_COLOR,pygame.Rect((ConstValue.SCREEN_RIGHT_SPACE-ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT)/2 + ConstValue.SCREEN_BOARD_WIDTH+ ConstValue.SCREEN_LEFT_SPACE,i * ConstValue.SCREEN_MINORECT_TOP_BOTTOM_SPACE + (i-1) * ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT,ConstValue.SCREEN_MINORECT_WIDTHANDHEIGHT))