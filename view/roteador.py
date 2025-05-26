import flet as ft
from view.telas.tela_login import TelaLogin
from view.telas.tela_cadastro import TelaCadastro
from view.telas.tela_usuario import TelaUsuario
from dao.cliente_dao import ClienteDAO


def navegar(page: ft.Page, route: str):
    page.views.clear()

    if route == "/login":
        tela_login = TelaLogin(
            on_login_sucesso=lambda usuario_id: page.go(f"/painel/{usuario_id}/perfil"),
            on_ir_cadastro=lambda: page.go("/cadastro")
        )
        page.views.append(
            ft.View("/login", controls=[tela_login.criar_view(page)])
        )

    elif route == "/cadastro":
        tela_cadastro = TelaCadastro(
            on_cadastro_sucesso=lambda: page.go("/login"),
            on_voltar_login=lambda: page.go("/login")
        )
        page.views.append(
            ft.View("/cadastro", controls=[tela_cadastro.view])
        )

    elif route.startswith("/painel/"):
        partes = route.split("/")
        if len(partes) < 3:
            page.go("/login")
            return

        usuario_id = partes[2]
        subrota = partes[3] if len(partes) > 3 else "perfil"

        cliente = ClienteDAO().buscar_por_id(usuario_id)
        if not cliente:
            page.go("/login")
            return

        tela_usuario = TelaUsuario(
            banco=None,
            cliente=cliente,
            on_logout=lambda: page.go("/login"),
            subrota=subrota
        )

        page.views.append(
            ft.View(route, controls=[tela_usuario.view])
        )

    else:
        page.go("/login")

    page.update()