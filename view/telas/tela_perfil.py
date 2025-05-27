import flet as ft
from controller.perfil_controller import PerfilController
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaPerfil:
    """
    Tela de exibição do perfil do cliente, contendo dados pessoais e contas ativas.
    """

    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        """Gera a interface visual principal da tela de perfil."""
        
        cliente_atualizado = PerfilController.buscar_cliente_por_documento(self.cliente.numero_documento)
        if cliente_atualizado:
            self.cliente = cliente_atualizado

        pessoa = self.cliente.pessoa

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

        def linha_info(icon, texto):
            return ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, size=20, color=CORES["primaria"]),
                    ft.Text(texto, style=ESTILOS_TEXTO["normal"])
                ]
            )

        def linha_multilinha(icon, rotulo, texto):
            return ft.Column([
                ft.Row([
                    ft.Icon(icon, size=20, color=CORES["primaria"]),
                    ft.Text(rotulo, style=ESTILOS_TEXTO["normal"])
                ]),
                ft.Text(texto, style=ESTILOS_TEXTO["normal"], selectable=True, no_wrap=False)
            ])

        dados_pessoais = [
            linha_info(ft.Icons.PERSON, f"Nome: {dados['nome']}"),
            linha_info(ft.Icons.BADGE, f"Documento: {dados['documento_formatado']}"),
            linha_info(ft.Icons.MAIL_OUTLINE, f"Email: {dados['email']}"),
            linha_info(ft.Icons.PHONE, f"Telefone: {dados['telefone']}")
        ]

        if dados["data_nascimento"]:
            dados_pessoais.append(
                linha_info(ft.Icons.CALENDAR_MONTH, f"Data de nascimento: {dados['data_nascimento']}")
            )

        dados_pessoais.append(
            linha_multilinha(ft.Icons.LOCATION_ON_OUTLINED, "Endereço:", dados['endereco'])
        )

        contas_ativas = [
            linha_info(
                ft.Icons.ACCOUNT_BALANCE,
                f"{conta.__class__.__name__} • Nº {conta.get_numero_conta()} • Saldo: R$ {conta.get_saldo():.2f}"
            )
            for conta in dados["contas"] if conta.get_estado_da_conta()
        ] or [
            ft.Text("❌ Nenhuma conta ativa encontrada.", italic=True, style=ESTILOS_TEXTO["normal"])
        ]

        return ft.Container(
            alignment=ft.alignment.top_center,
            padding=30,
            expand=True,
            bgcolor=CORES["secundaria"],
            content=ft.Container(
                width=520,
                padding=25,
                bgcolor=CORES["fundo"],
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Row([
                            ft.Icon(name=ft.Icons.PERSON_OUTLINE, size=28, color=CORES["primaria"]),
                            ft.Text("Informações do Cliente", style=ESTILOS_TEXTO["titulo"])
                        ], alignment=ft.MainAxisAlignment.CENTER),

                        CartaoResumo("Dados pessoais", dados_pessoais),
                        CartaoResumo("Contas ativas", contas_ativas),
                        self.notificador.get_snackbar()
                    ]
                )
            )
        )
