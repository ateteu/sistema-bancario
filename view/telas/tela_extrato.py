import flet as ft
from controller.conta_controller import ContaController
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo, CartaoTransacao


class TelaExtrato:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()

        self.dropdown_ref = ft.Ref[ft.Dropdown]()
        self.saldo_text = ft.Text("")
        self.lista_extrato = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)

        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        opcoes_contas = [
            ft.dropdown.Option(str(conta.get_numero_conta()))
            for conta in self.cliente.contas if conta.get_estado_da_conta()
        ]

        return ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=500,
                spacing=20,
                controls=[
                    ft.Text("Consulta de Extrato", size=22, weight=ft.FontWeight.BOLD),

                    ft.Dropdown(
                        label="Selecione uma conta",
                        ref=self.dropdown_ref,
                        width=300,
                        options=opcoes_contas,
                        on_change=self.atualizar_extrato,
                    ),

                    CartaoResumo(
                        titulo="Saldo atual",
                        conteudo=[self.saldo_text]
                    ),

                    CartaoResumo(
                        titulo="Últimas transações",
                        conteudo=[self.lista_extrato]
                    ),

                    self.notificador.get_snackbar()
                ]
            )
        )

    def atualizar_extrato(self, e):
        numero = self.dropdown_ref.current.value

        if not numero:
            self.notificador.erro(e.page, "Selecione uma conta.")
            return

        resultado, erro = ContaController.obter_extrato(numero)

        if erro:
            self.notificador.erro(e.page, erro)
            return

        saldo, historico = resultado
        self.saldo_text.value = f"R$ {saldo:.2f}"

        self.lista_extrato.controls.clear()
        if not historico:
            self.lista_extrato.controls.append(
                ft.Text("Nenhuma transação encontrada.", italic=True)
            )
        else:
            for item in reversed(historico[-10:]):
                self.lista_extrato.controls.append(CartaoTransacao(item))

        e.page.update()