from typing import Optional, List
from model.cliente import Cliente
from dao.dao import DAO
from dao.pessoa_dao import PessoaDAO
from dao.conta_dao import ContaDAO
from utils.constantes import ARQUIVO_CLIENTES

class ClienteDAO(DAO):
    """
    DAO para persistência de Clientes em 'clientes.json'.
    """

    def __init__(self):
        """
        Inicializa o DAO de clientes e os DAOs auxiliares de pessoas e contas.
        """
        super().__init__(ARQUIVO_CLIENTES)
        self._pessoa_dao = PessoaDAO()
        self._conta_dao = ContaDAO()

    def from_dict(self, dados: dict) -> Cliente:
        """
        Converte dicionário em instância de Cliente, carregando Pessoa e Contas.

        Args:
            dados (dict): Dicionário com campos de cliente.

        Returns:
            Cliente: Objeto Cliente pronto para uso.
        """
        pessoa = self._pessoa_dao.buscar_por_id(dados["documento"])
        contas = [self._conta_dao.buscar_por_id(n) for n in dados.get("contas", [])]
        return Cliente(pessoa=pessoa, senha=dados["senha"], contas=contas)

    def to_dict(self, obj: Cliente) -> dict:
        """
        Converte instância de Cliente para dicionário.

        Args:
            obj (Cliente): Objeto Cliente a serializar.

        Returns:
            dict: Dicionário com campos para JSON.
        """
        return {
            "documento": obj.pessoa.get_numero_documento(),
            "senha": obj._senha,
            "contas": [c.get_numero_conta() for c in obj.contas],
        }

    def tipo_de_id(self) -> str:
        """
        Retorna o campo usado como identificador no JSON de clientes.

        Returns:
            str: 'numero_documento'
        """
        return "numero_documento"

    def buscar_cliente_por_numero_documento(self, numero_documento: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo número do documento (CPF/CNPJ).

        Args:
            numero_documento (str): Número de documento do cliente.

        Returns:
            Optional[Cliente]: Cliente encontrado ou None.
        """
        return self.buscar_por_id(numero_documento)

    def buscar_cliente_por_numero_conta(self, numero_conta: str) -> Optional[Cliente]:
        """
        Encontra o cliente dono de uma determinada conta.

        Args:
            numero_conta (str): Número da conta.

        Returns:
            Optional[Cliente]: Cliente que possui a conta, ou None.
        """
        for cliente in self.listar_todos_clientes():
            if numero_conta in [c.get_numero_conta() for c in cliente.contas]:
                return cliente
        return None

    def listar_todos_clientes(self) -> List[Cliente]:
        """
        Retorna todos os clientes carregados.

        Returns:
            List[Cliente]: Lista de clientes.
        """
        return super().listar_todos_objetos()
