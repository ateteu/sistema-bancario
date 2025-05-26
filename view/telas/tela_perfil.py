import flet as ft
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo


class TelaPerfil:
    def __init__(self, cliente):
        """
        Tela de exibição de informações do perfil do cliente.
        """
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        titulo = ft.Text("Informações do Cliente", size=22, weight=ft.FontWeight.BOLD)

        # Dados pessoais
        dados_pessoais = [
            ft.Text(f"Nome: {self.cliente.get_nome()}"),
            ft.Text(f"CPF/CNPJ: {self.cliente.get_numero_documento()}"),
            ft.Text(f"Email: {self.cliente.get_email()}"),
            ft.Text(f"Telefone: {self.cliente.get_telefone()}"),
            ft.Text(f"Data de nascimento: {self.cliente.get_data_nascimento().strftime('%d/%m/%Y')}"),
            ft.Text(f"Endereço: {self.cliente.get_endereco()}"),
        ]

        # Contas ativas
        contas_ativas = [
            ft.Text(
                f"- {conta.__class__.__name__} | Nº {conta.get_numero_conta()} | "
                f"Saldo: R$ {conta.get_saldo():.2f}"
            )
            for conta in self.cliente.contas if conta.get_estado_da_conta()
        ] or [ft.Text("Nenhuma conta ativa encontrada.", italic=True)]

        return ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=500,
                spacing=20,
                controls=[
                    titulo,
                    CartaoResumo("Dados pessoais", dados_pessoais),
                    CartaoResumo("Contas ativas", contas_ativas),
                    self.notificador.get_snackbar()
                ]
            )
        )