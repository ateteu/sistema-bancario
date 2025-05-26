import flet as ft
from asyncio import sleep
from controller.cadastro_controller import CadastroController
from view.components.campos import (
    CampoNome, CampoCPF, CampoCNPJ, CampoTelefone, CampoEmail,
    CampoSenha, CampoCEP, CampoTextoPadrao, CampoDataNascimento
)
from view.components.botoes import BotaoPrimario, BotaoSecundario
from view.components.mensagens import Notificador
from controller.conta_controller import ContaController
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class TelaCadastro:
    def __init__(self, on_cadastro_sucesso=None, on_voltar_login=None):
        self.on_cadastro_sucesso = on_cadastro_sucesso
        self.on_voltar_login = on_voltar_login
        self.notificador = Notificador()

        self.tipo_pessoa_ref = ft.Ref[ft.RadioGroup]()
        self.tipo_conta_ref = ft.Ref[ft.RadioGroup]()

        self.nome = CampoNome()
        self.campo_documento = CampoCPF()
        self.documento_container = ft.Ref[ft.Container]()
        self.telefone = CampoTelefone()
        self.email = CampoEmail()
        self.senha = CampoSenha()
        self.cep = CampoCEP()
        self.numero_endereco = CampoTextoPadrao(label="Número", hint="Ex: 123", icon="pin")
        self.nome_fantasia = CampoTextoPadrao(label="Nome Fantasia", hint="Razão comercial", icon="store")
        self.nascimento = CampoDataNascimento()

        self.campos_dinamicos = ft.Column(controls=[])

        self.view = self.criar_view()
        # Não chamar atualizar_campos_visiveis aqui para evitar update antes de renderização

    def criar_view(self) -> ft.Container:
        grupo_tipo_pessoa = ft.RadioGroup(
            ref=self.tipo_pessoa_ref,
            value="fisica",
            on_change=self.atualizar_campos_visiveis,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(label="Pessoa Física", value="fisica"),
                    ft.Radio(label="Pessoa Jurídica", value="juridica")
                ]
            )
        )

        grupo_tipo_conta = ft.RadioGroup(
            ref=self.tipo_conta_ref,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(label="Poupança", value="poupanca"),
                    ft.Radio(label="Corrente", value="corrente")
                ]
            )
        )

        layout = ft.Column(
            width=450,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("Cadastro de Cliente", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Tipo de pessoa", size=14),
                grupo_tipo_pessoa,
                ft.Text("Tipo de conta", size=14),
                grupo_tipo_conta,
                self.nome,
                ft.Container(ref=self.documento_container, content=self.campo_documento),
                self.campos_dinamicos,
                self.telefone,
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(expand=2, content=self.cep),
                        ft.Container(expand=1, content=self.numero_endereco),
                    ]
                ),
                self.email,
                self.senha,
                ft.Row([
                    BotaoPrimario("Cadastrar", self.on_cadastrar_click),
                    BotaoSecundario("Voltar", lambda e: self.on_voltar_login() if self.on_voltar_login else None)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.notificador.get_snackbar()
            ]
        )

        return ft.Container(alignment=ft.alignment.center, expand=True, content=layout)

    def atualizar_campos_visiveis(self, e):
        tipo = self.tipo_pessoa_ref.current.value

        if tipo == "fisica":
            self.nome.atualizar_para_pessoa_fisica()
            self.campo_documento = CampoCPF()
            self.campos_dinamicos.controls = [self.nascimento]
        else:
            self.nome.atualizar_para_empresa()
            self.campo_documento = CampoCNPJ()
            self.campos_dinamicos.controls = [
                self.nome_fantasia,
                ft.Text("(Opcional)", size=12, italic=True, color=ft.Colors.GREY)
            ]

        self.documento_container.current.content = self.campo_documento

        if e:
            e.page.update()


    def coletar_dados(self) -> dict:
        tipo = self.tipo_pessoa_ref.current.value

        dados = {
            "tipo": tipo,
            "tipo_conta": self.tipo_conta_ref.current.value,
            "nome": self.nome.value,
            "numero_documento": self.campo_documento.value,
            "telefone": self.telefone.value,
            "cep": self.cep.value,
            "numero_endereco": self.numero_endereco.value,
            "endereco": f"{self.cep.value}, {self.numero_endereco.value}",
            "email": self.email.value,
            "senha": self.senha.value
        }

        if tipo == "fisica":
            dados["data_nascimento"] = self.nascimento.value
        elif self.nome_fantasia.value.strip():
            dados["nome_fantasia"] = self.nome_fantasia.value.strip()

        return dados
    
    async def on_cadastrar_click(self, e):
        page = e.page
        dados = self.coletar_dados()
        resultado = CadastroController.cadastrar_cliente(dados)

        if resultado["status"] == "sucesso":
            # Criação da conta após cadastro bem-sucedido
            tipo_conta = dados.get("tipo_conta")
            numero_documento = dados.get("numero_documento")

            if tipo_conta:
                resposta = ContaController.criar_conta(numero_documento, tipo_conta)
                print(">>> Criando conta via interface:", resposta)
            else:
                print(">>> Tipo de conta não selecionado.")

            self.notificador.sucesso(page, resultado["mensagem"])
            page.update()
            await sleep(1.5)
            if self.on_cadastro_sucesso:
                self.on_cadastro_sucesso()
        else:
            self.notificador.erro(page, resultado["mensagem"])
            page.update()
