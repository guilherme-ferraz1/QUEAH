from tkinter import *
from tkinter import messagebox

LARGEFONT = ("Verdana", 35)
MEDIUMFONT = ("Verdana", 12)

MATRIZ_VISUALIZACAO = [
    [X, X, 1, X, X],
    [X, 1, 2, 3, X],
    [1, 2, 3, 4, 5],
    [X, 1, 2, 3, X],
    [X, X, 1, X, X]
]

CASAS_POSSIVEIS_PAR = [1, 2, 3]
CASAS_POSSIVEIS_IMPAR = [2, 3]

POSICOES_INICIAIS_VERMELHO = [[1, 2], [2, 4], [1, 3], [2, 3]]
POSICOES_INICIAIS_AZUL = [[2, 0], [3, 1], [2, 1], [3, 2]]


class Application:
    def __init__(self, master=None):
        # self.iniciarJogo()
        self.jogador1 = PhotoImage(file=f"images/jogador1.png")
        self.jogador2 = PhotoImage(file=f"images/jogador2.png")
        self.casaTabuleiro = PhotoImage(file=f"images/peça.png")
        self.pinoVermelho = PhotoImage(file=f"images/pinoVermelho.png")
        self.pinoAzul = PhotoImage(file=f"images/pinoAzul.png")
        self.tabuleiro = Frame(master, width=600, height=550)
        self.tabuleiro.place(relx=0.5, rely=0.5, anchor=CENTER)
        turn = Label(master, text="Vez de: Jogador 1", font=LARGEFONT)
        turn.place(relx=0.5, rely=0.05, anchor=CENTER)

        fotoJogador1 = Label(master, image=self.jogador1)
        fotoJogador1.image = self.jogador1
        fotoJogador1.place(relx=0.05, rely=0.43, anchor=CENTER)

        fotoJogador2 = Label(master, image=self.jogador2)
        fotoJogador2.image = self.jogador2
        fotoJogador2.place(relx=0.95, rely=0.43, anchor=CENTER)

        player1 = Label(master, text="Jogador 1", font=MEDIUMFONT)
        player1.place(relx=0.05, rely=0.35, anchor=CENTER)

        player2 = Label(master, text="Jogador 2", font=MEDIUMFONT)
        player2.place(relx=0.95, rely=0.35, anchor=CENTER)

        piecesLeft1 = Label(
            master, text="Peças faltantes: 6", font=MEDIUMFONT)
        piecesLeft1.place(relx=0.07, rely=0.5, anchor=CENTER)

        piecesLeft2 = Label(
            master, text="Peças faltantes: 6", font=MEDIUMFONT)
        piecesLeft2.place(relx=0.93, rely=0.5, anchor=CENTER)

        restart = Button(
            master, text="Reiniciar partida", font=MEDIUMFONT, command=self.reiniciarPartida)
        restart.place(relx=0.9, rely=0.05, anchor=CENTER)

        for i in range(5):
            for j in range(5):
                if MATRIZ_VISUALIZACAO[i][j] != X:
                    if [i, j] in POSICOES_INICIAIS_AZUL:
                        peca = Label(self.tabuleiro,
                                     image=self.pinoAzul)
                        peca.place(x=80 * j + 100, y=80 * i + 120)
                        peca.bind("<Button-1>",
                                  lambda e: self.casaClicada())
                        peca.image = self.pinoAzul
                    elif [i, j] in POSICOES_INICIAIS_VERMELHO:
                        peca = Label(self.tabuleiro,
                                     image=self.pinoVermelho)
                        peca.place(x=80 * j + 100, y=80 * i + 120)
                        peca.bind("<Button-1>",
                                  lambda e: self.casaClicada())
                        peca.image = self.pinoVermelho
                    else:
                        peca = Label(self.tabuleiro,
                                     image=self.casaTabuleiro)
                        peca.place(x=80 * j + 100, y=80 * i + 120)
                        peca.bind("<Button-1>",
                                  lambda e: self.casaClicada())
                        peca.image = self.casaTabuleiro
                    peca = Label(self.tabuleiro, image=self.casaTabuleiro)

    def iniciarJogo(self):
        messagebox.showinfo("showinfo", "Bem vindo ao QUEAH! Boa diversão :)")

    def finalizarJogo(self):
        messagebox.showinfo(
            "showinfo", "Jogador 1 venceu!! Clique para jogar novamente.")

    def reiniciarPartida(self):
        messagebox.showinfo(
            "showinfo", "Partida reiniciada.")

    def casaClicada(self):
        messagebox.showinfo(
            "showinfo", "Uma casa do tabuleiro foi clicada.")


root = Tk()
root.geometry("1000x600")
root.title("QUEAH - Análise e projeto de sistemas")

Application(root)
root.mainloop()
