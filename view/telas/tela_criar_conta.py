# arquivo: view/telas/tela_criar_conta.py

import flet as ft
from controller.conta_controller import ContaController
from controller.perfil_controller import PerfilController
from view.components.mensagens import Notificador
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA

class TelaCriarConta:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()
        self.tipo_dropdown = ft.Ref[ft.Dropdown]()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        return ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=400,
                spacing=20,
                controls=[
                    ft.Text("Criar Nova Conta", size=22, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        ref=self.tipo_dropdown,
                        label="Tipo de conta",
                        options=[
                            ft.dropdown.Option(TIPO_CCORRENTE),
                            ft.dropdown.Option(TIPO_CPOUPANCA)
                        ]
                    ),
                    ft.ElevatedButton("Criar conta", on_click=self.criar_conta),
                    self.notificador.get_snackbar()
                ]
            )
        )

    def criar_conta(self, e):
        tipo = self.tipo_dropdown.current.value
        if not tipo:
            self.notificador.erro(e.page, "Selecione um tipo de conta.")
            return

        resultado = ContaController.criar_conta(self.cliente.numero_documento, tipo)
        if resultado["sucesso"]:
            # ✅ Atualiza o cliente com a nova conta salva
            cliente_atualizado = PerfilController.buscar_cliente_por_documento(self.cliente.numero_documento)
            if cliente_atualizado:
                self.cliente = cliente_atualizado
            self.notificador.sucesso(e.page, resultado["mensagem"])
        else:
            self.notificador.erro(e.page, resultado["mensagem"])
