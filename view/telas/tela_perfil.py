import flet as ft
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo

class TelaPerfil:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        pessoa = self.cliente.pessoa

        # 🧪 DEBUG: imprime contas carregadas
        print("🧪 DEBUG → Contas carregadas na TelaPerfil:")
        for conta in self.cliente.contas:
            print(
                f"   - Tipo: {conta.__class__.__name__} | Nº: {conta.get_numero_conta()} | "
                f"Saldo: {conta.get_saldo():.2f} | Ativa: {conta.get_estado_da_conta()}"
            )

        dados = {
            "nome": pessoa.get_nome(),
            "documento_formatado": pessoa.get_numero_documento(),
            "email": pessoa.get_email(),
            "telefone": pessoa.get_telefone(),
            "endereco": pessoa.get_endereco(),
            "data_nascimento": (
                pessoa.get_data_nascimento().strftime("%d/%m/%Y")
                if hasattr(pessoa, "get_data_nascimento") and pessoa.get_data_nascimento()
                else None
            ),
            "contas": self.cliente.contas
        }

        # ✅ Define os textos de dados pessoais
        dados_pessoais = [
            ft.Text(f"Nome: {dados['nome']}"),
            ft.Text(f"Documento: {dados['documento_formatado']}"),
            ft.Text(f"Email: {dados['email']}"),
            ft.Text(f"Telefone: {dados['telefone']}"),
            ft.Text(f"Endereço: {dados['endereco']}")
        ]

        if dados["data_nascimento"]:
            dados_pessoais.insert(4, ft.Text(f"Data de nascimento: {dados['data_nascimento']}"))

        # ✅ Lista contas ativas (ou mensagem padrão)
        contas_ativas = [
            ft.Text(
                f"- {conta.__class__.__name__} | Nº {conta.get_numero_conta()} | "
                f"Saldo: R$ {conta.get_saldo():.2f}"
            )
            for conta in dados["contas"] if conta.get_estado_da_conta()
        ] or [ft.Text("Nenhuma conta ativa encontrada.", italic=True)]

        # ✅ Retorna a interface completa
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
