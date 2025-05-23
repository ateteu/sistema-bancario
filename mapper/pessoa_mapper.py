from model.pessoa import Pessoa
from model.pessoa_fisica import PessoaFisica
from utils.constantes import TIPO_PFISICA

class PessoaMapper:
    """
    Classe responsável por mapear objetos Pessoa e suas subclasses para e a partir de dicionários.

    Essa classe oferece métodos estáticos para:
    - Criar instâncias de Pessoa a partir de um dicionário (deserialização).
    - Converter instâncias de Pessoa em dicionários (serialização).

    obs: Atualmente suporta apenas a subclasse PessoaFisica.
    """

    @staticmethod
    def from_dict(dados: dict) -> Pessoa:
        """
        Cria uma instância de Pessoa (PF/PJ) a partir de um dicionário.

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância da subclasse de Pessoa reconstruída.
        """
        tipo             = dados.get("tipo")
        nome             = dados.get("nome", "Desconhecido")
        email            = dados.get("email", "Desconhecido")
        numero_documento = dados["numero_documento"]
        cep              = dados.get("cep", "Desconhecido")
        numero_endereco  = dados.get("numero_endereco", "Desconhecido")
        endereco         = dados.get("endereco", "Desconhecido")
        telefone         = dados.get("telefone", "Desconhecido")

        if tipo == TIPO_PFISICA:
            data_nascimento = dados.get("data_nascimento", "Desconhecido")
            return PessoaFisica(nome, email, numero_documento, cep, numero_endereco, endereco, telefone, data_nascimento)
        else:
            raise ValueError(f"Tipo de Pessoa desconhecido: {tipo}")

    @staticmethod
    def to_dict(pessoa: Pessoa) -> dict:
        """
        Converte uma instância de Pessoa em dicionário.

        Args:
            pessoa (Pessoa): Objeto Pessoa a ser convertido.

        Returns:
            dict: Dicionário com os dados da pessoa.
        """
        dados = {
            "nome"             : pessoa.get_nome(),
            "email"            : pessoa.get_email(),
            "numero_documento" : pessoa.get_numero_documento(),
            "cep"              : pessoa.get_cep(),
            "numero_endereco"  : pessoa.get_numero_endereco(),
            "endereco"         : pessoa.get_endereco(),
            "telefone"         : pessoa.get_telefone(),
        }

        if isinstance(pessoa, PessoaFisica):
            dados["tipo"] = TIPO_PFISICA
            dados["data_nascimento"] = pessoa.get_data_nascimento()
        else:
            raise ValueError("Subclasse de Pessoa não suportada")

        return dados
