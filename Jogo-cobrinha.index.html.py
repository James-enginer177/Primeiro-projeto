import random
import tkinter as tk

TAMANHO = 20          # tamanho de cada quadrado (pixels)
COLUNAS = 24
LINHAS = 24
VELOCIDADE_INICIAL = 130  # milissegundos (menor = mais rápido)
VELOCIDADE_MINIMA = 60


class Cobrinha:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Jogo da Cobrinha")
        janela.resizable(False, False)

        self.topo = tk.Label(janela, font=("Arial", 14, "bold"))
        self.topo.pack(pady=4)

        self.canvas = tk.Canvas(
            janela, width=COLUNAS * TAMANHO, height=LINHAS * TAMANHO,
            bg="#1e293b", highlightthickness=0,
        )
        self.canvas.pack()

        self.recorde = 0
        janela.bind("<Key>", self.tecla)
        self.novo_jogo()

    def novo_jogo(self):
        self.corpo = [(12, 12), (11, 12), (10, 12)]
        self.direcao = (1, 0)
        self.proxima = (1, 0)
        self.pontos = 0
        self.velocidade = VELOCIDADE_INICIAL
        self.rodando = True
        self.pausado = False
        self.nova_comida()
        self.atualizar_placar()
        self.passo()

    def nova_comida(self):
        while True:
            pos = (random.randrange(COLUNAS), random.randrange(LINHAS))
            if pos not in self.corpo:
                self.comida = pos
                return

    def atualizar_placar(self):
        self.topo.config(text=f"Pontos: {self.pontos}   Recorde: {self.recorde}")

    def tecla(self, evento):
        k = evento.keysym.lower()
        movimentos = {
            "up": (0, -1), "w": (0, -1),
            "down": (0, 1), "s": (0, 1),
            "left": (-1, 0), "a": (-1, 0),
            "right": (1, 0), "d": (1, 0),
        }
        if k in movimentos:
            dx, dy = movimentos[k]
            # não deixa a cobrinha voltar para trás
            if (dx, dy) != (-self.direcao[0], -self.direcao[1]):
                self.proxima = (dx, dy)
        elif k == "space":
            if self.rodando:
                self.pausado = not self.pausado
                if not self.pausado:
                    self.passo()
                else:
                    self.mensagem("Pausado\n(espaço para continuar)")
        elif k == "return" and not self.rodando:
            self.novo_jogo()

    def passo(self):
        if not self.rodando or self.pausado:
            return

        self.direcao = self.proxima
        x, y = self.corpo[0]
        cabeca = (x + self.direcao[0], y + self.direcao[1])

        bateu_parede = not (0 <= cabeca[0] < COLUNAS and 0 <= cabeca[1] < LINHAS)
        if bateu_parede or cabeca in self.corpo:
            self.fim_de_jogo()
            return

        self.corpo.insert(0, cabeca)
        if cabeca == self.comida:
            self.pontos += 1
            self.recorde = max(self.recorde, self.pontos)
            self.velocidade = max(VELOCIDADE_MINIMA, self.velocidade - 3)
            self.nova_comida()
            self.atualizar_placar()
        else:
            self.corpo.pop()

        self.desenhar()
        self.janela.after(self.velocidade, self.passo)

    def desenhar(self):
        self.canvas.delete("all")
        cx, cy = self.comida
        self.canvas.create_oval(
            cx * TAMANHO + 2, cy * TAMANHO + 2,
            (cx + 1) * TAMANHO - 2, (cy + 1) * TAMANHO - 2,
            fill="#ef4444", outline="",
        )
        for i, (x, y) in enumerate(self.corpo):
            cor = "#4ade80" if i == 0 else "#22c55e"
            self.canvas.create_rectangle(
                x * TAMANHO + 1, y * TAMANHO + 1,
                (x + 1) * TAMANHO - 1, (y + 1) * TAMANHO - 1,
                fill=cor, outline="",
            )

    def mensagem(self, texto):
        self.canvas.create_text(
            COLUNAS * TAMANHO // 2, LINHAS * TAMANHO // 2,
            text=texto, fill="white", font=("Arial", 18, "bold"), justify="center",
        )

    def fim_de_jogo(self):
        self.rodando = False
        self.mensagem(f"Fim de jogo! {self.pontos} pontos\n\nEnter para jogar de novo")


if __name__ == "__main__":
    janela = tk.Tk()
    Cobrinha(janela)
    janela.mainloop()
    