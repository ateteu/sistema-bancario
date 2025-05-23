from model.conta import Conta
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA

class ContaMapper:
    """
    Classe responsável por mapear objetos Conta e suas subclasses para e a partir de dicionários.

    Essa classe oferece métodos estáticos para:
    - Criar instâncias de Conta a partir de um dicionário (deserialização).
    - Converter instâncias de Conta em dicionários (serialização).
    """

    @staticmethod
    def from_dict(dados: dict) -> Conta:
        """
        Cria uma instância de Conta a partir de um dicionário.

        Args:
            dados (dict): Dicionário contendo os dados da conta e seu tipo.

        Returns:
            Conta: Instância de ContaCorrente ou ContaPoupanca.
        
        Raises:
            ValueError: Se o valor de algum atributo for inválido (ex: saldo).
            TypeError: Se algum atributo for incompatível (ex: histórico).
        """
        tipo      = dados.get("tipo")
        numero    = dados["numero"]
        saldo     = dados.get("saldo", 0.0)
        historico = dados.get("historico", [])
        ativa     = dados.get("ativa", True)

        # Cria uma instância da subclasse correta
        if tipo == TIPO_CCORRENTE:
            conta = ContaCorrente(numero)
        elif tipo == TIPO_CPOUPANCA:
            conta = ContaPoupanca(numero)
        else:
            raise ValueError(f"Tipo de conta desconhecido: {tipo}")

        # Reconstrói os atributos comuns
        conta._set_saldo(saldo)
        conta._set_historico(historico)
        conta._set_estado_da_conta(ativa)
        return conta

    @staticmethod
    def to_dict(conta: Conta) -> dict:
        """
        Converte uma instância de Conta em dicionário.

        Args:
            conta (Conta): Objeto de uma subclasse de Conta.

        Returns:
            dict: Dicionário com os dados da conta (e o tipo (subclasse) de Conta incluído!).
        """
        return {
            "numero"    : conta.get_numero_conta(),
            "saldo"     : conta.get_saldo(),
            "historico" : conta.get_historico(),
            "ativa"     : conta._ativa,
            "tipo"      : TIPO_CCORRENTE if isinstance(conta, ContaCorrente) else TIPO_CPOUPANCA
        }
