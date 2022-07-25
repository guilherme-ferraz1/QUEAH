class Player:
  def __init__(self, turn):
    self.piecesReserved = 6
    self.piecesOnBoard = 4
    self.turn = turn
    self.winner = False

  def getPecas(self) -> int:
    return self.piecesOnBoard

  def getReservas(self) -> int:
    return self.piecesReserved

  def setWinner(self):
    self.winner = True

  def setTurn(self):
    if self.turn == True:
      self.turn = False
    else:
      self.turn = True
