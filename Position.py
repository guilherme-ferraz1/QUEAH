class Position:
    def __init__(self, status):
        self.status = status

    def setStatus(self, status: str):
        self.status = status
    
    def getStatus(self) -> str:
        return self.status