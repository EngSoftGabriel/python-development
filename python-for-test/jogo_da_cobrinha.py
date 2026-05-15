import tkinter as tk
from tkinter import messagebox
import random
from enum import Enum

class Direcao(Enum):
    CIMA = (0, -10)
    BAIXO = (0, 10)
    ESQUERDA = (-10, 0)
    DIREITA = (10, 0)

class JogoDaCobrinha:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Jogo da Cobrinha")
        self.janela.geometry("400x400")
        self.janela.resizable(False, False)
        
        # Configurações do jogo
        self.tamanho_celula = 10
        self.largura = 400 // self.tamanho_celula  # 40
        self.altura = 400 // self.tamanho_celula   # 40
        self.velocidade = 100  # ms
        
        # Canvas para desenhar o jogo
        self.canvas = tk.Canvas(
            self.janela, 
            width=400, 
            height=400, 
            bg='black'
        )
        self.canvas.pack()
        
        # Label para pontuação
        self.label_pontos = tk.Label(
            self.janela, 
            text="Pontos: 0", 
            font=("Arial", 12),
            fg="white",
            bg="black"
        )
        self.label_pontos.pack()
        
        # Inicializar jogo
        self.reiniciar_jogo()
        
        # Controles
        self.janela.bind('<Up>', lambda e: self.mudar_direcao(Direcao.CIMA))
        self.janela.bind('<Down>', lambda e: self.mudar_direcao(Direcao.BAIXO))
        self.janela.bind('<Left>', lambda e: self.mudar_direcao(Direcao.ESQUERDA))
        self.janela.bind('<Right>', lambda e: self.mudar_direcao(Direcao.DIREITA))
        self.janela.bind('<w>', lambda e: self.mudar_direcao(Direcao.CIMA))
        self.janela.bind('<s>', lambda e: self.mudar_direcao(Direcao.BAIXO))
        self.janela.bind('<a>', lambda e: self.mudar_direcao(Direcao.ESQUERDA))
        self.janela.bind('<d>', lambda e: self.mudar_direcao(Direcao.DIREITA))
        self.janela.bind('<r>', lambda e: self.reiniciar_jogo())
        
        # Iniciar loop do jogo
        self.atualizar()
    
    def reiniciar_jogo(self):
        """Reinicia o jogo para o estado inicial"""
        # Cobrinha começa no meio da tela
        self.cobrinha = [
            (self.largura // 2, self.altura // 2),
            (self.largura // 2 - 1, self.altura // 2),
            (self.largura // 2 - 2, self.altura // 2)
        ]
        self.direcao = Direcao.DIREITA
        self.proxima_direcao = Direcao.DIREITA
        self.pontos = 0
        self.gerar_comida()
        self.game_over = False
    
    def gerar_comida(self):
        """Gera uma nova comida em posição aleatória"""
        while True:
            x = random.randint(0, self.largura - 1)
            y = random.randint(0, self.altura - 1)
            if (x, y) not in self.cobrinha:
                self.comida = (x, y)
                break
    
    def mudar_direcao(self, nova_direcao):
        """Muda a direção da cobrinha (evita movimento retrógrado)"""
        # Não permite virar 180 graus
        if (self.direcao.value[0] * -1 == nova_direcao.value[0] and
            self.direcao.value[1] * -1 == nova_direcao.value[1]):
            return
        self.proxima_direcao = nova_direcao
    
    def atualizar(self):
        """Atualiza o estado do jogo"""
        if not self.game_over:
            self.direcao = self.proxima_direcao
            
            # Calcula nova posição da cabeça
            x, y = self.cobrinha[0]
            dx, dy = self.direcao.value
            nova_x = (x + dx // self.tamanho_celula) % self.largura
            nova_y = (y + dy // self.tamanho_celula) % self.altura
            
            # Verifica colisão com a cobrinha
            if (nova_x, nova_y) in self.cobrinha:
                self.game_over = True
                messagebox.showinfo(
                    "Game Over", 
                    f"Cobrinha colidiu consigo mesma!\n\nPontos: {self.pontos}\n\nPressione 'R' para recomeçar"
                )
            else:
                # Move cobrinha
                self.cobrinha.insert(0, (nova_x, nova_y))
                
                # Verifica se comeu a comida
                if (nova_x, nova_y) == self.comida:
                    self.pontos += 10
                    self.velocidade = max(50, self.velocidade - 2)  # Aumenta velocidade
                    self.gerar_comida()
                else:
                    self.cobrinha.pop()
        
        self.desenhar()
        self.label_pontos.config(text=f"Pontos: {self.pontos}")
        
        self.janela.after(self.velocidade, self.atualizar)
    
    def desenhar(self):
        """Desenha o jogo no canvas"""
        self.canvas.delete("all")
        
        # Desenha cobrinha
        for i, (x, y) in enumerate(self.cobrinha):
            x1 = x * self.tamanho_celula
            y1 = y * self.tamanho_celula
            x2 = x1 + self.tamanho_celula
            y2 = y1 + self.tamanho_celula
            
            # Cabeça em cor diferente
            if i == 0:
                cor = '#00FF00'  # Verde brilhante
            else:
                cor = '#00AA00'  # Verde mais escuro
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline='green')
        
        # Desenha comida
        x, y = self.comida
        x1 = x * self.tamanho_celula
        y1 = y * self.tamanho_celula
        x2 = x1 + self.tamanho_celula
        y2 = y1 + self.tamanho_celula
        self.canvas.create_oval(x1, y1, x2, y2, fill='red', outline='darkred')
        
        # Mensagem de game over
        if self.game_over:
            self.canvas.create_text(
                200, 200,
                text="GAME OVER",
                font=("Arial", 24, "bold"),
                fill="red"
            )

if __name__ == "__main__":
    janela = tk.Tk()
    jogo = JogoDaCobrinha(janela)
    janela.mainloop()
