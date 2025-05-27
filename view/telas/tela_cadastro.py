import flet as ft
import asyncio
from asyncio import sleep
from threading import Thread
from time import sleep as sleep_sync

from controller.cadastro_controller import CadastroController
from view.components.campos import (
    CampoNome, CampoCPF, CampoCNPJ, CampoTelefone, CampoEmail,
    CampoSenha, CampoCEP, CampoTextoPadrao, CampoDataNascimento
)
from view.components.botoes import BotaoPrimario, BotaoSecundario
from view.components.mensagens import Notificador
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaCadastro:
    def __init__(self, on_cadastro_sucesso=None, on_voltar_login=None):
        self.on_cadastro_sucesso = on_cadastro_sucesso
        self.on_voltar_login = on_voltar_login
        self.notificador = Notificador()

        self.tipo_pessoa_ref = ft.Ref[ft.RadioGroup]()
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

        Thread(target=self._delayed_init).start()

    def _delayed_init(self):
        sleep_sync(0.05)
        self.atualizar_campos_visiveis(None)

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

        layout = ft.Container(
            width=500,
            padding=30,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
            content=ft.Column(
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.APP_REGISTRATION, size=30, color=CORES["primaria"]),
                        ft.Text("Cadastro de Cliente", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text("Tipo de pessoa", style=ESTILOS_TEXTO["subtitulo"]),
                    grupo_tipo_pessoa,

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
                        BotaoPrimario("Cadastrar", lambda e: e.page.run_task(self.on_cadastrar_click, e)),
                        BotaoSecundario("Voltar", lambda e: self.on_voltar_login() if self.on_voltar_login else None)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    self.notificador.get_snackbar()
                ]
            )
        )

        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=CORES["secundaria"],
            content=layout
        )

    def atualizar_campos_visiveis(self, e):
        tipo = self.tipo_pessoa_ref.current.value if self.tipo_pessoa_ref.current else "fisica"

        self.nome.value = ""
        self.campo_documento.value = ""
        self.telefone.value = ""
        self.email.value = ""
        self.senha.value = ""
        self.cep.value = ""
        self.numero_endereco.value = ""
        self.nascimento.value = ""
        self.nome_fantasia.value = ""

        if tipo == "fisica":
            self.nome.atualizar_para_pessoa_fisica()
            self.campo_documento = CampoCPF()
            self.nascimento = CampoDataNascimento()
            self.campos_dinamicos.controls.clear()
            self.campos_dinamicos.controls.append(self.nascimento)
        else:
            self.nome.atualizar_para_empresa()
            self.campo_documento = CampoCNPJ()
            self.campos_dinamicos.controls.clear()
            self.campos_dinamicos.controls.append(self.nome_fantasia)
            self.campos_dinamicos.controls.append(
                ft.Text("(Opcional)", size=12, italic=True, color=CORES["texto"])
            )

        self.documento_container.current.content = self.campo_documento
        self.documento_container.current.update()
        self.campos_dinamicos.update()

        if e and hasattr(e.page, "update"):
            e.page.update()

    def coletar_dados(self) -> dict:
        tipo = self.tipo_pessoa_ref.current.value
        dados = {
            "tipo": tipo,
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

        resultado = await asyncio.to_thread(CadastroController.cadastrar_cliente, dados)

        if resultado["status"] == "sucesso":
            self.notificador.sucesso(page, resultado["mensagem"])
            page.update()
            await sleep(1.0)
            if self.on_cadastro_sucesso:
                self.on_cadastro_sucesso()
        else:
            self.notificador.erro(page, resultado["mensagem"])
            page.update()
