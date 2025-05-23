from model.conta import Conta
from utils.constantes import (
    TAXA_MANUTENCAO_CCORRENTE
)

class ContaCorrente(Conta):
    """
    Representa uma conta corrente com transferência ilimitada,
    sem rendimento mensal e com taxa de manutenção mensal.
    """

    def transferir(self, destino: 'Conta', valor: float) -> bool:
        """
        Transfere um valor para outra conta sem limite de valor.

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.

        Returns:
            bool: True se a transferência foi realizada com sucesso.
        
        Raises:
            ValueError: Se o saldo atualizado for inválido ao tentar ser definido.
        """
        
        if not self._ativa or not destino._ativa or valor <= 0 or valor > self._saldo:
            return False

        self._set_saldo(self.get_saldo() - valor)
        destino._set_saldo(destino.get_saldo() + valor)

        self._registrar_operacao(f'Transferência de R$ {valor:.2f} para conta {destino.get_numero_conta()}')
        destino._registrar_operacao(f'Recebido R$ {valor:.2f} da conta {self.get_numero_conta()}')
        return True

    def atualizacao_mensal(self) -> None:
        """
        Aplica a atualização mensal da conta corrente, cobrando uma taxa de manutenção fixa.

        A taxa é subtraída do saldo atual e o novo saldo é atualizado. A operação é registrada no histórico da conta.

        Raises:
            ValueError: Se o novo saldo calculado for inválido ao tentar ser definido.
        """
        saldo_atual = self.get_saldo()
        novo_saldo = saldo_atual - TAXA_MANUTENCAO_CCORRENTE
        self._set_saldo(novo_saldo)
        self._registrar_operacao(f"Atualização mensal: taxa de manutenção de R$ {TAXA_MANUTENCAO_CCORRENTE:.2f} cobrada")
