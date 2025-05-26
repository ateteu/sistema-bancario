from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_juridica import ValidarPessoaJuridica as Validar


class PessoaJuridica(Pessoa):
    """
    Representa uma pessoa jurídica com CNPJ e nome fantasia.
    Herda os campos comuns da classe Pessoa.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        numero_documento: str,
        cep: str,
        numero_endereco: str,
        endereco: str,
        telefone: str,
        nome_fantasia: str = ""
    ):
        """
        Inicializa uma Pessoa Jurídica com os dados obrigatórios e nome fantasia opcional.

        Args:
            nome (str): Nome da empresa (razão social).
            email (str): E-mail de contato.
            numero_documento (str): CNPJ.
            cep (str): CEP da sede.
            numero_endereco (str): Número do endereço.
            endereco (str): Endereço completo.
            telefone (str): Telefone de contato.
            nome_fantasia (str, opcional): Nome fantasia da empresa.
        """
        erros = Validar.todos_campos(
            nome, email, numero_documento, cep, numero_endereco, telefone, nome_fantasia
        )
        if erros:
            raise ValueError("\n".join(erros))

        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone)
        self._nome_fantasia = nome_fantasia

    def __str__(self) -> str:
        """
        Retorna uma representação textual da pessoa jurídica.

        Returns:
            str: Nome fantasia (ou mensagem padrão) com o CNPJ.
        """
        nome_exibicao = self._nome_fantasia.strip() or "Empresa sem nome fantasia"
        return f"{nome_exibicao} (CNPJ: {self._numero_documento})"

    def get_nome_fantasia(self) -> str:
        """
        Retorna o nome fantasia da empresa.

        Returns:
            str: Nome fantasia (ou string vazia).
        """
        return self._nome_fantasia or ""

    def get_tipo(self) -> str:
        """
        Retorna o tipo da pessoa ('juridica').

        Returns:
            str: Tipo da pessoa.
        """
        return "juridica"