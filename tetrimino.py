from enum import Enum
class TetriminoKinds(Enum):
	Z = 1
	S = 2
	L = 3
	J = 4
	I = 5
	o = 6
	t = 7

class Tetrimino:
	def __init__(self,kind,)