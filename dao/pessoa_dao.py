from model.pessoa import Pessoa
from model.pessoa_fisica import PessoaFisica
from dao.dao import DAO
from utils.constantes import (
    ARQUIVO_PESSOAS,
    TIPO_PFISICA,
    TIPO_PJURIDICA
)

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
        Cria uma instância de Pessoa (PF/PJ) a partir de um dicionário.

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância da subclasse de Pessoa reconstruída.
        """
        tipo             = dados.get("tipo")
        numero_documento = dados["numero_documento"]
        nome             = dados.get("nome", "Desconhecido")
        email            = dados.get("email", "Desconhecido")
        cep              = dados.get("cep", "Desconhecido")
        numero_endereco  = dados.get("numero_endereco", "Desconhecido")
        endereco         = dados.get("endereco", "Desconhecido")
        
        pessoa._set_endereco = endereco

        if tipo == TIPO_PFISICA:
            data_nascimento = dados.get("data_nascimento", "")
            pessoa = PessoaFisica(numero_documento, nome, email, cep, numero_endereco, data_nascimento)
        else:
            raise ValueError(f"Tipo de Pessoa desconhecido: {tipo}")
        return pessoa
    
    def to_dict(self, pessoa: Pessoa) -> dict:
        """
        Converte uma instância de Pessoa em dicionário.

        Args:
            pessoa (Pessoa): Objeto Pessoa a ser convertido.

        Returns:
            dict: Dicionário com os dados da pessoa.
        """
        dados = {
            "numero_documento" : pessoa.get_numero_documento(),
            "nome"             : pessoa.get_nome(),
            "email"            : pessoa.get_email(),
            "cep"              : pessoa.get_cep(),
            "numero_endereco"  : pessoa.get_numero_endereco(),
            "endereco"         : pessoa.get_endereco(),
        }

        if isinstance(pessoa, PessoaFisica):
            dados["tipo"] = TIPO_PFISICA
            dados["data_nascimento"] = pessoa.get_data_nascimento()
        else:
            raise ValueError("Subclasse de Pessoa não suportada")

        return dados

    def tipo_de_id(self) -> str:
        """
        Retorna o nome do campo usado como identificador único da pessoa.

        Returns:
            str: 'numero_documento' (vale pra CPF ou CNPJ).
        """
        return "numero_documento"
