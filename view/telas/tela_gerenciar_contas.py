# arquivo: view/telas/tela_gerenciar_contas.py

import flet as ft
from controller.conta_controller import ContaController
from view.components.mensagens import Notificador


class TelaGerenciarContas:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()

        self.conta_dropdown = ft.Ref[ft.Dropdown]()
        self.senha_field = ft.Ref[ft.TextField]()
        self.dropdown_control = None
        self.container = None

        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        self.dropdown_control = ft.Dropdown(
            ref=self.conta_dropdown,
            label="Selecione uma conta",
            width=400,
        )

        self.container = ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=500,
                spacing=20,
                controls=[
                    ft.Text("Gerenciar Contas", size=22, weight=ft.FontWeight.BOLD),
                    self.dropdown_control,
                    ft.TextField(ref=self.senha_field, label="Confirme sua senha", password=True),
                    ft.Row([
                        ft.ElevatedButton("Encerrar conta", on_click=self.encerrar_conta)
                    ]),
                    self.notificador.get_snackbar()
                ]
            )
        )

        # ✅ Atualiza lista automaticamente quando a tela for exibida
        self.container.on_view_init = lambda e: self.recarregar_lista_contas()

        return self.container

    def recarregar_lista_contas(self):
        contas = ContaController.listar_contas(self.cliente.numero_documento)

        if not contas:
            self.dropdown_control.options = []
            self.dropdown_control.label = "Nenhuma conta encontrada"
            return

        opcoes = [
            ft.dropdown.Option(
                key=str(conta.get_numero_conta()),
                text=f"{conta.__class__.__name__} - Nº {conta.get_numero_conta()} - "
                     f"{'Ativa' if conta.get_estado_da_conta() else 'Inativa'}"
            )
            for conta in contas if conta.get_estado_da_conta()
        ]

        self.dropdown_control.options = opcoes
        self.conta_dropdown.current.value = None

        if self.senha_field.current:
            self.senha_field.current.value = ""

    def atualizar_tela(self, e):
        self.recarregar_lista_contas()
        self.notificador.sucesso(e.page, "Lista atualizada com sucesso.")
        e.page.update()

    def encerrar_conta(self, e):
        numero = self.conta_dropdown.current.value
        senha = self.senha_field.current.value

        if not numero or not senha:
            self.notificador.erro(e.page, "Selecione uma conta ativa e digite a senha.")
            return

        resultado = ContaController.excluir_conta(
            self.cliente.numero_documento,
            numero,
            senha
        )

        if resultado["sucesso"]:
            self.notificador.sucesso(e.page, resultado["mensagem"])
            self.recarregar_lista_contas()
        else:
            self.notificador.erro(e.page, resultado["mensagem"])

        if self.senha_field.current:
            self.senha_field.current.value = ""

        e.page.update()
