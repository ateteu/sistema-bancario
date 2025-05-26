from typing import Optional, List
from model.cliente import Cliente
from dao.dao import DAO
from dao.pessoa_dao import PessoaDAO
from dao.conta_dao import ContaDAO
from utils.constantes import ARQUIVO_CLIENTES

class ClienteDAO(DAO):
    """
    DAO para persistência de Clientes no arquivo correspondente.
    """

    def __init__(self):
        """
        Inicializa o DAO de clientes e os DAOs auxiliares de pessoas e contas.
        """
        super().__init__(ARQUIVO_CLIENTES)
        self._pessoa_dao = PessoaDAO()
        self._conta_dao = ContaDAO()

    def criar_objeto(self, dados: dict) -> Cliente:
        """
        Cria uma instância de Cliente, usando dados passados, carregando Pessoa e Contas.

        Args:
            dados (dict): Dicionário com campos de cliente.

        Returns:
            Cliente: Objeto Cliente pronto para uso.
        """
        # Usa o DAO de pessoa para buscar a pessoa com o id (cpf/cnpj) correspondente
        pessoa = self._pessoa_dao.buscar_por_id(dados["numero_documento"])

        # Usa o DAO de conta para buscar a(s) conta(s) com o id (numero_conta) correspondente
        contas = [self._conta_dao.buscar_por_id(n) for n in dados.get("contas", [])]

        # Cria o objeto cliente com os dados correspondentes
        return Cliente(pessoa=pessoa, senha=dados["senha"], contas=contas)

    def extrair_dados_do_objeto(self, obj: Cliente) -> dict:
        """
        Converte instância de Cliente para dicionário.

        Args:
            obj (Cliente): Objeto Cliente a serializar.

        Returns:
            dict: Dicionário com campos para JSON.
        """
        return {
            "numero_documento" : obj.pessoa.get_numero_documento(),
            "senha"     : obj._senha,
            "contas"    : [c.get_numero_conta() for c in obj.contas],
        }

    def tipo_de_id(self) -> str:
        """
        Retorna o campo usado como identificador no JSON de clientes.

        Returns:
            str: 'numero_documento'
        """
        return "numero_documento"

    def buscar_por_id(self, id_valor: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo identificador único (CPF ou documento).

        Args:
            id_valor (str): Valor do documento do cliente.

        Returns:
            Optional[Cliente]: Instância de Cliente se encontrado, ou None caso contrário.
        """
        return super().buscar_por_id(id_valor)

    def buscar_cliente_por_numero_conta(self, numero_conta: str) -> Optional[Cliente]:
        """
        Encontra o cliente dono de uma determinada conta.

        Args:
            numero_conta (str): Número da conta.

        Returns:
            Optional[Cliente]: Cliente que possui a conta, ou None.
        """
        for cliente in self.listar_todos_objetos():
            if numero_conta in [c.get_numero_conta() for c in cliente.contas]:
                return cliente
        return None