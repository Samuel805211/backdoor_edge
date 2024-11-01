from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
import random

# Configurações do jogo
SNAKE_SIZE = 20
FOOD_SIZE = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)

class SnakeGame(Screen):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = (20, 0)
        self.food = self.spawn_food()
        self.obstacles = [self.spawn_obstacle() for _ in range(5)]
        self.score = 0
        Clock.schedule_interval(self.update, 0.2)
        self.bind(size=self.update_graphics)

    def on_enter(self):
        # Define o fundo preto quando entra na tela de jogo
        Window.clearcolor = (0, 0, 0, 1)

    def spawn_food(self):
        return (random.randint(0, (SCREEN_WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
                random.randint(0, (SCREEN_HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)

    def spawn_obstacle(self):
        return (random.randint(0, (SCREEN_WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
                random.randint(0, (SCREEN_HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)

    def on_touch_down(self, touch):
        head_x, head_y = self.snake[0]
        if touch.x > head_x and abs(touch.x - head_x) > abs(touch.y - head_y):
            self.snake_direction = (SNAKE_SIZE, 0)   # Direita
        elif touch.x < head_x and abs(touch.x - head_x) > abs(touch.y - head_y):
            self.snake_direction = (-SNAKE_SIZE, 0)  # Esquerda
        elif touch.y > head_y:
            self.snake_direction = (0, SNAKE_SIZE)   # Cima
        else:
            self.snake_direction = (0, -SNAKE_SIZE)  # Baixo

    def update(self, dt):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.snake_direction[0], head_y + self.snake_direction[1])

        if (new_head in self.snake or  
            new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or  
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
            new_head in self.obstacles):
            self.reset_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.update_graphics()

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = (20, 0)
        self.food = self.spawn_food()
        self.obstacles = [self.spawn_obstacle() for _ in range(5)]
        self.score = 0
        self.update_graphics()

    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0, 1, 0)
            for x, y in self.snake:
                Rectangle(pos=(x, y), size=(SNAKE_SIZE, SNAKE_SIZE))

            Color(1, 0, 0)
            Rectangle(pos=self.food, size=(FOOD_SIZE, FOOD_SIZE))

            Color(0, 0, 1)
            for obstacle in self.obstacles:
                Rectangle(pos=obstacle, size=(FOOD_SIZE, FOOD_SIZE))

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        Window.clearcolor = (1, 1, 1, 1)

        # Adiciona o fundo de imagem
        background = Image(source='download (2).jpg', pos_hint={'center_x': 0.5, 'center_y': 0.8}, size_hint=(1, 1))
        layout.add_widget(background)

        # Botões
        play_button = Button(text='Jogar', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0.5, 1, 0, 1), background_color=(0, 0, 0, 1), height=50, width=300)
        config_button = Button(text='Configuração', pos_hint={'center_x': 0.5, 'center_y': 0.3}, size_hint=(None, None), color=(1, 0, 0, 1), background_color=(0, 0, 0, 1), height=50, width=300)
        exit_button = Button(text='Sair do Jogo', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.2}, color=(1, 1, 0, 1), background_color=(1, 0, 0, 1), height=50, width=300)
        label = Label(text='Criador: Samuel Rodrigues Silva Lima', size_hint=(None, None), pos_hint={'center_x':0.5, 'center_y':0.1}, font_size=30, color=(1,0,0,1))
        layout.add_widget(label)

        # Adiciona os botões ao layout
        layout.add_widget(play_button)
        layout.add_widget(config_button)
        layout.add_widget(exit_button)

        # Liga o botão de "Jogar" para iniciar o jogo
        play_button.bind(on_press=self.start_game)
        exit_button.bind(on_press=self.exit_game)

        self.add_widget(layout)

    def start_game(self, instance):
        # Muda para o widget do jogo
        self.manager.current = 'game'

    def exit_game(self, instance):
        App.get_running_app().stop()

class SnakeApp(App):
    icon = 'download.jpg'  # Define o ícone do aplicativo

    def build(self):
        # Cria o gerenciador de telas
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SnakeGame(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()
