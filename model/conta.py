from abc import ABC, abstractmethod
from utils.helpers import data_hora_atual_str

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

    def encerrar_conta(self) -> None:
        """
        Encerra a conta, tornando-a inativa.
        """
        self._ativa = False
        self._registrar_operacao("Conta encerrada")

    def _set_estado_da_conta(self, novo_estado: bool) -> None:
        """
        Define o estado de ativação da conta. Obs: A operação não é registrada!

        Args:
            novo_estado (bool): True para conta ativa, False para inativa.
        """
        self._ativa = novo_estado

    def get_saldo(self) -> float:
        """
        Retorna o saldo atual da conta.

        Returns:
            float: Saldo da conta.
        """
        return self._saldo

    def _set_saldo(self, novo_saldo: float) -> None:
        """
        Define o saldo da conta. Obs: A operação não é registrada!

        Args:
            novo_saldo (float): Novo valor de saldo.
        """
        self._saldo = novo_saldo

    def get_historico(self) -> list[str]:
        """
        Retorna o histórico de transações da conta.

        Returns:
            list[str]: Lista de descrições de transações.
        """
        return self._historico.copy()

    def _set_historico(self, novo_historico: list[str]) -> None:
        """
        Substitui o histórico da conta. Obs: A operação não é registrada!

        Args:
            novo_historico (list[str]): Lista de novas descrições de transações.
        """
        self._historico = novo_historico

    def get_numero_conta(self) -> str:
        """
        Retorna o número da conta.

        Returns:
            str: Número da conta.
        """
        return self._numero_conta

    def _registrar_operacao(self, descricao: str) -> None:
        """
        Adiciona um registro da operação no histórico da conta, com data e hora.

        Args:
            descricao (str): Descrição da operação.
        """
        registro = f"[{data_hora_atual_str()}] {descricao}"
        self._historico.append(registro)

    def __str__(self) -> str:
        """
        Retorna uma representação textual da conta.

        Returns:
            str: Representação da conta.
        """
        return f"Conta {self.get_numero_conta()} | Saldo: R$ {self.get_saldo():.2f}"
