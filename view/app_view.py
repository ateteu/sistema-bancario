import flet as ft
from view.roteador import navegar


def main(page: ft.Page):
    """
    Função principal da aplicação.

    Configura o tema, tamanho da janela e ativa o roteador de navegação.
    """
    # Configurações visuais e da janela
    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 1000
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # Define a função de navegação para mudanças de rota
    page.on_route_change = lambda e: navegar(page, page.route)

    # Rota inicial
    page.go("/login")


# Inicia a aplicação
if __name__ == "__main__":
    ft.app(target=main)
