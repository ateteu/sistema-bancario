from utils.constantes import TAMANHO_MIN_NUMERO_CONTA

class ValidarConta:
    """
    Classe utilitária responsável pela validação de atributos relacionados a contas bancárias.
    Cada método lança exceções apropriadas em caso de entrada inválida.
    """
    @staticmethod
    def numero_conta(numero_conta: str) -> None:
        """
        Valida o número da conta.

        Verifica se o valor fornecido é uma string composta apenas por dígitos,
        com comprimento mínimo definido por 'TAMANHO_MIN_NUMERO_CONTA'.

        Args:
            numero_conta (str): Número da conta a ser validado.

        Raises:
            TypeError: Se o número da conta não for uma string.
            ValueError: Se o número da conta estiver vazio.
            ValueError: Se o número da conta contiver caracteres não numéricos.
            ValueError: Se o número da conta for menor que o comprimento mínimo exigido.
        """
        if not isinstance(numero_conta, str):
            raise TypeError("Número da conta deve ser uma string.")
        if numero_conta == "":
            raise ValueError("Número da conta não pode ser vazio.")
        if not numero_conta.isdigit():
            raise ValueError("Número da conta deve conter apenas dígitos.")
        if len(numero_conta) < TAMANHO_MIN_NUMERO_CONTA:
            raise ValueError("Número da conta muito curto.")

    @staticmethod
    def _verificacoes_basicas_saldo(saldo: float) -> None:
        """
        Verifica se o saldo é um número real válido e finito.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN (não é um número) ou infinito.
        """
        if not isinstance(saldo, (int, float)):
            raise TypeError("O saldo deve ser um número.")
        if not (saldo == saldo and saldo != float("inf") and saldo != float("-inf")):
            raise ValueError("O saldo não pode ser NaN ou infinito.")

    @staticmethod
    def saldo_positivo_ou_zero(saldo: float) -> None:
        """
        Valida que o saldo é numérico, finito e não-negativo.

        Essa validação é usada em operações que não permitem saldo negativo,
        como transferências bancárias.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
            ValueError: Se o saldo for negativo.
        """
        ValidarConta._verificacoes_basicas_saldo(saldo)
        if saldo < 0:
            raise ValueError("O saldo não pode ser negativo.")

    @staticmethod
    def saldo_livre(saldo: float) -> None:
        """
        Valida que o saldo é numérico e finito, permitindo valores negativos.

        Essa validação é usada em situações onde saldos negativos são aceitáveis,
        como atualizações mensais de cobrança.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
        """
        ValidarConta._verificacoes_basicas_saldo(saldo)

    @staticmethod
    def historico(historico: list) -> None:
        """
        Valida se o histórico da conta é uma lista de strings.

        Args:
            historico (list): Lista que representa o histórico a ser validado.

        Raises:
            TypeError: Se o histórico não for uma lista.
            TypeError: Se algum item da lista não for uma string.
        """
        if not isinstance(historico, list):
            raise TypeError("Histórico da conta deve ser uma lista.")
        for item in historico:
            if not isinstance(item, str):
                raise TypeError("Cada item do histórico da conta deve ser uma string.")

    @staticmethod
    def estado_da_conta(estado: bool) -> None:
        """
        Valida se o estado da conta é um valor booleano.

        Args:
            estado (bool): Valor booleano que representa o estado da conta.

        Raises:
            TypeError: Se o estado informado não for do tipo booleano.
        """
        if not isinstance(estado, bool):
            raise TypeError("O estado da conta deve ser um valor booleano.")
