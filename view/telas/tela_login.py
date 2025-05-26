import flet as ft
from view.components.campos import CampoCPF, CampoCNPJ, CampoSenha
from view.components.botoes import BotaoPrimario, BotaoSecundario
from view.components.mensagens import Notificador
from controller.auth_controller import AuthController


class TelaLogin:
    def __init__(self, on_login_sucesso=None, on_ir_cadastro=None):
        self.on_login_sucesso = on_login_sucesso
        self.on_ir_cadastro = on_ir_cadastro
        self.notificador = Notificador()

        self.tipo_ref = ft.Ref[ft.RadioGroup]()
        self.documento_container = ft.Ref[ft.Container]()

        self.campo_documento = CampoCPF()  # começa como CPF
        self.campo_senha = CampoSenha()

    def criar_view(self, page: ft.Page) -> ft.Container:
        grupo_tipo = ft.RadioGroup(
            ref=self.tipo_ref,
            value="cpf",
            on_change=self.trocar_campo_documento,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(label="CPF", value="cpf"),
                    ft.Radio(label="CNPJ", value="cnpj"),
                ]
            )
        )

        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                width=400,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Acesso ao sistema bancário", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text("Tipo de documento", size=14),
                    grupo_tipo,
                    ft.Container(ref=self.documento_container, content=self.campo_documento),
                    self.campo_senha,
                    BotaoPrimario("Entrar", on_click=self.on_login_click),
                    BotaoSecundario("Criar conta", on_click=lambda e: self.on_ir_cadastro()),
                    self.notificador.get_snackbar()
                ]
            )
        )

    def trocar_campo_documento(self, e):
        tipo = self.tipo_ref.current.value
        self.campo_documento = CampoCPF() if tipo == "cpf" else CampoCNPJ()
        self.documento_container.current.content = self.campo_documento
        e.page.update()

    def mostrar_erro(self, page: ft.Page, mensagem: str):
        self.notificador.erro(page, mensagem)

    def on_login_click(self, e):
        page = e.page
        documento = self.campo_documento.value.strip()
        senha = self.campo_senha.value.strip()

        resultado = AuthController.login(documento, senha)

        if resultado["status"] != "sucesso":
            self.mostrar_erro(page, resultado["mensagem"])
            return

        if self.on_login_sucesso:
            self.on_login_sucesso(resultado["usuario_id"])