from abc import ABC, abstractmethod

class Conta(ABC):
    """
    Representa uma conta bancária.

    Attributes:
        _numero_conta (str): Número único da conta.
        _saldo (float): Saldo atual da conta.
        _historico (list[str]): Lista de operações realizadas.
        _ativa (bool): Indica se a conta está ativa.
    """

    def __init__(self, numero: str):
        """
        Inicializa uma nova conta com saldo zerado.

        Args:
            numero (str): Número único da conta.
        """
        self._numero_conta = numero
        self._saldo = 0.0
        self._historico = []
        self._ativa = True

    @abstractmethod
    def transferir(self, destino: 'Conta', valor: float) -> bool:
        """
        Transfere um valor para outra conta.

        Este método deve ser implementado pelas subclasses.

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.

        Returns:
            bool: True se a transferência foi realizada com sucesso.
        """
        pass

    @abstractmethod
    def atualizacao_mensal(self) -> None:
        """
        Aplica regras específicas de atualização mensal.

        Este método deve ser implementado pelas subclasses.
        """
        pass

    def encerrar(self) -> None:
        """
        Encerra a conta, tornando-a inativa.
        """
        self._ativa = False
        self._registrar_operacao("Conta encerrada")

    def get_saldo(self) -> float:
        """
        Retorna o saldo atual da conta.

        Returns:
            float: Saldo da conta.
        """
        return self._saldo

    def get_historico(self) -> list[str]:
        """
        Retorna o histórico de transações da conta.

        Returns:
            list[str]: Lista de descrições de transações.
        """
        return self._historico.copy()

    def get_numero_conta(self) -> str:
        """
        Retorna o número da conta.

        Returns:
            str: Número da conta.
        """
        return self._numero_conta

    def _registrar_operacao(self, descricao: str) -> None:
        """
        Registra uma operação no histórico da conta.

        Args:
            descricao (str): Descrição da operação.
        """
        self._historico.append(descricao)

    def __str__(self) -> str:
        """
        Retorna uma representação textual da conta.

        Returns:
            str: Representação da conta.
        """
        return f"Conta {self._numero_conta} | Saldo: R$ {self._saldo:.2f}"
