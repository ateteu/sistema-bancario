from model.conta import Conta
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA, NUMERO_CONTA_PARA_ERRO

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
            ValueError: Se um ou mais campos obrigatórios estiverem ausentes.
            ValueError: Se o 'tipo' da conta (salvo no BD) for desconhecido.
        """
        campos_obrigatorios = ["tipo", "numero", "saldo", "historico", "ativa"]

        # Verifica todos campos faltantes no Banco de dados
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados]
        if campos_faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(campos_faltantes)}")

        tipo      = dados["tipo"]
        numero    = dados["numero"]
        saldo     = dados["saldo"]
        historico = dados["historico"]
        ativa     = dados["ativa"]

        if tipo == TIPO_CCORRENTE:
            return ContaCorrente(numero, saldo, historico, ativa)
        elif tipo == TIPO_CPOUPANCA:
            return ContaPoupanca(numero, saldo, historico, ativa)
        else:
            raise ValueError(f"Tipo de conta desconhecido: {tipo}")

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
            "ativa"     : conta.get_estado_da_conta(),
            "tipo"      : TIPO_CCORRENTE if isinstance(conta, ContaCorrente) else TIPO_CPOUPANCA
        }
