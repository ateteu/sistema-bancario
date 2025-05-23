from model.conta import Conta
from model.exceptions import ContaInativaError
from utils.constantes import (
    TAXA_MANUTENCAO_CCORRENTE
)

class ContaCorrente(Conta):
    """
    Representa uma conta corrente com transferência ilimitada,
    sem rendimento mensal e com taxa de manutenção mensal.

    Herda atributos e métodos padrão de Conta.
    """

    def transferir(self, destino: 'Conta', valor: float) -> None:
        """
        Transfere um valor para outra conta sem limite de valor.

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.

        Returns:
            bool: True se a transferência foi realizada com sucesso.
        
        Raises:
            ContaInativaError: Se esta conta ou a conta de destino estiver inativa.
            ValueError: Se o valor a ser transferido for inválido ou o saldo for insuficiente.
        """
        if not self._ativa:
            raise ContaInativaError(self.get_numero_conta())
        if not destino._ativa:
            raise ContaInativaError(destino.get_numero_conta())
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para a transferência.")

        self._set_saldo(self.get_saldo() - valor)
        destino._set_saldo(destino.get_saldo() + valor)

        self._registrar_operacao(f'Transferência de R$ {valor:.2f} para conta {destino.get_numero_conta()}')
        destino._registrar_operacao(f'Recebido R$ {valor:.2f} da conta {self.get_numero_conta()}')

    def atualizacao_mensal(self) -> None:
        """
        Aplica a atualização mensal da conta corrente, cobrando uma taxa de manutenção fixa.

        A taxa é subtraída do saldo atual e o novo saldo é atualizado. A operação é registrada no histórico da conta.

        Raises:
            ContaInativaError: Se a conta estiver inativa.
            ValueError: Se o novo saldo calculado for inválido ao tentar ser definido.
        """
        conta_ativa = self.get_estado_da_conta()
        if not conta_ativa:
            raise ContaInativaError(self.get_numero_conta())
        
        saldo_atual = self.get_saldo()
        novo_saldo = saldo_atual - TAXA_MANUTENCAO_CCORRENTE
        self._set_saldo(novo_saldo)
        self._registrar_operacao(f"Atualização mensal: taxa de manutenção de R$ {TAXA_MANUTENCAO_CCORRENTE:.2f} cobrada")
