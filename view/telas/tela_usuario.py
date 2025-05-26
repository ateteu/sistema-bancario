import flet as ft
from view.telas.tela_perfil import TelaPerfil
from view.telas.tela_pagamento import TelaPagamento
from view.telas.tela_extrato import TelaExtrato


class TelaUsuario:
    def __init__(self, banco, cliente, on_logout, subrota: str = None):
        self.banco = banco
        self.cliente = cliente
        self.on_logout = on_logout
        self.subrota = subrota  # <- salva a rota desejada
        self.conteudo_ref = ft.Ref[ft.Container]()
        self.view = self.criar_view()

    def criar_view(self) -> ft.View:
        view = ft.View(
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

        # ⚡ Executa carregamento após renderização
        def apos_renderizacao(e):
            if self.subrota:
                self.carregar_tela(self.subrota, e)

        view.on_view_pop = apos_renderizacao  # Alternativa: view.on_view_init
        return view

    def criar_sidebar(self) -> ft.Container:
        return ft.Container(
            width=240,
            bgcolor=ft.Colors.GREY_100,
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(self.cliente.pessoa.get_nome(), size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.TextButton("Perfil", icon=ft.Icons.PERSON, on_click=lambda e: self.carregar_tela("perfil", e)),
                    ft.TextButton("Pagamentos", icon=ft.Icons.PAYMENTS, on_click=lambda e: self.carregar_tela("pagamento", e)),
                    ft.TextButton("Extrato", icon=ft.Icons.RECEIPT_LONG, on_click=lambda e: self.carregar_tela("extrato", e)),
                    ft.TextButton("Sair", icon=ft.Icons.LOGOUT, on_click=self.on_logout),
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

        if e and e.page:
            e.page.update()