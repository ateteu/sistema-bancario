import flet as ft


class CartaoResumo(ft.Container):
    def __init__(self, titulo: str, conteudo: list[ft.Control], cor_fundo: str = ft.Colors.WHITE):
        super().__init__(
            bgcolor=cor_fundo,
            padding=20,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.Colors.GREY_400,
                offset=ft.Offset(2, 2),
            ),
            content=ft.Column(
                controls=[ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD)] + conteudo,
                spacing=8
            )
        )


class LinhaSeparadora(ft.Divider):
    """Linha cinza suave com padding lateral."""
    def __init__(self):
        super().__init__(height=1, thickness=1, color=ft.Colors.GREY_300)

class CartaoTransacao(ft.Container):
    def __init__(self, texto: str):
        super().__init__(
            padding=10,
            bgcolor=self._cor_fundo(texto),
            border_radius=8,
            content=ft.Text(
                value=texto,
                size=14,
                weight=ft.FontWeight.W500,
                color=ft.Colors.BLACK87
            )
        )

    def _cor_fundo(self, texto: str) -> str:
        texto = texto.lower()
        if "recebida" in texto or "recebido" in texto or "entrada" in texto:
            return ft.Colors.GREEN_100
        if "enviada" in texto or "saída" in texto or "enviado" in texto:
            return ft.Colors.RED_100
        return ft.Colors.GREY_100
