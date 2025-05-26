import flet as ft
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo


class TelaPerfil:
    """
    Tela de exibição do perfil do cliente logado.
    Mostra os dados cadastrais da pessoa e as contas bancárias ativas.
    """

    def __init__(self, cliente):
        """
        Inicializa a tela com base no cliente fornecido.

        Args:
            cliente: Instância de Cliente (PessoaFisica ou PessoaJuridica).
        """
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        """
        Constrói e retorna a estrutura visual da tela.

        Returns:
            ft.Container: Layout da tela de perfil.
        """
        titulo = ft.Text("Informações do Cliente", size=22, weight=ft.FontWeight.BOLD)

        pessoa = self.cliente.pessoa

        dados_pessoais = [
            ft.Text(f"Nome: {pessoa.get_nome()}"),
            ft.Text(f"CPF/CNPJ: {pessoa.get_numero_documento()}"),
            ft.Text(f"Email: {pessoa.get_email()}"),
            ft.Text(f"Telefone: {pessoa.get_telefone()}"),
            ft.Text(f"Endereço: {pessoa.get_endereco()}")
        ]

        # Adiciona data de nascimento apenas se for Pessoa Física
        if hasattr(pessoa, "get_data_nascimento"):
            dados_pessoais.insert(4, ft.Text(
                f"Data de nascimento: {pessoa.get_data_nascimento().strftime('%d/%m/%Y')}")
            )

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