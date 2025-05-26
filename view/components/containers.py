import flet as ft


class CartaoResumo(ft.Container):
    """
    Cartão visual para exibir informações agrupadas como título e conteúdo.

    Usado para agrupar dados como saldo, extrato, perfil, etc.
    """

    def __init__(self, titulo: str, conteudo: list[ft.Control], cor_fundo: str = ft.Colors.WHITE):
        """
        Inicializa um cartão com título e conteúdo disposto verticalmente.

        Args:
            titulo (str): Título em destaque no topo do cartão.
            conteudo (list[ft.Control]): Lista de elementos visuais (ex: Text, Row...).
            cor_fundo (str): Cor de fundo do cartão. Branco por padrão.
        """
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
    """
    Linha horizontal discreta para dividir seções visuais.

    É fina e em tom cinza claro, ideal para interfaces suaves.
    """
    def __init__(self):
        super().__init__(height=1, thickness=1, color=ft.Colors.GREY_300)


class CartaoTransacao(ft.Container):
    """
    Cartão visual para exibir uma transação bancária no extrato.

    A cor de fundo muda conforme o tipo de operação detectado no texto.
    """

    def __init__(self, texto: str):
        """
        Inicializa o cartão com a descrição da transação e cor de fundo automática.

        Args:
            texto (str): Descrição da transação (ex: "Transferência recebida de João").
        """
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
        """
        Retorna a cor de fundo baseada no conteúdo textual da transação.

        Args:
            texto (str): Texto da transação.

        Returns:
            str: Cor sugerida (ex: verde claro para entrada, vermelho para saída).
        """
        texto = texto.lower()
        if "recebida" in texto or "recebido" in texto or "entrada" in texto:
            return ft.Colors.GREEN_100
        if "enviada" in texto or "saída" in texto or "enviado" in texto:
            return ft.Colors.RED_100
        return ft.Colors.GREY_100
