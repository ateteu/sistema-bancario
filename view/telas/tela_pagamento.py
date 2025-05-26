import flet as ft
from view.components.campos import CampoCPF, CampoValor, CampoTextoPadrao
from view.components.botoes import BotaoPrimario
from view.components.mensagens import Notificador
from controller.pagamento_controller import PagamentoController
from controller.conta_controller import ContaController


class TelaPagamento:
    """
    Tela de transferência de valores entre contas de clientes.

    Permite selecionar uma conta de origem e informar os dados do destinatário.
    """

    def __init__(self, banco, cliente):
        """
        Inicializa a tela com base no cliente logado e banco (opcional).

        Args:
            banco: Objeto do banco (não utilizado diretamente).
            cliente: Cliente logado, contendo contas disponíveis.
        """
        self.banco = banco
        self.cliente = cliente
        self.notificador = Notificador()

        self.conta_ref = ft.Ref[ft.Dropdown]()
        self.campo_cpf = CampoCPF()
        self.campo_valor = CampoValor()
        self.campo_desc = CampoTextoPadrao(label="Descrição", hint="Opcional", icon="description")
        self.saldo_text = ft.Text("")

        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        """
        Cria e retorna a interface da tela de pagamento.

        Returns:
            ft.Container: Container com layout da tela.
        """
        opcoes_contas = [
            ft.dropdown.Option(str(conta.get_numero_conta()))
            for conta in self.cliente.contas if conta.get_estado_da_conta()
        ]

        dropdown_conta = ft.Dropdown(
            label="Conta de origem",
            ref=self.conta_ref,
            options=opcoes_contas,
            width=300,
            on_change=self.atualizar_saldo
        )

        return ft.Container(
            alignment=ft.alignment.top_center,
            padding=30,
            expand=True,
            content=ft.Column(
                width=450,
                spacing=20,
                controls=[
                    ft.Text("Transferência entre contas", size=22, weight=ft.FontWeight.BOLD),
                    dropdown_conta,
                    self.saldo_text,
                    self.campo_cpf,
                    self.campo_valor,
                    self.campo_desc,
                    BotaoPrimario("Confirmar pagamento", self.realizar_pagamento),
                    self.notificador.get_snackbar()
                ]
            )
        )

    def atualizar_saldo(self, e):
        """
        Atualiza o texto de saldo disponível da conta selecionada.

        Args:
            e: Evento disparado ao trocar de conta.
        """
        numero = self.conta_ref.current.value

        if not numero:
            self.saldo_text.value = ""
            e.page.update()
            return

        resultado, erro = ContaController.obter_extrato(numero)

        if erro:
            self.saldo_text.value = "Erro ao carregar saldo."
        else:
            saldo, _ = resultado
            self.saldo_text.value = f"Saldo disponível: R$ {saldo:.2f}"

        e.page.update()

    def realizar_pagamento(self, e):
        """
        Realiza a transferência com os dados preenchidos.

        Args:
            e: Evento disparado ao clicar no botão de confirmação.
        """
        page = e.page
        conta_origem_num = self.conta_ref.current.value

        if not conta_origem_num:
            self.notificador.erro(page, "Selecione uma conta de origem.")
            return

        if not self.campo_cpf.validar() or not self.campo_valor.validar():
            return

        dados = {
            "cpf_destino": self.campo_cpf.value,
            "valor": self.campo_valor.get_valor(),
            "descricao": self.campo_desc.value,
            "conta_origem": int(conta_origem_num)
        }

        resultado = PagamentoController.realizar_pagamento(dados, self.banco)

        if resultado["sucesso"]:
            self.notificador.sucesso(page, resultado["mensagem"])
            self.atualizar_saldo(e)
        else:
            self.notificador.erro(page, "\n".join(resultado["erros"]))

        page.update()
