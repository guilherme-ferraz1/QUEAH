class Position:
    
    def __init__(self, Status):
        self.status = Status

    def setStatus(self, Status: str):
        self.status = Status
    
    def getStatus(self) -> str:
        return self.status