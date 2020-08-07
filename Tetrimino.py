import ConstValue
import pdb

from BoardManager import BoardState #BoardState enum사용위해서
from enum import IntEnum
class TetriminoState(IntEnum):
	O = 0
	R = 1 
	T = 2
	L = 3
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
	#tetrimino의 회전상태
	__tetriminoState = TetriminoState.O
	__centerLocation = [0,0]
	__wallKickData = {}
	__untilStackingFrame = 0
	__isHoldPossible = True
	'''
	멤버메서드
	'''
	def __init__(self,tetriminoState,location):
		self.__tetriminoState = tetriminoState
		self.__centerLocation = location
	def GetState(self):
		return self.__tetriminoState
	def GetPrintInfo(self):
		return self.GetPrintInfoBasedOnTetriminoState(self.GetState())
	def __GetNextStateOnClockwiseRotate(self):
		return (self.__tetriminoState+1) % ConstValue.NUMOFTETRIMINOSTATE
	def __GetNextStateOnCounterClockwiseRotate(self):
		return (self.__tetriminoState-1) % ConstValue.NUMOFTETRIMINOSTATE
	def __GetWallKickData(self):
		return self.__wallKickData
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		pass
	def GetLocation(self):
		return self.__centerLocation
	def GetColor(self):
		pass
	def GetIsHoldPossible(self):
		return self.__isHoldPossible
	def IsStackingPossible(self,board):
		return self.__untilStackingFrame >= ConstValue.STACKING_DELAY_FRAME and not self.IsMovingDownPossible(board) 
	def SetLocation(self,vertical,horizontal):
		location = [vertical,horizontal]
		self.__centerLocation = location
	def SetHardDrop(self):#하드드롭은 바로 스태킹할수 있도록 함
		self.__untilStackingFrame = ConstValue.STACKING_DELAY_FRAME
	def SetIsHoldPossible(self,isHoldPossible):
		self.__isHoldPossible = isHoldPossible
	def __SetState(self,tetriminoState):
			self.__tetriminoState = tetriminoState
	#자식 클래스에서 __wallkickData를 초기화하는데 사용
	def _SetWallKickData(self,wallKickData):
		self.__wallKickData = wallKickData
	#TetriminoUpdate는 매프레임 필수로 호출되어야함
	def TetriminoUpdate(self,board):
		self.__UpdateUntilStackingFrame(board)
	#테트리미노가 하강할 수 있다면 True 없다면 False
	def IsMovingDownPossible(self,board):
		if self.__CheckingOverlap(1,0,self.GetState(),board):
			return True
		else:
			return False
	#테트리미노가 하강할 수 있다면 이동
	def MoveDown(self,board):
		if self.IsMovingDownPossible(board):
			centerLocation = self.GetLocation()
			self.SetLocation(centerLocation[0]+1,centerLocation[1])
	#테트리미노가 왼쪽으로 이동할 수 있다면 이동후 True반환 아니면 False반환
	def MoveLeft(self,board):
		if self.__CheckingOverlap(0,-1,self.GetState(),board):
			centerLocation = self.GetLocation()
			self.SetLocation(centerLocation[0],centerLocation[1]-1)
			return True
		else:
			#이동에 성공 못할시 False
			return False
	#테트리미노가 오른쪽으로 이동할 수 있다면 이동후 True반환 아니면 False반환
	def MoveRight(self,board):
		if self.__CheckingOverlap(0,1,self.GetState(),board):
			centerLocation = self.GetLocation()
			self.SetLocation(centerLocation[0],centerLocation[1]+1)
			return True
		else:
			#이동에 성공 못할시 False
			return False
	#테트리미노가 시계방향으로 회전할 수 있다면 회전후 True반환 아니면 False반환
	#테트리미노의 회전알고리즘은 SRS알고리즘을 따름
	#참조: https://tetris.wiki/Super_Rotation_System
	def ClockwiseRotate(self,board):
		kickTestValue = self.__ClockwiseWallKickTest(board)
		if kickTestValue != ConstValue.FAILTUPLE:#회전 성공
				#중심축 변경
				self.SetLocation(self.GetLocation()[0] + kickTestValue[0],self.GetLocation()[1] + kickTestValue[1])
				#회전상태 변경
				self.__SetState(self.__GetNextStateOnClockwiseRotate())
		else: #회전 실패
			return False
	#테트리미노가 반시계방향으로 회전할 수 있다면 회전후 True반환 아니면 False반환
	def CounterClockwiseRotate(self,board):
		kickTestValue = self.__CounterClockwiseWallKickTest(board)
		if kickTestValue != ConstValue.FAILTUPLE:#회전 성공
				#중심축 변경
				self.SetLocation(self.GetLocation()[0] + kickTestValue[0],self.GetLocation()[1] + kickTestValue[1])
				#회전상태 변경
				self.__SetState(self.__GetNextStateOnCounterClockwiseRotate())
		else: #회전 실패
			return False
	#중심좌표가 이동할 시 그곳에 존재할수 있는지 검사
	#존재할수 있다면 True 아니면 False
	def __CheckingOverlap(self,goalVerticalDelta,goalHorizontalDelta,goalState,board):
		goalPrintInfo = self.GetPrintInfoBasedOnTetriminoState(goalState)
		centerLocation = self.GetLocation()
		for i in range(0,len(goalPrintInfo)):
			for j in range(0,len(goalPrintInfo[i])):
				if goalPrintInfo[i][j] == 1 and board[i+goalVerticalDelta+centerLocation[0]-len(goalPrintInfo)//2][j+goalHorizontalDelta+centerLocation[1]-len(goalPrintInfo)//2] != BoardState.EMPTY:
					return False
		return True				
	#presentState를 goalState로 바꾸는 과정에서 5가지 테스트케이스를 테스트후
	#올바른 kickValue를 return
	def __5TestCaseTest(self,presentState,goalState,board):
		for kickValue in self.__GetWallKickData()[TetriminoState2Str(presentState) + "->" + TetriminoState2Str(goalState)]:
			if self.__CheckingOverlap(kickValue[0],kickValue[1],goalState,board):
				return kickValue
		return ConstValue.FAILTUPLE
	#ClockwiseRotate,CounterClockwiseRotate함수에서 사용
	#회전시 wallkick현상 발생 체크(ex/T스핀,S스핀,Z스핀,I스핀,L스핀,J스핀)
	#return값: 이동해야하는 중심축 오프셋값 튜플 (ex/ (+1,0) 수직축 1하강 수평축 변화x), ConstValue.FAILTUPLE이 리턴되면 회전불가
	def __ClockwiseWallKickTest(self,board):
		return self.__5TestCaseTest(self.GetState(),self.__GetNextStateOnClockwiseRotate(),board)
	def __CounterClockwiseWallKickTest(self,board):
		return self.__5TestCaseTest(self.GetState(),self.__GetNextStateOnCounterClockwiseRotate(),board)
	#untilStackingFrame을 업데이트함
	def __UpdateUntilStackingFrame(self,board):
		if not self.IsMovingDownPossible(board):
			self.__untilStackingFrame = self.__untilStackingFrame + 1

class Smino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[0,1,1],
				[1,1,0],
				[0,0,0]
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,1,0],
				[0,1,1],
				[0,0,1]
			]
		elif tetriminoState == TetriminoState.T:
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
	def GetColor(self):
		return ConstValue.SMINO_COLOR
class Zmino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[1,1,0],
				[0,1,1],
				[0,0,0]
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,0,1],
				[0,1,1],
				[0,1,0]
			]
		elif tetriminoState == TetriminoState.T:
			return [
				[0,0,0],
				[1,1,0],
				[0,1,1]
			]
		else:
			return [
				[0,1,0],
				[1,1,0],
				[1,0,0]
			]
	def GetColor(self):
		return ConstValue.ZMINO_COLOR
class Jmino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[1,0,0],
				[1,1,1],
				[0,0,0]
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,1,1],
				[0,1,0],
				[0,1,0]
			]
		elif tetriminoState == TetriminoState.T:
			return [
				[0,0,0],
				[1,1,1],
				[0,0,1]
			]
		else:
			return [
				[0,1,0],
				[0,1,0],
				[1,1,0]
			]
	def GetColor(self):
		return ConstValue.JMINO_COLOR
class Lmino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[0,0,1],
				[1,1,1],
				[0,0,0]
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,1,0],
				[0,1,0],
				[0,1,1]
			]
		elif tetriminoState == TetriminoState.T:
			return [
				[0,0,0],
				[1,1,1],
				[1,0,0]
			]
		else:
			return [
				[1,1,0],
				[0,1,0],
				[0,1,0]
			]
	def GetColor(self):
		return ConstValue.LMINO_COLOR
class Tmino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[0,1,0],
				[1,1,1],
				[0,0,0]
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,1,0],
				[0,1,1],
				[0,1,0]
			]
		elif tetriminoState == TetriminoState.T:
			return [
				[0,0,0],
				[1,1,1],
				[0,1,0]
			]
		else:
			return [
				[0,1,0],
				[1,1,0],
				[0,1,0]
			]
	def GetColor(self):
		return ConstValue.TMINO_COLOR
class Omino(Tetrimino):
	def __init__(self,tetriminoState,location):
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
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		return [
			[1,1,0],
			[1,1,0],
			[0,0,0]
		]
	def GetColor(self):
		return ConstValue.OMINO_COLOR
class Imino(Tetrimino):
	def __init__(self,tetriminoState,location):
		self._SetWallKickData({
			"O->R": [(0,0),(-2,0),(+1,0),(-2,-1),(+1,+2)],
			"R->O": [(0,0),(+2,0),(-1,0),(+2,+1),(-1,-2)],
			"R->T": [(0,0),(-1,0),(+2,0),(-1,+2),(+2,-1)],
			"T->R": [(0,0),(+1,0),(-2,0),(+1,-2),(-2,+1)],
			"T->L": [(0,0),(+2,0),(-1,0),(+2,+1),(-1,-2)],
			"L->T": [(0,0),(-2,0),(+1,0),(-2,-1),(+1,+2)],
			"L->O": [(0,0),(+1,0),(-2,0),(+1,-2),(-2,+1)],
			"O->L": [(0,0),(-1,0),(+2,0),(-1,+2),(+2,-1)]
		})
		super().__init__(tetriminoState,location)
	#테트리미노의 출력정보에 해당하는 리스트를 반환
	#ex) O상태의 s미노의 리턴값: [
	#	[0,1,1],
	#	[1,1,0],
	#	[0,0,0]	
	#]
	def GetPrintInfoBasedOnTetriminoState(self,tetriminoState):
		if tetriminoState == TetriminoState.O:
			return [
				[0,0,0,0,0],
				[1,1,1,1,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
			]
		elif tetriminoState == TetriminoState.R:
			return [
				[0,0,1,0,0],
				[0,0,1,0,0],
				[0,0,1,0,0],
				[0,0,1,0,0],
				[0,0,0,0,0],
			]
		elif tetriminoState == TetriminoState.T:
			return [
				[0,0,0,0,0],
				[0,0,0,0,0],
				[1,1,1,1,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
			]
		else:
			return [
				[0,1,0,0,0],
				[0,1,0,0,0],
				[0,1,0,0,0],
				[0,1,0,0,0],
				[0,0,0,0,0],
			]
	def GetColor(self):
		return ConstValue.IMINO_COLOR