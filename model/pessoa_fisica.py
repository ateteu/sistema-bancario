from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores import Validar
#from utils.helpers import converter_str_para_datetime

class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com data de nascimento e representação textual por CPF.
    """

    def __init__(self, nome: str, email: str, numero_documento: str, cep: str, numero_endereco: str, telefone: str, data_nascimento: str):
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
            data_nascimento (str): Data de nascimento no formato "dd/mm/aaaa".

        Raises:
            ValueError: Se algum dos dados fornecidos for inválido (ex: data de nascimento, email, etc).
            ValueError: Se houver erro ao usar a API (viaCEP) para atualizar o endereço.
        """
        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone)

        data_convertida = datetime.strptime(data_nascimento, "%d/%m/%Y")
        Validar.data_nascimento(data_convertida)
        self._data_nascimento = data_convertida # Armazenado como datetime

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
