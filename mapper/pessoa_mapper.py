from model.pessoa import Pessoa
from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica
from utils.constantes import TIPO_PFISICA, TIPO_PJURIDICA

class PessoaMapper:
    """
    Classe responsável por mapear objetos Pessoa e suas subclasses para e a partir de dicionários.
    """

    @staticmethod
    def from_dict(dados: dict) -> Pessoa:
        """
        Cria uma instância de Pessoa (Física ou Jurídica) a partir de um dicionário.

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância da subclasse de Pessoa reconstruída.
        
        Raises:
            ValueError: Se campos obrigatórios estiverem ausentes ou tipo desconhecido.
        """
        tipo = dados.get("tipo")

        campos_comuns = [
            "tipo", "nome", "email", "numero_documento", "cep",
            "numero_endereco", "endereco", "telefone"
        ]

        campos_faltantes = [campo for campo in campos_comuns if campo not in dados]

        if tipo == TIPO_PFISICA:
            if "data_nascimento" not in dados:
                campos_faltantes.append("data_nascimento")
        elif tipo == TIPO_PJURIDICA:
               dados.setdefault("nome_fantasia", "")

        if campos_faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(campos_faltantes)}")

        if tipo == TIPO_PFISICA:
            return PessoaFisica(
                nome=dados["nome"],
                email=dados["email"],
                numero_documento=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                data_nascimento=dados["data_nascimento"]
            )

        elif tipo == TIPO_PJURIDICA:
            return PessoaJuridica(
                nome=dados["nome"],
                email=dados["email"],
                cnpj=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                nome_fantasia=dados["nome_fantasia"]
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
            "nome": pessoa.get_nome(),
            "email": pessoa.get_email(),
            "numero_documento": pessoa.get_numero_documento(),
            "cep": pessoa.get_cep(),
            "numero_endereco": pessoa.get_numero_endereco(),
            "endereco": pessoa.get_endereco(),
            "telefone": pessoa.get_telefone()
        }

        if isinstance(pessoa, PessoaFisica):
            dados["tipo"] = TIPO_PFISICA
            dados["data_nascimento"] = pessoa.get_data_nascimento().strftime("%d/%m/%Y")

        elif isinstance(pessoa, PessoaJuridica):
            dados["tipo"] = TIPO_PJURIDICA
            dados["nome_fantasia"] = pessoa.get_nome_fantasia()
        else:
            raise ValueError("Subclasse de Pessoa não suportada")

        return dados