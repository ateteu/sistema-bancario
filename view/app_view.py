import flet as ft
from view.roteador import navegar


def main(page: ft.Page):
    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 1000
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # Roteador ativado
    page.on_route_change = lambda e: navegar(page, page.route)

    # Vai direto para /login
    page.go("/login")
