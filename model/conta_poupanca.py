from model.conta import Conta
from model.exceptions import ContaInativaError
from utils.constantes import (
    LIMITE_TRANSFERENCIA_CPOUPANCA,
    RENDIMENTO_MENSAL_CPOUPANCA
)

class ContaPoupanca(Conta):
    """
    Representa uma conta poupança com limite de transferência
    e aplicação de rendimento mensal.

    Herda atributos e métodos padrão de Conta.
    """

    def transferir(self, destino: 'Conta', valor: float) -> None:
        """
        Transfere um valor para outra conta, respeitando o limite de transferência.

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.

        Returns:
            bool: True se a transferência foi realizada com sucesso.
        
        Raises:
            ContaInativaError: Se a conta de origem ou destino estiver inativa.
            ValueError: Se o valor for inválido, exceder o saldo ou o limite permitido.
        """
        if not self._ativa:
            raise ContaInativaError(self.get_numero_conta())
        if not destino._ativa:
            raise ContaInativaError(destino.get_numero_conta())
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para a transferência.")
        if valor > LIMITE_TRANSFERENCIA_CPOUPANCA:
            raise ValueError(f"O valor da transferência excede o limite permitido de R$ {LIMITE_TRANSFERENCIA_CPOUPANCA:.2f}.")
        
        self._set_saldo(self.get_saldo() - valor)
        destino._set_saldo(destino.get_saldo() + valor)

        self._registrar_operacao(f'Transferência de R$ {valor:.2f} para conta {destino.get_numero_conta()}')
        destino._registrar_operacao(f'Recebido R$ {valor:.2f} da conta {self.get_numero_conta()}')

    def atualizacao_mensal(self) -> None:
        """
        Aplica o rendimento mensal ao saldo da conta e registra a operação no histórico.

        O rendimento é calculado multiplicando o saldo atual pela constante RENDIMENTO_MENSAL_CPOUPANCA,
        e o saldo é atualizado com esse valor.

        Raises:
            ContaInativaError: Se a conta estiver inativa.
            ValueError: Se o saldo atualizado for inválido ao tentar ser definido.
        """
        conta_ativa = self.get_estado_da_conta()
        if not conta_ativa:
            raise ContaInativaError(self.get_numero_conta())
        
        saldo_atual = self.get_saldo()
        rendimento = saldo_atual * RENDIMENTO_MENSAL_CPOUPANCA
        novo_saldo = saldo_atual + rendimento
        self._set_saldo(novo_saldo)
        self._registrar_operacao(f"Atualização mensal: rendimento de R$ {rendimento:.2f} aplicado.")
