# arquivo: view/telas/tela_editar_cliente.py

import flet as ft
from view.components.mensagens import Notificador

class TelaEditarCliente:
    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()
        self.email_field = ft.Ref[ft.TextField]()
        self.telefone_field = ft.Ref[ft.TextField]()
        self.senha_atual_field = ft.Ref[ft.TextField]()
        self.nova_senha_field = ft.Ref[ft.TextField]()
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        return ft.Container(
            padding=30,
            alignment=ft.alignment.top_center,
            expand=True,
            content=ft.Column(
                width=450,
                spacing=20,
                controls=[
                    ft.Text("Alterar Dados do Cliente", size=22, weight=ft.FontWeight.BOLD),
                    ft.TextField(ref=self.email_field, label="Email", value=self.cliente.pessoa.get_email()),
                    ft.TextField(ref=self.telefone_field, label="Telefone", value=self.cliente.pessoa.get_telefone()),
                    ft.Divider(),
                    ft.TextField(ref=self.senha_atual_field, label="Senha atual", password=True),
                    ft.TextField(ref=self.nova_senha_field, label="Nova senha", password=True),
                    ft.ElevatedButton("Salvar alterações", on_click=self.salvar_dados),
                    self.notificador.get_snackbar()
                ]
            )
        )

    def salvar_dados(self, e):
        try:
            # Atualiza email e telefone
            self.cliente.pessoa.set_email(self.email_field.current.value)
            self.cliente.pessoa.set_telefone(self.telefone_field.current.value)

            # Atualiza senha (se preenchida)
            senha_atual = self.senha_atual_field.current.value.strip()
            nova_senha = self.nova_senha_field.current.value.strip()

            if senha_atual and nova_senha:
                self.cliente.alterar_senha(senha_atual, nova_senha)

            from dao.cliente_dao import ClienteDAO
            ClienteDAO().atualizar_objeto(self.cliente)

            self.notificador.sucesso(e.page, "Dados atualizados com sucesso!")
        except Exception as err:
            self.notificador.erro(e.page, str(err))