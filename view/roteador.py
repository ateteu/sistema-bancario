import flet as ft
from view.telas.tela_login import TelaLogin
from view.telas.tela_cadastro import TelaCadastro
from view.telas.tela_usuario import TelaUsuario
from dao.cliente_dao import ClienteDAO


def navegar(page: ft.Page, route: str):
    """
    Função responsável por gerenciar a navegação entre telas.

    Define qual tela será exibida com base na rota acessada.

    Args:
        page (ft.Page): Página Flet atual.
        route (str): Rota acessada (ex: "/login", "/painel/{id}/extrato").
    """
    page.views.clear()

    # === Tela de login ===
    if route == "/login":
        tela_login = TelaLogin(
            on_login_sucesso=lambda usuario_id: page.go(f"/painel/{usuario_id}/perfil"),
            on_ir_cadastro=lambda: page.go("/cadastro")
        )
        page.views.append(
            ft.View("/login", controls=[tela_login.criar_view(page)])
        )

    # === Tela de cadastro ===
    elif route == "/cadastro":
        tela_cadastro = TelaCadastro(
            on_cadastro_sucesso=lambda: page.go("/login"),
            on_voltar_login=lambda: page.go("/login")
        )

        page.views.append(
            ft.View("/cadastro", controls=[tela_cadastro.view])
        )

        # Executa após renderização da tela
        def _apos_renderizacao(e):
            tela_cadastro.atualizar_campos_visiveis(e)

        page.on_resize = _apos_renderizacao
        page.update()

    # === Painel do usuário ===
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

        page.views.append(tela_usuario.view)


    # === Rota desconhecida: volta para login ===
    else:
        page.go("/login")

    page.update()