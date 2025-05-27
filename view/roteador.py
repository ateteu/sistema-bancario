# arquivo: view/roteador.py

import flet as ft
from urllib.parse import quote, unquote

from view.telas.tela_login import TelaLogin
from view.telas.tela_cadastro import TelaCadastro
from view.telas.tela_usuario import TelaUsuario
from controller.perfil_controller import PerfilController


def navegar(page: ft.Page, route: str):
    print("[DEBUG] ROTA RECEBIDA:", route)
    page.views.clear()  # Garante que nada antigo seja mantido

    def redirecionar_para_painel(usuario_id):
        rota_segura = f"/painel/{quote(usuario_id, safe='')}/perfil"
        print("[DEBUG] Navegando para:", rota_segura)
        page.go(rota_segura)

    if route == "/login":
        tela_login = TelaLogin(
            on_login_sucesso=redirecionar_para_painel,
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
        view = ft.View("/cadastro", controls=[tela_cadastro.view])
        page.views.append(view)

        def _apos_renderizacao(e):
            tela_cadastro.atualizar_campos_visiveis(e)

        page.on_resize = _apos_renderizacao
        page.update()

    elif route.startswith("/painel/"):
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(route)
        rota_limpa = parsed.path
        query = parse_qs(parsed.query)
        resetar = query.get("resetar", ["false"])[0] == "true"

        partes = rota_limpa.split("/")
        print("[DEBUG] Partes da rota:", partes)
        print("[DEBUG] Resetar?", resetar)

        usuario_id = unquote(partes[2])
        print("[DEBUG] ID decodificado:", usuario_id)

        cliente = PerfilController.buscar_cliente_por_documento(usuario_id)
        print("[DEBUG] Cliente encontrado?", cliente is not None)

        if not cliente:
            print("[ERRO] Cliente não encontrado, redirecionando para login")
            page.go("/login")
            return

        subrota = partes[3] if len(partes) > 3 else "perfil"
        print("[DEBUG] Subrota identificada:", subrota)

        # ✅ Garante nova instância da tela para limpar estado
        nova_tela_usuario = TelaUsuario(
            banco=None,
            cliente=cliente,
            on_logout=lambda e: page.go("/login"),
            subrota=subrota,
            resetar=resetar
        )

        # ✅ Cria View explícita com rota única para não manter cache
        view = ft.View(route, controls=[nova_tela_usuario.view])
        page.views.append(view)

    else:
        print("[ERRO] Rota desconhecida, redirecionando para login")
        page.go("/login")

    page.update()
