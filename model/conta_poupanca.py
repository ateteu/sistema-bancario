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

    @property
    def limite_transferencia(self) -> float:
        return LIMITE_TRANSFERENCIA_CPOUPANCA

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
