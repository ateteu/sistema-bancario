from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_fisica import ValidarPessoaFisica as Validar
#from utils.helpers import converter_str_para_datetime

class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com data de nascimento e representação textual por CPF.
    """

    def __init__(self, nome: str, email: str, numero_documento: str, cep: str, numero_endereco: str, telefone: str, data_nascimento: str|datetime):
        """
        Inicializa uma pessoa física.
        Obs: Data de nascimento é recebido como str, mas armazenado no objeto como datetime.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Email da pessoa.
            numero_documento (str): Número de documento da pessoa (único e imutável).
            cep (str): CEP da residência.
            numero_endereco (str): Número do endereço.
            telefone (str): Telefone da pessoa.
            data_nascimento (str|datetime): Data de nascimento no formato "dd/mm/aaaa" se for str ou
            no formato datetime.

        Raises:
            ValueError: Se algum dos dados fornecidos for inválido (ex: data de nascimento, email, etc).
            ValueError: Se houver erro ao usar a API (viaCEP) para atualizar o endereço.
        """
        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone)
        self._data_nascimento = Validar.data_nascimento(data_nascimento)

    def __str__(self) -> str:
        """
        Retorna uma representação textual simples da pessoa física.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._numero_documento})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento da pessoa física.

        Returns:
            datetime: Data de nascimento da pessoa.
        """
        return self._data_nascimento
