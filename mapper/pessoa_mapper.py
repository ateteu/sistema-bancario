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
        Cria uma instância de Pessoa a partir de um dicionário.
        Obs: apenas disponível para Pessoa Física no momento!

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância da subclasse de Pessoa reconstruída.
        
        Raises:
            ValueError: Se um ou mais campos obrigatórios estiverem ausentes.
            ValueError: Se o 'tipo' da conta (salvo no BD) for desconhecido.
        """
        campos_obrigatorios = [
            "tipo", "nome", "email", "numero_documento", "cep",
            "numero_endereco", "endereco", "telefone", "data_nascimento"
        ]

        # Verifica todos campos faltantes no Banco de dados
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados]
        if campos_faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(campos_faltantes)}")

        tipo             = dados["tipo"]
        nome             = dados["nome"]
        email            = dados["email"]
        numero_documento = dados["numero_documento"]
        cep              = dados["cep"]
        numero_endereco  = dados["numero_endereco"]
        endereco         = dados["endereco"]
        telefone         = dados["telefone"]
        
        if tipo == TIPO_PFISICA:
            data_nascimento  = dados["data_nascimento"]
            return PessoaFisica(
                nome, email, numero_documento, cep, numero_endereco, endereco, telefone, data_nascimento
            )
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
