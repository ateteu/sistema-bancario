from dao.dao import DAO
from model.pessoa import Pessoa
from mapper.pessoa_mapper import PessoaMapper
from utils.constantes import ARQUIVO_PESSOAS

class PessoaDAO(DAO):
    """
    DAO para persistência de objetos do tipo Pessoa no arquivo correspondente.

    Esta classe é responsável por serializar e desserializar objetos Pessoa (e suas subclasses)
    para armazenamento e leitura em formato JSON.
    """

    def __init__(self):
        """
        Inicializa o DAO de pessoas com o caminho do arquivo JSON.
        """
        super().__init__(ARQUIVO_PESSOAS)

    def from_dict(self, dados: dict) -> Pessoa:
        """
        Constrói um objeto Pessoa (ou subclasse) a partir de um dicionário.

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância de Pessoa ou subclasse correspondente.

        Raises:
            ValueError: Se houver erro na criação do objeto Pessoa, ao usar dados do dicionário.
        """
        return PessoaMapper.from_dict(dados)

    def to_dict(self, pessoa: Pessoa) -> dict:
        """
        Converte um objeto Pessoa (ou subclasse) em um dicionário serializável.

        Args:
            pessoa (Pessoa): Objeto Pessoa a ser convertido.

        Returns:
            dict: Representação em dicionário da pessoa.

        Raises:
            ValueError: Se a subclasse de Pessoa não for suportada.
        """
        return PessoaMapper.to_dict(pessoa)

    def tipo_de_id(self) -> str:
        """
        Retorna o nome do campo usado como identificador único da pessoa.

        Returns:
            str: 'numero_documento' (vale pra CPF ou CNPJ).
        """
        return "numero_documento"
