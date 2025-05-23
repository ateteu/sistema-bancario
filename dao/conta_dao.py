from typing import Optional, List
from model.conta import Conta
from mapper.conta_mapper import ContaMapper
from dao.dao import DAO
from utils.constantes import ( 
    ARQUIVO_CONTAS, 
    TIPO_CCORRENTE, 
    TIPO_CPOUPANCA 
)

class ContaDAO(DAO):
    """
    DAO responsável pela persistência de objetos do tipo Conta
    (ContaCorrente, ContaPoupanca) no arquivo em questão.
    """

    def __init__(self):
        """
        Inicializa o DAO de contas com o caminho do arquivo.
        """
        super().__init__(ARQUIVO_CONTAS)

    def from_dict(self, dados: dict) -> Conta:
        """
        Cria uma instância de Conta a partir de um dicionário, usando o mapper de conta.

        Args:
            dados (dict): Dicionário contendo os dados da conta e seu tipo.

        Returns:
            Conta: Instância de ContaCorrente ou ContaPoupanca.
        
        Raises:
            ValueError: Se o valor de algum atributo for inválido (ex: saldo).
            TypeError: Se algum atributo for incompatível (ex: histórico).
        """
        return ContaMapper.from_dict(dados)

    def to_dict(self, conta: Conta) -> dict:
        """
        Converte uma instância de Conta em dicionário, usando o mapper de conta.

        Args:
            conta (Conta): Objeto de uma subclasse de Conta.

        Returns:
            dict: Dicionário com os dados da conta (e o tipo (subclasse) de Conta incluído!).
        """
        return ContaMapper.to_dict(conta)

    def tipo_de_id(self) -> str:
        """
        Retorna o campo usado como identificador da conta no JSON.

        Returns:
            str: 'numero_conta'
        """
        return "numero_conta"

    def buscar_conta_por_numero(self, numero: str) -> Optional[Conta]:
        """
        Busca uma conta pelo número da conta.

        Args:
            numero (str): Número da conta.

        Returns:
            Optional[Conta]: Conta encontrada ou None.
        """
        return self.buscar_por_id(numero)

    def lista_contas_do_cliente(self, cliente_id: str) -> List[Conta]:
        """
        Busca todas as contas associadas a um cliente.

        Args:
            cliente_id (str): Identificador único do cliente.

        Returns:
            List[Conta]: Lista de contas pertencentes ao cliente.
        """
        return [conta for conta in self.listar_todos_objetos() if conta.cliente_id == cliente_id]
