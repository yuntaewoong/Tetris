import pygame
import ConstValue

class Game:
	'''
	멤버변수
	'''
	__x = 0
	__clock = 0
	__screen = 0
	'''
	멤버함수
	'''
	def Run(self):
		pygame.init()
		pygame.display.set_caption(ConstValue.CAPTION)
		self.__screen = pygame.display.set_mode((ConstValue.SCREEN_WIDTH, ConstValue.SCREEN_HEIGHT))
		self.__x = 10
		self.__clock = pygame.time.Clock()
		self.__UpdateLoop()

	def __UpdateLoop(self):
		while True:
			self.__clock.tick(ConstValue.FRAMERATE)
			self.__screen.fill((0,0,0))#화면 지우기

			if self.__x != 600:
				pygame.draw.rect(self.__screen,(255,0,0),pygame.Rect(10,10,self.__x,10))
				self.__x += 1
			else:
				pygame.draw.rect(self.__screen,(255,255,0),pygame.Rect(10,20,300,300))
			

			pygame.display.update()#화면 그린거 반영
