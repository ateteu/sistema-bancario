from model.conta import Conta
from model.exceptions import ContaInativaError
from utils.constantes import (
    TAXA_MANUTENCAO_CCORRENTE
)

class ContaCorrente(Conta):
    """
    Representa uma conta corrente com limite de transferência superior,
    sem rendimento mensal e com taxa de manutenção mensal.

    Herda atributos e métodos padrão de Conta.
    """

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
