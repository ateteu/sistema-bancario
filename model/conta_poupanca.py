from model.conta import Conta
from utils.constantes import (
    LIMITE_TRANSFERENCIA_CPOUPANCA,
    RENDIMENTO_MENSAL_CPOUPANCA
)

class ContaPoupanca(Conta):
    """
    Representa uma conta poupança com limite de transferência
    e aplicação de rendimento mensal.
    """

    def transferir(self, destino: 'Conta', valor: float) -> bool:
        """
        Transfere um valor para outra conta, respeitando o limite de transferência.

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.

        Returns:
            bool: True se a transferência foi realizada com sucesso.
        """

        # Não permite transações acima do limite
        if (not self._ativa or not destino._ativa or
                valor <= 0 or valor > self._saldo or valor > self.LIMITE_TRANSFERENCIA_CPOUPANCA):
            return False

        self._saldo -= valor
        destino._saldo += valor

        self._registrar_operacao(f'Transferência de R$ {valor:.2f} para conta {destino.get_numero()}')
        destino._registrar_operacao(f'Recebido R$ {valor:.2f} da conta {self.get_numero()}')
        return True

    def atualizacao_mensal(self) -> None:
        """
        Aplica rendimento mensal sobre o saldo da conta poupança.
        """
        rendimento = self._saldo * self.RENDIMENTO_MENSAL_CPOUPANCA
        self._saldo += rendimento
        self._registrar_operacao(f"Atualização mensal: rendimento de R$ {rendimento:.2f} aplicado")
