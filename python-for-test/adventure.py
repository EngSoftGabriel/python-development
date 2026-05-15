import tkinter as tk
from tkinter import Canvas
import math

class PokemonYellowGame:
    """Jogo estilo Pokemon Yellow usando Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Yellow - Game Boy Style")
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
        """Desenhar o bonequinho estilo personagem vermelho e azul"""
        cx = self.player_x + self.player_size // 2  # Centro X
        cy = self.player_y + self.player_size // 2  # Centro Y
        
        # Cores
        RED = "#FF3333"
        CYAN = "#00FFFF"
        DARK_RED = "#CC0000"
        
        # Desenhar corpo (elipse/oval grande vermelha)
        # Corpo principal
        self.canvas.create_oval(
            cx - 14, cy - 4,
            cx + 14, cy + 20,
            fill=RED,
            outline=DARK_RED,
            width=2
        )
        
        # Desenhar cabeça (círculo vermelho no topo)
        self.canvas.create_oval(
            cx - 10, cy - 18,
            cx + 10, cy - 2,
            fill=RED,
            outline=DARK_RED,
            width=2
        )
        
        # Desenhar olhos (dois círculos ciano)
        eye_radius = 3
        # Olho esquerdo
        self.canvas.create_oval(
            cx - 5, cy - 12,
            cx - 5 + eye_radius * 2, cy - 12 + eye_radius * 2,
            fill=CYAN,
            outline="#0099FF",
            width=1
        )
        # Olho direito
        self.canvas.create_oval(
            cx + 5 - eye_radius, cy - 12,
            cx + 5 + eye_radius, cy - 12 + eye_radius * 2,
            fill=CYAN,
            outline="#0099FF",
            width=1
        )
        
        # Desenhar braço/detalhe azul (lado esquerdo)
        self.canvas.create_oval(
            cx - 18, cy + 2,
            cx - 8, cy + 14,
            fill=CYAN,
            outline="#0099FF",
            width=2
        )
        
        # Desenhar pernas (dois pequenos retângulos vermelhos)
        leg_width = 4
        # Perna esquerda
        self.canvas.create_rectangle(
            cx - 8, cy + 20,
            cx - 4, cy + 28,
            fill=RED,
            outline=DARK_RED,
            width=1
        )
        # Perna direita
        self.canvas.create_rectangle(
            cx + 4, cy + 20,
            cx + 8, cy + 28,
            fill=RED,
            outline=DARK_RED,
            width=1
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

        if self.keys_pressed.get('Left') or self.keys_pressed.get('a'):
            self.player_x -= self.player_speed

        if self.keys_pressed.get('Right') or self.keys_pressed.get('d'):
            self.player_x += self.player_speed        
        
        # Manter o bonequinho dentro dos limites
        if self.player_y < 0:
            self.player_y = 0
        if self.player_y + self.player_size > 288:
            self.player_y = 288 - self.player_size
    
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
    game = PokemonYellowGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
