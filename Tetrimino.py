import ConstValue
import pdb
from enum import IntEnum
class TetriminoState(IntEnum):
	O = 1
	R = 2 
	T = 3
	L = 4
def TetriminoState2Str(tetriminoState):
	if tetriminoState == TetriminoState.O:
		return 'O'
	elif tetriminoState == TetriminoState.R:
		return 'R'
	elif tetriminoState == TetriminoState.T:
		return 'T'
	else:
		return 'L'



class Tetrimino:
	'''
	멤버변수
	'''
	__kind = ""
	#tetrimino의 회전상태
	__tetriminoState = TetriminoState.O
	__centerLocation = [0,0]
	__wallKickData = {}
	'''
	멤버메서드
	'''
	def __init__(self,tetriminoState,location):
		self.__tetriminoState = tetriminoState
		self.__centerLocation = location
	def GetState(self):
		return self.__tetriminoState
	def GetLocation(self):
		return self.__centerLocation
	def SetLocation(self,vertical,horizontal):
		location = [vertical,horizontal]
		self.__centerLocation = location

	def _GetWallKickData(self):
		return self.__wallKickData
	#시계방향 반시계방향 설정에따라 다음 테트리미노 상태 결정
	#Rotate함수들에서 사용됨(protected))
	def _SetNextState(self,rotateKind):
		if rotateKind == "Clockwise":
			self.__tetriminoState = (self.__tetriminoState+1) % ConstValue.NUMOFTETRIMINOSTATE
		elif rotateKind == "CounterClockwise":
			self.__tetriminoState = (self.__tetriminoState-1) % ConstValue.NUMOFTETRIMINOSTATE
	def _SetWallKickData(self,wallKickData):
		self.__wallKickData = wallKickData
	def _SetKind(self,kind):
		self.__kind = kind
	#테트리미노의 출력정보에 해당하는 리스트를 반환
	#ex) O상태의 s미노의 리턴값: [
	#	[0,1,1],
	#	[1,1,0],
	#	[0,0,0]	
	#]
	def GetPrintInfo(self):
		pass
	#테트리미노가 하강할 수 있다면 이동후 True반환 아니면 False반환
	def MoveDown(self,board):
		pass
	#테트리미노가 회전할 수 있다면 회전후 True반환 아니면 False반환
	#테트리미노의 회전알고리즘은 SRS알고리즘을 따름
	#참조: https://tetris.wiki/Super_Rotation_System
	def ClockwiseRotate(self,board):
		pass
	def CounterClockwiseRotate(self,board):
		pass

class Smino(Tetrimino):
	def __init__(self,tetriminoState,location):
		self._SetKind("S")
		self._SetWallKickData({
			"O->R": [(0,0),(-1,0),(-1,+1),(0,-2),(-1,-2)],
			"R->O": [(0,0),(+1,0),(+1,-1),(0,+2),(+1,+2)],
			"R->T": [(0,0),(+1,0),(+1,-1),(0,+2),(+1,+2)],
			"T->R": [(0,0),(-1,0),(-1,+1),(0,-2),(-1,-2)],
			"T->L": [(0,0),(+1,0),(+1,+1),(0,-2),(+1,-2)],
			"L->T": [(0,0),(-1,0),(-1,-1),(0,+2),(-1,+2)],
			"L->O": [(0,0),(-1,0),(-1,-1),(0,+2),(-1,+2)],
			"O->L": [(0,0),(+1,0),(+1,+1),(0,-2),(+1,-2)]
		})
		super().__init__(tetriminoState,location)
	#테트리미노의 출력정보에 해당하는 리스트를 반환
	#ex) O상태의 s미노의 리턴값: [
	#	[0,1,1],
	#	[1,1,0],
	#	[0,0,0]	
	#]
	def GetPrintInfo(self):
		if self.GetState() == TetriminoState.O:
			return [
				[0,1,1],
				[1,1,0],
				[0,0,0]
			]
		elif self.GetState() == TetriminoState.R:
			return [
				[0,1,0],
				[0,1,1],
				[0,0,1]
			]
		elif self.GetState() == TetriminoState.T:
			return [
				[0,0,0],
				[0,1,1],
				[1,1,0]
			]
		else:
			return [
				[1,0,0],
				[1,1,0],
				[0,1,0]
			]
	#테트리미노가 하강할 수 있다면 이동후 True반환 아니면 False반환
	def MoveDown(self,board):
		if self.GetState() == TetriminoState.O:
			centerLocation = self.GetLocation()
			if board[centerLocation[0]+1][centerLocation[1]-1] == 0 and board[centerLocation[0]+1][centerLocation[1]] == 0 and board[centerLocation[0]][centerLocation[1]+1] == 0:
				self.SetLocation(centerLocation[0]+1,centerLocation[1])
				return True 
		elif self.GetState() == TetriminoState.R:
			centerLocation = self.GetLocation()
			if board[centerLocation[0]+1][centerLocation[1]] == 0 and board[centerLocation[0]+1][centerLocation[1]+2] == 0:
				self.SetLocation(centerLocation[0]+1,centerLocation[1])
				return True
		elif self.GetState() == TetriminoState.T:
			centerLocation = self.GetLocation()
			if board[centerLocation[0]+2][centerLocation[1]-1] == 0 and board[centerLocation[0]+2][centerLocation[1]] == 0 and board[centerLocation[0]+1][centerLocation[1]+1] == 0:
				self.SetLocation(centerLocation[0]+1,centerLocation[1])
				return True
		else:
			centerLocation = self.GetLocation()
			if board[centerLocation[0]+1][centerLocation[1]-1] == 0 and board[centerLocation[0]+2][centerLocation[1]] == 0:
				self.SetLocation(centerLocation[0]+1,centerLocation[1])
				return True
		#이동에 성공 못할시 False
		return False
	#kick되었을때 그곳에 존재할수 있는지 검사
	#존재할수 있다면 True 아니면 False
	#__WallKickTest함수에서 사용
	def __CheckingOverlap(self,goalVertical,goalHorizontal,goalState,board):
		goalCenterLocation = (
			self.GetLocation()[0] + goalVertical,
			self.GetLocation()[1] + goalHorizontal
		)
		if goalState == TetriminoState.O:
			if board[goalCenterLocation[0]][goalCenterLocation[1]-1] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]-1][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]-1][goalCenterLocation[1] + 1] == 0:
				return True  
		elif goalState == TetriminoState.R:
			if board[goalCenterLocation[0]-1][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]+1] == 0 and board[goalCenterLocation[0]+1][goalCenterLocation[1] + 1] == 0:
				return True
		elif goalState == TetriminoState.T:
			if board[goalCenterLocation[0]+1][goalCenterLocation[1]-1] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]+1][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1] + 1] == 0:
				return True
		else:
			if board[goalCenterLocation[0]-1][goalCenterLocation[1]-1] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]-1] == 0 and board[goalCenterLocation[0]][goalCenterLocation[1]] == 0 and board[goalCenterLocation[0]+1][goalCenterLocation[1]] == 0:
				return True
		return False
	#presentState를 goalState로 바꾸는 과정에서 5가지 테스트케이스를 테스트후
	#올바른 kickValue를 return
	def __5TestCaseTest(self,presentState,goalState,board):
		for kickValue in self._GetWallKickData()[TetriminoState2Str(presentState) + "->" + TetriminoState2Str(goalState)]:
			if self.__CheckingOverlap(kickValue[0],kickValue[1],goalState,board):
				return kickValue
	#ClockwiseRotate,CounterClockwiseRotate함수에서 사용
	#회전시 wallkick현상 발생 체크(ex/T스핀,S스핀,Z스핀,I스핀,L스핀,J스핀)
	#return값: 이동해야하는 중심축 오프셋값 튜플 (ex/ (+1,0) 수직축 1하강 수평축 변화x)
	def __WallKickTest(self,board,rotateKind):
		if rotateKind == "Clockwise" and self.GetState() == TetriminoState.O:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "Clockwise" and self.GetState() == TetriminoState.R:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "Clockwise" and self.GetState() == TetriminoState.T:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "Clockwise" and self.GetState() == TetriminoState.L:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "CounterClockwise" and self.GetState() == TetriminoState.O:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "CounterClockwise" and self.GetState() == TetriminoState.R:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "CounterClockwise" and self.GetState() == TetriminoState.T:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		elif rotateKind == "CounterClockwise" and self.GetState() == TetriminoState.L:
			return self.__5TestCaseTest(TetriminoState.O,TetriminoState.R,board)
		return ConstValue.FAILTUPLE

	#테트리미노가 시계방향으로 회전할 수 있다면 회전후 True반환 아니면 False반환
	def ClockwiseRotate(self,board):
		kickTestValue = self.__WallKickTest(board,"Clockwise")
		
		if kickTestValue != ConstValue.FAILTUPLE:#회전 성공
				#중심축 변경
				self.SetLocation(self.GetLocation()[0] + kickTestValue[0],self.GetLocation()[1] + kickTestValue[1])
				#회전상태 변경
				self._SetNextState("Clockwise")
		else: #회전 실패
			return False
	#테트리미노가 반시계방향으로 회전할 수 있다면 회전후 True반환 아니면 False반환
	def CounterClockwiseRotate(self,board):
		kickTestValue = self.__WallKickTest(board,"CounterClockwise")
		
		if kickTestValue != ConstValue.FAILTUPLE:#회전 성공
				#중심축 변경
				self.SetLocation(self.GetLocation()[0] + kickTestValue[0],self.GetLocation()[1] + kickTestValue[1])
				#회전상태 변경
				self._SetNextState("CounterClockwise")
		else: #회전 실패
			return False
