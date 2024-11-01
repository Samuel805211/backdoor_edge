from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import threading
import json

class PermissionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Texto inicial e botões de permissão
        layout.add_widget(Label(text="Conceda permissões para o aplicativo"))

        # ToggleButtons para cada permissão
        self.permissions = {
            'camera': ToggleButton(text='Permitir Câmera', state='normal'),
            'contacts': ToggleButton(text='Permitir Contatos', state='normal'),
            'sms': ToggleButton(text='Permitir SMS', state='normal')
        }

        for perm in self.permissions.values():
            layout.add_widget(perm)

        # Botão de confirmação
        confirm_button = Button(text="Confirmar Permissões")
        confirm_button.bind(on_press=self.confirm_permissions)
        layout.add_widget(confirm_button)

        self.add_widget(layout)

    def confirm_permissions(self, instance):
        # Coleta as permissões do usuário e envia para a tela principal
        permissions = {perm: btn.state == 'down' for perm, btn in self.permissions.items()}
        self.manager.get_screen('main').start_socket_connection(permissions)
        self.manager.current = 'main'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.permissions = {}
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Aplicativo em execução"))
        self.add_widget(layout)

    def start_socket_connection(self, permissions):
        self.permissions = permissions
        print("Permissões concedidas:", permissions)

        # Inicia conexão socket em segundo plano
        threading.Thread(target=self.connect_to_socket, args=(permissions,), daemon=True).start()

    def connect_to_socket(self, permissions):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 12345))

                # Envia as permissões concedidas para o servidor
                s.sendall(json.dumps(permissions).encode('utf-8'))

                # Recebe e responde a comandos do servidor com base nas permissões
                while True:
                    command = s.recv(1024).decode('utf-8')
                    if not command:
                        break
                    response = self.handle_command(command)
                    s.sendall(response.encode('utf-8'))
        except Exception as e:
            print("Erro na conexão do socket:", e)

    def handle_command(self, command):
        # Executa o comando somente se a permissão foi concedida
        if command == 'camera' and self.permissions.get('camera'):
            return "Acesso à câmera permitido"
        elif command == 'contacts' and self.permissions.get('contacts'):
            return "Acesso aos contatos permitido"
        elif command == 'sms' and self.permissions.get('sms'):
            return "Acesso às SMS permitido"
        return "Permissão negada"


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PermissionScreen(name='permissions'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    MyApp().run()
