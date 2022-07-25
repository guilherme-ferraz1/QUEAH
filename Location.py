class Location:
  def __init__(self, line, column):
    self.line = line
    self.column = column

  def getLine(self) -> int:
    return self.line

  def getColumn(self) -> int: 
    return self.column
