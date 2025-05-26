import flet as ft
from view.telas.tela_perfil import TelaPerfil
from view.telas.tela_pagamento import TelaPagamento
from view.telas.tela_extrato import TelaExtrato


class TelaUsuario:
    """
    Tela principal do cliente após login.

    Permite navegação entre sub-telas: Perfil, Pagamento e Extrato.
    """

    def __init__(self, banco, cliente, on_logout, subrota: str = None):
        """
        Inicializa a tela de painel do usuário.

        Args:
            banco: Objeto do sistema bancário (usado para operações).
            cliente: Objeto Cliente logado.
            on_logout (callable): Função a ser chamada ao clicar em "Sair".
            subrota (str, opcional): Tela inicial a ser exibida ("perfil", "extrato"...).
        """
        self.banco = banco
        self.cliente = cliente
        self.on_logout = on_logout
        self.conteudo_ref = ft.Ref[ft.Container]()
        self.view = self.criar_view()

        if subrota:
            self.carregar_tela(subrota)

    def criar_view(self) -> ft.View:
        """
        Cria a estrutura visual geral da tela (sidebar + conteúdo).

        Returns:
            ft.View: Estrutura da view principal com rota personalizada.
        """
        return ft.View(
            route=f"/painel/{self.cliente.pessoa.get_numero_documento()}",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        self.criar_sidebar(),
                        ft.Container(
                            ref=self.conteudo_ref,
                            expand=True,
                            padding=30,
                            content=ft.Text("Bem-vindo ao sistema bancário", size=20)
                        )
                    ]
                )
            ]
        )

    def criar_sidebar(self) -> ft.Container:
        """
        Cria o menu lateral de navegação com botões de acesso.

        Returns:
            ft.Container: Sidebar com nome e botões de ação.
        """
        return ft.Container(
            width=240,
            bgcolor=ft.Colors.GREY_100,
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(self.cliente.pessoa.get_nome(), size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.TextButton("Perfil", on_click=lambda e: self.carregar_tela("perfil", e)),
                    ft.TextButton("Pagamentos", on_click=lambda e: self.carregar_tela("pagamento", e)),
                    ft.TextButton("Extrato", on_click=lambda e: self.carregar_tela("extrato", e)),
                    ft.TextButton("Sair", on_click=self.on_logout),
                ]
            )
        )

    def carregar_tela(self, rota: str, e=None):
        match rota:
            case "perfil":
                tela = TelaPerfil(self.cliente)
            case "pagamento":
                tela = TelaPagamento(self.banco, self.cliente)
            case "extrato":
                tela = TelaExtrato(self.cliente)
            case _:
                tela = ft.Text("Tela não encontrada.")

        self.conteudo_ref.current.content = tela.view

        # Atualiza a interface
        try:
            (e.page if e else self.view.controls[0].page).update()
        except Exception:
            pass  # ignora caso raro de view ainda não montada

