from tkinter import *
from tkinter import messagebox
from Board import Board
from Location import Location
from inspect import _void
from Position import Position

LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 12)

class PlayerInterface:
    def __init__(self, master=None):
        self.fotoJogador1 = PhotoImage(file=f"images/jogador1.png")
        self.fotoJogador2 = PhotoImage(file=f"images/jogador2.png")
        self.casaTabuleiro = PhotoImage(file=f"images/peça.png")
        self.pinoVermelho = PhotoImage(file=f"images/pinoVermelho.png")
        self.pinoAzul = PhotoImage(file=f"images/pinoAzul.png")
        self.tabuleiro = Frame(master, width=600, height=550)
        self.tabuleiro.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.board = Board()
        self.isAdicionarPeca = False
        self.posicoesIniciais = [
            [Position('RESERVA_1'), Position('INATIVA'), Position('LIVRE'), Position('INATIVA'), Position('INATIVA')],
            [Position('INATIVA'), Position('LIVRE'), Position('OCUPADA_2'), Position('OCUPADA_2'), Position('INATIVA')],
            [Position('OCUPADA_1'), Position('OCUPADA_1'), Position('LIVRE'), Position('OCUPADA_2'), Position('OCUPADA_2')],
            [Position('INATIVA'), Position('OCUPADA_1'), Position('OCUPADA_1'), Position('LIVRE'), Position('INATIVA')],
            [Position('INATIVA'), Position('INATIVA'), Position('LIVRE'), Position('INATIVA'), Position('RESERVA_2')]
        ]

        fotoJogador1 = Label(master, image=self.fotoJogador1)
        fotoJogador1.place(relx=0.05, rely=0.43, anchor=CENTER)

        fotoJogador2 = Label(master, image=self.fotoJogador2)
        fotoJogador2.place(relx=0.95, rely=0.43, anchor=CENTER)

        player1 = Label(master, text="Jogador 1", font=MEDIUMFONT)
        player1.place(relx=0.05, rely=0.35, anchor=CENTER)

        player2 = Label(master, text="Jogador 2", font=MEDIUMFONT)
        player2.place(relx=0.95, rely=0.35, anchor=CENTER)

        self.iniciarInterfaceUsuario()

    def setIsAdicionarPeca(self, isAdicionar) -> _void:
        self.isAdicionarPeca = isAdicionar

    def clickTabuleiro(self, linha, coluna) -> _void:
        posicao = Location(linha, coluna)
        # VERIFICA SE ENTRA NO CASO DE USO DE ADICIONAR PEÇA
        if self.isAdicionarPeca:
            self.board.limparPosicoesSelecionadas()
            posicaoDestinoValida = self.board.validarSeVazio(posicao)
            if posicaoDestinoValida == False:
                messagebox.showinfo("showinfo", "Movimento irregular")
            else:
                self.board.adicionarPeca(posicao)
                self.board.passarTurno()
                self.setIsAdicionarPeca(False)
                self.atualizaInterface()
        else:
            # VERIFICA SE ENTRA NO CASO DE USO DE MOVIMENTAR PEÇA
            if self.board.turnPlayer == 1:
                if self.board.player1.getPecas() < 4 and self.board.player1.getReservas() > 0:
                    messagebox.showinfo("showinfo", "Você deve adicionar uma peça reserva")
            if self.board.turnPlayer == 2:
                if self.board.player2.getPecas() < 4 and self.board.player2.getReservas() > 0:
                    messagebox.showinfo("showinfo", "Você deve adicionar uma peça reserva")

            if self.board.selectedLocation is None:
                self.board.clickTabuleiro(posicao)
                posicaoValida = self.board.validarPosicao(self.board.selectedLocation)
                if posicaoValida == False:
                    messagebox.showinfo("showinfo", "Movimento irregular")
                    self.board.limparPosicoesSelecionadas()
            else:
                self.board.clickTabuleiro(posicao)
                posicaoDestinoValida = self.board.validarPosicaoDestino(self.board.selectedLocation, self.board.selectedDestiny)
                if posicaoDestinoValida == False:
                    messagebox.showinfo("showinfo", "Movimento irregular")
                    self.board.limparPosicoesSelecionadas()
                else:
                    isVazio = self.board.validarSeVazio(self.board.selectedDestiny)
                    if isVazio == True:
                        self.board.removerPeca(self.board.selectedLocation)
                        self.board.movimentarPeca(self.board.selectedDestiny)
                        # CASO DE USO VERIFICAR VENCEDOR APÓS A AÇÃO DO JOGADOR
                        temVencedor = self.board.verificarVencedor()
                        if temVencedor == True:
                            self.iniciarInterfaceUsuario()
                            return
                        self.atualizaInterface()
                        self.board.limparPosicoesSelecionadas()
                    else:
                        isInimigo = self.board.verificarSeInimigo(self.board.selectedDestiny)
                        if isInimigo == False:
                            messagebox.showinfo("showinfo", "Movimento irregular")
                            self.board.limparPosicoesSelecionadas()
                        else:
                            isSeguinteVazia = self.board.posicaoSeguinteIsVazia(self.board.selectedLocation, self.board.selectedDestiny)
                            if isSeguinteVazia == False:
                                messagebox.showinfo("showinfo", "Movimento irregular")
                                self.board.limparPosicoesSelecionadas()
                            else:
                                self.board.removerPeca(self.board.selectedLocation)
                                self.board.removerPeca(self.board.selectedDestiny)
                                self.board.movimentarPecaAdjacente(self.board.selectedLocation, self.board.selectedDestiny)
                                # CASO DE USO VERIFICAR VENCEDOR APÓS A AÇÃO DO JOGADOR
                                temVencedor = self.board.verificarVencedor()
                                if temVencedor == True:
                                    self.iniciarInterfaceUsuario()
                                    return
                                self.atualizaInterface()
                                self.board.limparPosicoesSelecionadas()

    def clickReservas(self, linha, coluna):
        # CASO DE USO ADICIONAR PEÇA
        posicao = Location(linha, coluna)
        reservaPecasJogadorDaVez = self.board.validarReserva(self.board.turnPlayer, posicao)
        if reservaPecasJogadorDaVez == True:
            self.setIsAdicionarPeca(True)
        else:
            self.setIsAdicionarPeca(False)
            messagebox.showinfo("showinfo", "Jogador não tem mais peças reservas ou não clickou no seu monte.")
    

    def iniciarInterfaceUsuario(self) -> _void:
        turn = Label(None, text=("Vez de: Jogador " + str(self.board.turnPlayer)), font=LARGEFONT)
        turn.place(relx=0.5, rely=0.05, anchor=CENTER)

        piecesLeft1 = Label(None, text="Peças reservas: " + str(self.board.player1.piecesReserved), font=MEDIUMFONT)
        piecesLeft1.place(relx=0.07, rely=0.5, anchor=CENTER)

        piecesLeft2 = Label(None, text="Peças reservas: " + str(self.board.player2.piecesReserved), font=MEDIUMFONT)
        piecesLeft2.place(relx=0.93, rely=0.5, anchor=CENTER)
    
        self.board.redefinirPartida()

        for i in range(5):
            for j in range(5):
                if self.posicoesIniciais[i][j].getStatus() == 'OCUPADA_1':
                    peca = Label(self.tabuleiro, image=self.pinoAzul)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.pinoAzul
                if self.posicoesIniciais[i][j].getStatus() == 'OCUPADA_2':
                    peca = Label(self.tabuleiro, image=self.pinoVermelho)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.pinoVermelho
                if self.posicoesIniciais[i][j].getStatus() == 'LIVRE':
                    peca = Label(self.tabuleiro, image=self.casaTabuleiro)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.casaTabuleiro
                    peca = Label(self.tabuleiro, image=self.casaTabuleiro)
                if self.posicoesIniciais[i][j].getStatus() == 'RESERVA_1' and self.board.player1.getReservas() > 0:
                    peca = Label(self.tabuleiro, image=self.pinoAzul)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickReservas(linha, coluna))
                    peca.image = self.pinoAzul
                if self.posicoesIniciais[i][j].getStatus() == 'RESERVA_2' and self.board.player2.getReservas() > 0:
                    peca = Label(self.tabuleiro, image=self.pinoVermelho)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickReservas(linha, coluna))
                    peca.image = self.pinoVermelho

    def atualizaInterface(self) -> _void:
        turn = Label(None, text=("Vez de: Jogador " + str(self.board.turnPlayer)), font=LARGEFONT)
        turn.place(relx=0.5, rely=0.05, anchor=CENTER)
    
        piecesLeft1 = Label(None, text="Peças reservas: " + str(self.board.player1.getReservas()), font=MEDIUMFONT)
        piecesLeft1.place(relx=0.07, rely=0.5, anchor=CENTER)

        piecesLeft2 = Label(None, text="Peças reservas: " + str(self.board.player2.getReservas()), font=MEDIUMFONT)
        piecesLeft2.place(relx=0.93, rely=0.5, anchor=CENTER)
        
        for i in range(5):
            for j in range(5):
                if self.board.positions[i][j].getStatus() == 'OCUPADA_1':
                    peca = Label(self.tabuleiro, image=self.pinoAzul)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.pinoAzul
                if self.board.positions[i][j].getStatus() == 'OCUPADA_2':
                    peca = Label(self.tabuleiro, image=self.pinoVermelho)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.pinoVermelho
                if self.board.positions[i][j].getStatus() == 'LIVRE':
                    peca = Label(self.tabuleiro, image=self.casaTabuleiro)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickTabuleiro(linha, coluna))
                    peca.image = self.casaTabuleiro
                    peca = Label(self.tabuleiro, image=self.casaTabuleiro)
                if self.board.positions[i][j].getStatus() == 'RESERVA_1' and self.board.player1.getReservas() > 0:
                    peca = Label(self.tabuleiro, image=self.pinoAzul)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    pos = [i,j]
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickReservas(linha, coluna))
                    peca.image = self.pinoAzul
                if self.board.positions[i][j].getStatus() == 'RESERVA_2' and self.board.player2.getReservas() > 0:
                    peca = Label(self.tabuleiro, image=self.pinoVermelho)
                    peca.place(x=80 * j + 100, y=80 * i + 120)
                    peca.bind("<Button-1>", lambda event, linha=i, coluna=j: self.clickReservas(linha, coluna))
                    peca.image = self.pinoVermelho

root = Tk()
root.geometry("1200x600")
root.title("QUEAH - Análise e projeto de sistemas")

PlayerInterface(root)
root.mainloop()