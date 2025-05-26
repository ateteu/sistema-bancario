from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_fisica import ValidarPessoaFisica as Validar


class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física com CPF e data de nascimento.
    """

    def __init__(self, nome: str, email: str, numero_documento: str, cep: str, numero_endereco: str, endereco: str, telefone: str, data_nascimento: str | datetime):
        """
        Inicializa uma pessoa física com número de documento (CPF) e data de nascimento.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Endereço de e-mail.
            numero_documento (str): CPF da pessoa (11 dígitos).
            cep (str): CEP do endereço.
            numero_endereco (str): Número da residência.
            endereco (str): Endereço completo.
            telefone (str): Telefone da pessoa.
            data_nascimento (str | datetime): Data de nascimento como string (dd/mm/aaaa) ou objeto datetime.
        """
        # Realiza validação de todos os campos usando o validador de pessoa física
        erros = Validar.todos_campos(nome, email, numero_documento, cep, numero_endereco, telefone, data_nascimento)
        if erros:
            raise ValueError("\n".join(erros))

        # Inicializa a superclasse Pessoa com os campos comuns
        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone)

        # Converte string para datetime se necessário
        if isinstance(data_nascimento, str):
            self._data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        else:
            self._data_nascimento = data_nascimento

    def __str__(self):
        return f"{self._nome} (CPF: {self._numero_documento})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento como objeto datetime.
        """
        return self._data_nascimento