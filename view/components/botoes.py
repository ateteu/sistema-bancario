import flet as ft


class BotaoPrimario(ft.ElevatedButton):
    """Botão com estilo primário padrão do sistema."""

    def __init__(self, texto: str, on_click: callable):
        super().__init__(
            text=texto,
            on_click=on_click,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )


class BotaoSecundario(ft.TextButton):
    """Botão secundário (texto apenas), usado para navegação."""

    def __init__(self, texto: str, on_click: callable):
        super().__init__(
            text=texto,
            on_click=on_click,
            style=ft.ButtonStyle(color=ft.Colors.BLUE_800)
        )