# arquivo: view/telas/tela_criar_conta.py

import flet as ft
import uuid
from controller.conta_controller import ContaController
from controller.perfil_controller import PerfilController
from view.components.mensagens import Notificador
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaCriarConta:
    def __init__(self, cliente):
        print("🆕 [TelaCriarConta] nova instância criada")
        self.cliente = cliente
        self.notificador = Notificador()
        self.dropdown_ref = ft.Ref[ft.Dropdown]()  # ✅ ref do Dropdown
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        layout = ft.Container(
            width=420,
            padding=25,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
            content=ft.Column(
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.ACCOUNT_BALANCE, size=28, color=CORES["primaria"]),
                        ft.Text("Criar Nova Conta", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Dropdown(
                        ref=self.dropdown_ref,
                        key=str(uuid.uuid4()),  # ✅ força reset visual
                        label="Tipo de conta",
                        width=300,
                        options=[
                            ft.dropdown.Option("Corrente"),
                            ft.dropdown.Option("Poupança")
                        ]
                    ),

                    ft.ElevatedButton(
                        "Criar conta",
                        on_click=self.criar_conta,
                        bgcolor=CORES["primaria"],
                        color=CORES["icone_sidebar"]
                    ),

                    self.notificador.get_snackbar()
                ]
            )
        )

        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=CORES["secundaria"],
            padding=30,
            content=layout
        )

    def criar_conta(self, e):
        dropdown_opcao = self.dropdown_ref.current
        tipo_exibido = dropdown_opcao.value if dropdown_opcao else None

        print("🔍 Dropdown selecionado:", tipo_exibido)

        if not tipo_exibido:
            self.notificador.erro(e.page, "Selecione um tipo de conta.")
            return

        mapa_tipo = {
            "Corrente": TIPO_CCORRENTE,
            "Poupança": TIPO_CPOUPANCA
        }

        tipo = mapa_tipo.get(tipo_exibido)

        if not tipo:
            self.notificador.erro(e.page, "Tipo de conta inválido.")
            return

        resultado = ContaController.criar_conta(self.cliente.numero_documento, tipo)

        if resultado["sucesso"]:
            cliente_atualizado = PerfilController.buscar_cliente_por_documento(self.cliente.numero_documento)
            if cliente_atualizado:
                self.cliente = cliente_atualizado
            self.notificador.sucesso(e.page, resultado["mensagem"])
        else:
            self.notificador.erro(e.page, resultado["mensagem"])

        # ✅ Reset visual garantido (independente do resultado)
        self.dropdown_ref.current.key = str(uuid.uuid4())
        self.dropdown_ref.current.value = None
        self.dropdown_ref.current.update()
