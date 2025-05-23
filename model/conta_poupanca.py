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
        
        Raises:
            ValueError: Se o saldo atualizado for inválido ao tentar ser definido.
        """

        # Não permite transações acima do limite
        if (not self._ativa or not destino._ativa or
                valor <= 0 or valor > self._saldo or valor > LIMITE_TRANSFERENCIA_CPOUPANCA):
            return False

        self._set_saldo(self.get_saldo() - valor)
        destino._set_saldo(destino.get_saldo() + valor)

        self._registrar_operacao(f'Transferência de R$ {valor:.2f} para conta {destino.get_numero_conta()}')
        destino._registrar_operacao(f'Recebido R$ {valor:.2f} da conta {self.get_numero_conta()}')
        return True

    def atualizacao_mensal(self) -> None:
        """
        Aplica o rendimento mensal ao saldo da conta e registra a operação no histórico.

        O rendimento é calculado multiplicando o saldo atual pela constante RENDIMENTO_MENSAL_CPOUPANCA,
        e o saldo é atualizado com esse valor.

        Raises:
            ValueError: Se o saldo atualizado for inválido ao tentar ser definido.
        """
        saldo_atual = self.get_saldo()
        rendimento = saldo_atual * RENDIMENTO_MENSAL_CPOUPANCA
        novo_saldo = saldo_atual + rendimento
        self._set_saldo(novo_saldo)
        self._registrar_operacao(f"Atualização mensal: rendimento de R$ {rendimento:.2f} aplicado.")
