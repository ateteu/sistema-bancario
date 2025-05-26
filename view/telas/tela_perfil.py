import flet as ft
from controller.perfil_controller import PerfilController
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo

class TelaPerfil:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        response = PerfilController.obter_dados_perfil(self.cliente.pessoa.get_numero_documento())
        if response["status"] != "sucesso":
            return ft.Text(response["mensagem"])

        dados = response["dados"]

        dados_pessoais = [
            ft.Text(f"Nome: {dados['nome']}"),
            ft.Text(dados["documento_formatado"]),
            ft.Text(f"Email: {dados['email']}"),
            ft.Text(f"Telefone: {dados['telefone']}"),
            ft.Text(f"Endereço: {dados['endereco']}")
        ]

        if dados["data_nascimento"]:
            dados_pessoais.insert(4, ft.Text(f"Data de nascimento: {dados['data_nascimento']}"))

        contas_ativas = [
            ft.Text(
                f"- {conta.__class__.__name__} | Nº {conta.get_numero_conta()} | "
                f"Saldo: R$ {conta.get_saldo():.2f}"
            )
            for conta in dados["contas"] if conta.get_estado_da_conta()
        ] or [ft.Text("Nenhuma conta ativa encontrada.", italic=True)]

        return ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=500,
                spacing=20,
                controls=[
                    ft.Text("Informações do Cliente", size=22, weight=ft.FontWeight.BOLD),
                    CartaoResumo("Dados pessoais", dados_pessoais),
                    CartaoResumo("Contas ativas", contas_ativas),
                    self.notificador.get_snackbar()
                ]
            )
        )
