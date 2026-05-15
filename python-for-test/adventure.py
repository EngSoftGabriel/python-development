import tkinter as tk
from tkinter import Canvas
import math

class AdventureGame:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Adventure")
        self.root.geometry("320x288")
        self.root.resizable(False, False)
        
        # Cores
        self.BLACK = "#000000"
        self.YELLOW = "#FFFF00"
        self.WHITE = "#FFFFFF"
        
        # Criar canvas
        self.canvas = Canvas(
            root, 
            width=320, 
            height=288, 
            bg=self.BLACK, 
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Posição do bonequinho (x, y)
        self.player_x = 160 - 16  # Centro da tela
        self.player_y = 144 - 16  # Centro da tela
        self.player_size = 32
        self.player_speed = 4
        
        # Dicionário para rastrear teclas pressionadas
        self.keys_pressed = {}
        
        # Desenhar bonequinho
        self.player_oval = None
        self.draw_player()
        
        # Bind eventos de teclado
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.focus()
        
        # Iniciar o loop do jogo
        self.update_game()
    
    def draw_player(self):
        """Desenhar o bonequinho amarelo com contorno branco"""
        x1 = self.player_x
        y1 = self.player_y
        x2 = self.player_x + self.player_size
        y2 = self.player_y + self.player_size
        
        # Apagar o bonequinho anterior se existir
        if self.player_oval is not None:
            self.canvas.delete(self.player_oval)
        
        # Desenhar quadrado amarelo com contorno branco
        self.player_oval = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=self.YELLOW,
            outline=self.WHITE,
            width=2
        )
        
        # Desenhar olhos (pequenos círculos pretos)
        eye_size = 4
        # Olho esquerdo
        self.canvas.create_oval(
            x1 + 8, y1 + 8,
            x1 + 8 + eye_size, y1 + 8 + eye_size,
            fill=self.BLACK
        )
        # Olho direito
        self.canvas.create_oval(
            x2 - 12, y1 + 8,
            x2 - 12 + eye_size, y1 + 8 + eye_size,
            fill=self.BLACK
        )
        
        # Desenhar boca (pequena linha preta)
        mouth_y = y1 + 20
        self.canvas.create_line(
            x1 + 10, mouth_y,
            x2 - 10, mouth_y,
            fill=self.BLACK,
            width=2
        )
    
    def on_key_press(self, event):
        """Registrar tecla pressionada"""
        self.keys_pressed[event.keysym] = True
    
    def on_key_release(self, event):
        """Registrar tecla liberada"""
        if event.keysym in self.keys_pressed:
            self.keys_pressed[event.keysym] = False
    
    def handle_input(self):
        """Processar entrada do teclado"""
        # Movimento para cima
        if self.keys_pressed.get('Up') or self.keys_pressed.get('w'):
            self.player_y -= self.player_speed
        
        # Movimento para baixo
        if self.keys_pressed.get('Down') or self.keys_pressed.get('s'):
            self.player_y += self.player_speed

        # Movimento para a esquerda
        if self.keys_pressed.get('Left') or self.keys_pressed.get('a'):
            self.player_x -= self.player_speed

        # Movimento para a direita
        if self.keys_pressed.get('Right') or self.keys_pressed.get('d'):
            self.player_x += self.player_speed

        # Manter o bonequinho dentro dos limites
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y + self.player_size > 288:
            self.player_y = 288 - self.player_size

        # Manter o bonequinho dentro dos limites horizontais
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x + self.player_size > 320:
            self.player_x = 320 - self.player_size
    
    def update_game(self):
        """Loop principal do jogo"""
        # Processar entrada
        self.handle_input()
        
        # Limpar canvas
        self.canvas.delete("all")
        
        # Redesenhar tudo
        self.draw_player()
        
        # Agendar próxima atualização (60 FPS)
        self.root.after(16, self.update_game)


def main():
    root = tk.Tk()
    game = AdventureGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
