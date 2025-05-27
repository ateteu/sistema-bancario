import flet as ft
from view.components.campos import CampoValor, CampoTextoPadrao, CampoCPF, CampoCNPJ
from view.components.mensagens import Notificador
from controller.pagamento_controller import PagamentoController
from controller.conta_controller import ContaController
from controller.perfil_controller import PerfilController  # ✅ Substituição aqui


class TelaPagamento:
    def __init__(self, banco, cliente):
        self.banco = banco
        self.cliente = cliente
        self.notificador = Notificador()

        self.tipo_chave = ft.Ref[ft.Dropdown]()
        self.conta_destino_ref = ft.Ref[ft.Dropdown]()
        self.campo_doc = CampoCPF()
        self.campo_doc.on_blur = self.buscar_destinatario_automatico
        self.container_chave = ft.Container(content=ft.Column([self.campo_doc]))

        self.dropdown_conta_destino = ft.Dropdown(
            ref=self.conta_destino_ref,
            label="Conta de destino",
            width=300,
            opacity=0,
            disabled=True
        )

        self.campo_valor = CampoValor()
        self.campo_desc = CampoTextoPadrao(label="Descrição", hint="Opcional")
        self.campo_senha = ft.TextField(label="Sua senha", password=True, can_reveal_password=True, width=300)
        self.nome_destinatario_text = ft.Text("", size=14, italic=True)

        self.conta_ref = ft.Ref[ft.Dropdown]()
        self.saldo_text = ft.Text("", size=14, italic=True)
        self.tipo_conta_text = ft.Text("", size=14)
        self.limite_text = ft.Text("", size=14)

        self.destinatario_confirmado = False
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        opcoes_contas = [
            ft.dropdown.Option(num) for num in ContaController.contas_ativas_para_dropdown(self.cliente)
        ]

        dropdown_conta = ft.Dropdown(
            label="Conta de origem",
            ref=self.conta_ref,
            options=opcoes_contas,
            width=300,
            on_change=self.atualizar_saldo
        )

        self.dropdown_tipo = ft.Dropdown(
            ref=self.tipo_chave,
            label="Tipo de chave",
            width=300,
            options=[ft.dropdown.Option("CPF"), ft.dropdown.Option("CNPJ")],
            on_change=self.alternar_campo_chave
        )

        return ft.Container(
            alignment=ft.alignment.top_center,
            padding=30,
            expand=True,
            content=ft.Column(
                width=450,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.PAYMENTS, size=28),
                        ft.Text("Transferência entre contas", size=22, weight=ft.FontWeight.BOLD),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    dropdown_conta,
                    self.saldo_text,
                    self.tipo_conta_text,
                    self.limite_text,
                    self.dropdown_tipo,
                    self.container_chave,
                    self.nome_destinatario_text,
                    self.dropdown_conta_destino,
                    self.campo_valor,
                    self.campo_desc,
                    self.campo_senha,
                    ft.Container(
                        bgcolor=ft.Colors.TRANSPARENT,
                        content=ft.ElevatedButton("Confirmar pagamento", on_click=self.realizar_pagamento)
                    ),
                    self.notificador.get_snackbar()
                ]
            )
        )

    def alternar_campo_chave(self, e):
        tipo = self.tipo_chave.current.value
        self.destinatario_confirmado = False
        self.nome_destinatario_text.value = ""
        self.dropdown_conta_destino.opacity = 0
        self.dropdown_conta_destino.disabled = True
        self.dropdown_conta_destino.options = []

        self.campo_doc = CampoCPF() if tipo == "CPF" else CampoCNPJ()
        self.campo_doc.on_blur = self.buscar_destinatario_automatico
        self.container_chave.content = ft.Column([self.campo_doc])
        self.container_chave.update()
        e.page.update()

    def buscar_destinatario_automatico(self, e):
        doc = self.campo_doc.value.strip()
        self.destinatario_confirmado = False
        self.dropdown_conta_destino.opacity = 0
        self.dropdown_conta_destino.disabled = True
        self.dropdown_conta_destino.options = []

        if not doc:
            self.nome_destinatario_text.value = ""
            e.page.update()
            return

        cliente = PerfilController.buscar_cliente_por_documento(doc)  # ✅ Substituição aqui
        if not cliente:
            self.nome_destinatario_text.value = "❌ Destinatário não encontrado."
        else:
            contas = [c for c in cliente.contas if c.get_estado_da_conta()]
            if not contas:
                self.nome_destinatario_text.value = "❌ Destinatário não possui conta ativa."
            else:
                nome = cliente.pessoa.get_nome()
                self.nome_destinatario_text.value = f"👤 {nome}"
                self.dropdown_conta_destino.options = [
                    ft.dropdown.Option(str(c.get_numero_conta())) for c in contas
                ]
                self.dropdown_conta_destino.opacity = 1
                self.dropdown_conta_destino.disabled = False
                self.destinatario_confirmado = True

        e.page.update()

    def atualizar_saldo(self, e):
        numero = self.conta_ref.current.value
        self.saldo_text.value = ""
        self.tipo_conta_text.value = ""
        self.limite_text.value = ""

        if numero:
            resultado, erro = ContaController.obter_extrato(numero)

            if erro or not isinstance(resultado, tuple) or len(resultado) != 2:
                self.saldo_text.value = "Erro ao carregar saldo."
            else:
                saldo, conta = resultado
                self.saldo_text.value = f"💰 Saldo disponível: R$ {saldo:.2f}"
                self.tipo_conta_text.value = f"Tipo da conta: {conta.__class__.__name__}"
                self.limite_text.value = f"🔒 Limite de transferência: R$ {conta.limite_transferencia:.2f}"

        e.page.update()

    def realizar_pagamento(self, e):
        page = e.page

        try:
            conta_origem = int(self.conta_ref.current.value)
            conta_destino = int(self.conta_destino_ref.current.value)
        except (ValueError, TypeError):
            self.notificador.erro(page, "Erro ao selecionar conta. Tente novamente.")
            return

        doc_destino = self.campo_doc.value.strip()
        senha = self.campo_senha.value.strip()

        if not conta_origem:
            self.notificador.erro(page, "Selecione uma conta de origem.")
            return

        if not doc_destino:
            self.notificador.erro(page, "Informe o CPF ou CNPJ do destinatário.")
            return

        if not self.destinatario_confirmado:
            self.notificador.erro(page, "Confirme o destinatário.")
            return

        if not conta_destino:
            self.notificador.erro(page, "Selecione a conta de destino.")
            return

        if not self.campo_valor.validar():
            return

        if not senha:
            self.notificador.erro(page, "Digite sua senha para confirmar.")
            return

        resultado = PagamentoController.processar_pagamento(
            conta_origem_num=conta_origem,
            doc_destino=doc_destino,
            valor=self.campo_valor.get_valor(),
            descricao=self.campo_desc.value,
            senha=senha,
            conta_destino_numero=conta_destino
        )

        if resultado["sucesso"]:
            self.notificador.sucesso(page, resultado["mensagem"])
            self.atualizar_saldo(e)
            self.campo_senha.value = ""
            self.campo_valor.limpar()
            self.campo_desc.value = ""
            self.destinatario_confirmado = False
            self.nome_destinatario_text.value = ""
            self.campo_doc.value = ""
            self.dropdown_conta_destino.opacity = 0
            self.dropdown_conta_destino.disabled = True
            self.dropdown_conta_destino.options = []
        else:
            self.notificador.erro(page, "\n".join(resultado["erros"]))

        page.update()