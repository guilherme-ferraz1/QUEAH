from inspect import _void
from tkinter import *
from tkinter import messagebox
from Location import Location
from Player import Player
from Position import Position

class Board:
    def __init__(self):
        self.player1 = Player(True)
        self.player2 = Player(False)
        self.turnPlayer = 1
        self.selectedLocation = None
        self.selectedDestiny = None
        self.matchStatus = 0
        self.positions = None
        self.vencedor = None
        self.redefinirPartida()

    def setStatusMatch(self) -> _void:
        if self.matchStatus == 0:
            self.matchStatus = 1
        if self.matchStatus == 1:
            self.matchStatus = 0
        
    def passarTurno(self) -> _void:
        turno1 = self.player1.turn == True
        if (turno1):
            self.player1.setTurn()
            self.player2.setTurn()
            self.turnPlayer = 2
        else:
            self.player1.setTurn()
            self.player2.setTurn()
            self.turnPlayer = 1

    def definirJogadorInicial(self) -> int:
        turno1 = self.player1.turn == True
        if (turno1):
            return 1
        else:
            self.player1.turn = True
            return 1

    def verificarSeInimigo(self, selectedDestiny: Location) -> bool:
        turno1 = self.player1.turn == True
        if (turno1):
            if self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].getStatus() == 'OCUPADA_2':
                return True
            else:
                return False
        else:
            if self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].getStatus() == 'OCUPADA_1':
                return True
            else:
                return False
    
    def definirVencedor(self) -> _void: 
        turno1 = self.player1.turn == True
        if (turno1):
            self.player1.setWinner()
            messagebox.showinfo("showinfo", "Jogador 1 venceu!!!!")
            self.redefinirPartida()
        else:
            self.player2.setWinner()
            messagebox.showinfo("showinfo", "Jogador 2 venceu!!!!")
            self.redefinirPartida()
        self.setStatusMatch()

    def redefinirPecas(self) -> _void:
        self.positions = [
            [Position('RESERVA_1'), Position('INATIVA'), Position('LIVRE'), Position('INATIVA'), Position('INATIVA')],
            [Position('INATIVA'), Position('LIVRE'), Position('OCUPADA_2'), Position('OCUPADA_2'), Position('INATIVA')],
            [Position('OCUPADA_1'), Position('OCUPADA_1'), Position('LIVRE'), Position('OCUPADA_2'), Position('OCUPADA_2')],
            [Position('INATIVA'), Position('OCUPADA_1'), Position('OCUPADA_1'), Position('LIVRE'), Position('INATIVA')],
            [Position('INATIVA'), Position('INATIVA'), Position('LIVRE'), Position('INATIVA'), Position('RESERVA_2')]
        ]
    
    def redefinirPartida(self) -> _void:
        self.redefinirPecas()
        self.turnPlayer = self.definirJogadorInicial()
        self.resetarJogadores()
        self.limparPosicoesSelecionadas()
        self.setStatusMatch()
    
    def limparPosicoesSelecionadas(self) -> _void:
        self.selectedDestiny = None 
        self.selectedLocation = None
    
    def resetarJogadores(self) -> _void:
        self.player1 = Player(True)
        self.player2 = Player(False)

    def movimentarPeca(self, selectedDestiny: Location) -> _void:
        turno1 = self.player1.turn == True
        if (turno1):
            self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].setStatus('OCUPADA_1')
        else:
            self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].setStatus('OCUPADA_2')

    def validarPosicao(self, selectedLocation: Location) -> bool:
        if self.turnPlayer == 1:
            if self.positions[selectedLocation.getLine()][selectedLocation.getColumn()].getStatus() == 'OCUPADA_1':
                return True
            else:
                return False
        if self.turnPlayer == 2:
            if self.positions[selectedLocation.getLine()][selectedLocation.getColumn()].getStatus() == 'OCUPADA_2':
                return True
            else:
                return False

    def validarPosicaoDestino(self, selectedLocation: Location, selectedDestiny: Location) -> bool:
        linhaPosicao = selectedLocation.getLine()
        colunaPosicao = selectedLocation.getColumn()
        linhaPosicaoDestino = selectedDestiny.getLine()
        colunaPosicaoDestino = selectedDestiny.getColumn()
        if linhaPosicao == linhaPosicaoDestino:
            if colunaPosicao + 1 == colunaPosicaoDestino or colunaPosicao -1 == colunaPosicaoDestino:
                return True
        if colunaPosicao == colunaPosicaoDestino:
            if linhaPosicao + 1 == linhaPosicaoDestino or linhaPosicao -1 == linhaPosicaoDestino:
                return True
        return False
    
    def getUserPecasOponentes(self) -> int:
        if self.turnPlayer == 1:
            return self.player2.piecesOnBoard
        else:
            return self.player1.piecesOnBoard

    def adicionarPeca(self, selectedDestiny: Location) -> int:
        if self.turnPlayer == 1:
            self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].setStatus('OCUPADA_1')
            self.player1.piecesOnBoard = self.player1.piecesOnBoard + 1
            self.player1.piecesReserved = self.player1.piecesReserved - 1
        if self.turnPlayer == 2:
            self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].setStatus('OCUPADA_2')
            self.player2.piecesOnBoard = self.player2.piecesOnBoard + 1
            self.player2.piecesReserved = self.player2.piecesReserved - 1

    def posicaoSeguinteIsVazia(self, selectedLocation: Location, selectedDestiny: Location) -> bool:
        linhaPosicao = selectedLocation.getLine()
        colunaPosicao = selectedLocation.getColumn()
        linhaPosicaoDestino = selectedDestiny.getLine()
        colunaPosicaoDestino = selectedDestiny.getColumn()
        if linhaPosicao == linhaPosicaoDestino:
            if colunaPosicao + 1 == colunaPosicaoDestino:
                return self.positions[linhaPosicaoDestino][colunaPosicaoDestino + 1].getStatus() == 'LIVRE'
            if colunaPosicao - 1 == colunaPosicaoDestino:
                return self.positions[linhaPosicaoDestino][colunaPosicaoDestino - 1].getStatus() == 'LIVRE'
        if colunaPosicao == colunaPosicaoDestino:
            if linhaPosicao + 1 == linhaPosicaoDestino:
                return self.positions[linhaPosicaoDestino + 1][colunaPosicaoDestino].getStatus() == 'LIVRE'
            if linhaPosicao - 1 == linhaPosicaoDestino:
                return self.positions[linhaPosicaoDestino - 1][colunaPosicaoDestino].getStatus() == 'LIVRE'
        return False

    def verificarBloqueioMovimento(self) -> bool:
        for i in range(5):
            for j in range(5):
                if self.turnPlayer == 2:
                    if self.positions[i][j].getStatus() == 'OCUPADA_1':
                        if self.positions[i][j + 1].getStatus() == 'LIVRE':
                            return False
                        if self.positions[i][j - 1].getStatus() == 'LIVRE' and j != 0:
                            return False
                        if self.positions[i + 1][j].getStatus() == 'LIVRE':
                            return False
                        if self.positions[i - 1][j].getStatus() == 'LIVRE' and i != 0:
                            return False
                        if self.positions[i][j + 1].getStatus() == 'OCUPADA_2' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i, j + 1)):
                            return False
                        if self.positions[i][j - 1].getStatus() == 'OCUPADA_2' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i, j - 1)) and j != 0:
                            return False
                        if self.positions[i + 1][j].getStatus() == 'OCUPADA_2' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i + 1, j)):
                            return False
                        if self.positions[i - 1][j].getStatus() == 'OCUPADA_2' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i - 1, j)) and i != 0:
                            return False
                if self.turnPlayer == 1:
                    if self.positions[i][j].getStatus() == 'OCUPADA_2':
                        if self.positions[i][j + 1].getStatus() == 'LIVRE':
                            return False
                        if self.positions[i][j - 1].getStatus() == 'LIVRE' and j != 0:
                            return False
                        if self.positions[i + 1][j].getStatus() == 'LIVRE':
                            return False
                        if self.positions[i - 1][j].getStatus() == 'LIVRE' and i != 0:
                            return False
                        if self.positions[i][j + 1].getStatus() == 'OCUPADA_1' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i, j + 1)):
                            return False
                        if self.positions[i][j - 1].getStatus() == 'OCUPADA_1' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i, j - 1)) and j != 0:
                            return False
                        if self.positions[i + 1][j].getStatus() == 'OCUPADA_1' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i + 1, j)):
                            return False
                        if self.positions[i - 1][j].getStatus() == 'OCUPADA_1' and self.posicaoSeguinteIsVazia(Location(i, j), Location(i - 1, j)) and i != 0:
                            return False
        return True

    def validarSeVazio(self, selectedDestiny: Location) -> bool:
        return self.positions[selectedDestiny.getLine()][selectedDestiny.getColumn()].getStatus() == 'LIVRE'

    def removerPeca(self, location: Location) -> _void:
        self.positions[location.getLine()][location.getColumn()].setStatus('LIVRE')

    def movimentarPecaAdjacente(self, selectedLocation: Location, selectedDestiny: Location) -> _void:
        linhaPosicao = selectedLocation.getLine()
        colunaPosicao = selectedLocation.getColumn()
        linhaPosicaoDestino = selectedDestiny.getLine()
        colunaPosicaoDestino = selectedDestiny.getColumn()
        if self.turnPlayer == 1:
            self.player2.piecesOnBoard = self.player2.piecesOnBoard - 1
            if linhaPosicao == linhaPosicaoDestino:
                if colunaPosicao + 1 == colunaPosicaoDestino:
                    self.positions[linhaPosicaoDestino][colunaPosicaoDestino + 1].setStatus('OCUPADA_1')
                if colunaPosicao - 1 == colunaPosicaoDestino:
                    self.positions[linhaPosicaoDestino][colunaPosicaoDestino - 1].setStatus('OCUPADA_1')
            if colunaPosicao == colunaPosicaoDestino:
                if linhaPosicao + 1 == linhaPosicaoDestino:
                    self.positions[linhaPosicaoDestino + 1][colunaPosicaoDestino].setStatus('OCUPADA_1')
                if linhaPosicao - 1 == linhaPosicaoDestino:
                    self.positions[linhaPosicaoDestino - 1][colunaPosicaoDestino].setStatus('OCUPADA_1')
        else:
            self.player1.piecesOnBoard = self.player1.piecesOnBoard - 1
            if linhaPosicao == linhaPosicaoDestino:
                if colunaPosicao + 1 == colunaPosicaoDestino:
                    self.positions[linhaPosicaoDestino][colunaPosicaoDestino + 1].setStatus('OCUPADA_2')
                if colunaPosicao - 1 == colunaPosicaoDestino:
                    self.positions[linhaPosicaoDestino][colunaPosicaoDestino - 1].setStatus('OCUPADA_2')
            if colunaPosicao == colunaPosicaoDestino:
                if linhaPosicao + 1 == linhaPosicaoDestino:
                    self.positions[linhaPosicaoDestino + 1][colunaPosicaoDestino].setStatus('OCUPADA_2')
                if linhaPosicao - 1 == linhaPosicaoDestino:
                    self.positions[linhaPosicaoDestino - 1][colunaPosicaoDestino].setStatus('OCUPADA_2')

    def clickTabuleiro(self, location: Location): 
        if self.selectedLocation is None:
            self.selectedLocation = location
        else:
            self.selectedDestiny = location
    
    def validarReserva(self, player: int, posicao: Location):
        if player == 1:
            return self.player1.getReservas() > 0 and self.player1.piecesOnBoard < 4 and self.positions[posicao.getLine()][posicao.getColumn()].getStatus() == 'RESERVA_1'
        if player == 2:
            return self.player2.getReservas() > 0 and self.player2.piecesOnBoard < 4 and self.positions[posicao.getLine()][posicao.getColumn()].getStatus() == 'RESERVA_2'

    def verificarVencedor(self) -> bool:
        pecasOpositor = self.getUserPecasOponentes()
        if pecasOpositor == 0:
            self.definirVencedor()
            return True
        else:
            if pecasOpositor > 2:
                self.passarTurno()
            else:
                isBloqueado = self.verificarBloqueioMovimento()
                if isBloqueado == False:
                    self.passarTurno()
                else:
                    self.definirVencedor()
                    return True
        return False

        