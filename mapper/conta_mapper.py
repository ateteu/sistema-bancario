from model.conta import Conta
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class ContaMapper:
    """
    Classe responsável por mapear objetos Conta e suas subclasses para e a partir de dicionários.

    Métodos:
    - from_dict: Cria uma instância de Conta (Corrente ou Poupança) a partir de um dicionário.
    - to_dict: Converte uma instância de Conta em um dicionário para salvar no JSON.
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
            ValueError: Se campos obrigatórios estiverem ausentes ou tipo inválido.
        """
        campos_obrigatorios = ["tipo", "numero", "saldo", "historico", "ativa"]
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados]
        if campos_faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(campos_faltantes)}")

        tipo      = dados["tipo"]
        numero    = int(dados["numero"])       # ✅ Conversão segura
        saldo     = float(dados["saldo"])      # ✅ Garante tipo correto
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
            dict: Dicionário com os dados da conta para serialização.
        """
        tipo = TIPO_CCORRENTE if isinstance(conta, ContaCorrente) else TIPO_CPOUPANCA
        print(">>> Serializando conta:", conta.get_numero_conta(), "| tipo:", tipo)

        return {
            "numero"    : str(conta.get_numero_conta()),   # ✅ Serializado como string
            "saldo"     : conta.get_saldo(),
            "historico" : conta.get_historico(),
            "ativa"     : conta.get_estado_da_conta(),
            "tipo"      : tipo
        }
