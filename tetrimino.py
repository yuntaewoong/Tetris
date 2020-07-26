class Tetrimino:
	'''
	멤버변수
	'''
	#__isRotated가 true면 서있는 상태
	__kind = ""
	__isRotated = False
	__centerLocation = [0,0]
	#__해당 tetrimino의 주변상황(블록이 존재하면 1 아니면 0)
	__around = [
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0]
	]
	'''
	멤버메서드
	'''
	def __init__(self,kind,isRotated,location):
		self.kind = kind
		self.__isRotated = isRotated
		self.__centerLocation = location
	
	def SetLocation(self,location):
		self.__centerLocation = location
	def SetAround(self,around):
		self.__around = around
	def GetAround(self):
		return self.__around
	def GetRotate(self):
		return self.__isRotated
	def GetLocation(self):
		return self.__centerLocation
	def ToggleRotate(self):
		self.__isRotated = not self.__isRotated



	#centerLocation에 따라 알맞은 형태로 출력
	def Print(self):
		pass
	#테트리미노가 하강할 수 있다면 이동후 True반환 아니면 False반환
	def MoveDown(self,board):
		pass
	#테트리미노가 회전할 수 있다면 회전후 True반환 아니면 False반환
	def Rotate(self,board):
		pass
	#테트리미노 주위를 감지해서 around멤버를 업데이트, board매개변수는 게임판의 상태 이중 리스트임(블록존재하면 1 아니면 0)
	#board에 자기 자신은 표현되어 있지 않음
	def observeAround(self,board):
		pass

class Smino(Tetrimino):
	def __init(self,kind,isRotated,location):
		super().__init__(self,kind,isRotated,location)
		if isRotated == True:
			self.SetAround([
				[0,0,1,0],
				[0,1,1,0],
				[0,1,0,0],
				[0,0,0,0]
			])
		else:	
			self.SetAround([
				[0,0,0,0],
				[1,1,0,0],
				[0,1,1,0],
				[0,0,0,0]
			])
	#centerLocation에 따라 알맞은 형태로 출력
	def Print(self):
		pass
	#테트리미노가 하강할 수 있다면 이동후 True반환 아니면 False반환
	def MoveDown(self,board):
		#세로 모양
		if self.GetRotate() == True:
			if (self.GetAround()[3][1] == 0) and (self.GetAround()[2][2] == 0):#하강 조건 만족
				newLocation = [self.GetLocation()[0],self.GetLocation()[1]+1]
				self.SetLocation(newLocation)#좌표 1 하강
				self.observeAround(self,board)#하강후 다시 주위 관찰
				return True
		#가로 모양
		else:
			if (self.GetAround()[2][0] == 0) and (self.GetAround()[3][1] == 0) and (self.GetAround()[3][2] == 0):#하강 조건 만족
				newLocation = [self.GetLocation()[0],self.GetLocation()[1]+1]
				self.SetLocation(newLocation)#좌표 1 하강
				self.observeAround(self,board)#하강후 다시 주위 관찰
				return True
		return False

		
	#테트리미노가 회전할 수 있다면 회전후 True반환 아니면 False반환
	def Rotate(self,board):
		#세로 모양
		if self.GetRotate() == True:
			if (self.GetAround()[1][0] == 0) and (self.GetAround()[2][2] == 0):#회전 조건 만족
				self.ToggleRoate()
				self.observeAround(self,board)#하강후 다시 주위 관찰
				return True
		#가로 모양
		else:
			if (self.GetAround()[0][1] == 0) and (self.GetAround()[0][2] == 0) and (self.GetAround()[1][2] == 0):#회전 조건 만족
				self.ToggleRotate()#회전상태바꾸기
				self.observeAround(self,board)#회전후 다시 주위 관찰
				return True
		return False
	#테트리미노 주위를 감지해서 around멤버를 업데이트, board매개변수는 게임판의 상태 이중 리스트임(블록존재하면 1 아니면 0)(12 X 24) 가로10 + 벽2/ 세로 20 + 벽 1 + 여유분 3
	#board에는 자기 자신은 표현되어 있지 않음
	def observeAround(self,board):

		pass
