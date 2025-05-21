from utils import validadores

class Cliente:
    """
    Representa um cliente do sistema bancário.

    Attributes:
        _nome (str): Nome completo do cliente.
        _cpf (str): CPF do cliente (único e imutável).
        _cep (str): CEP da residência do cliente.
        _numero_casa (str): Número da casa do cliente.
        _endereco (str): Endereço completo do cliente, preenchido a partir do CEP e número.
    """

    def __init__(self, nome: str, senha: str, email: str, cpf: str, cep: str, numero_casa: str, endereco: str) -> None:
        """
        Inicializa um novo cliente com os dados fornecidos.

        Args:
            nome (str): Nome completo do cliente.
            senha (str): Senha de acesso ao sistema.
            email (str): Email do cliente.
            cpf (str): CPF do cliente (único e imutável).
            cep (str): CEP da residência.
            numero_casa (str): Número da casa.
            endereco (str): Endereço completo (resolvido a partir do CEP e número).
        """
        self._nome = nome
        self._senha = senha
        self._email = email
        self._cpf = cpf
        self._cep = cep
        self._numero_casa = numero_casa
        self._endereco = endereco

    def get_nome(self) -> str:
        """
        Retorna o nome do cliente.

        Returns:
            str: Nome do cliente.
        """
        return self._nome

    def set_nome(self, novo_nome: str) -> None:
        """
        Altera o nome do cliente.

        Args:
            novo_nome (str): Novo nome a ser atribuído.
        
        Raises:
            ValueError: Se o nome for inválido.
        """
        validadores.validar_nome(novo_nome)
        self._nome = novo_nome

    def verificar_senha(self, senha_digitada: str) -> bool:
        """
        Verifica se a senha informada é correta.

        Args:
            senha_digitada (str): Senha digitada para verificação.

        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        return self._senha == senha_digitada

    def alterar_senha(self, senha_antiga: str, nova_senha: str) -> bool:
        """
        Altera a senha do cliente se a senha antiga estiver correta.

        Args:
            senha_antiga (str): Senha atual.
            nova_senha (str): Nova senha desejada.

        Returns:
            bool: True se a alteração foi feita, False caso contrário.
        
        Raises:
            ValueError: Se a nova senha não for válida.
        """
        if self.verificar_senha(senha_antiga):
            validadores.validar_senha(nova_senha)
            self._senha = nova_senha
            return True
        return False

    def get_email(self) -> str:
        """
        Retorna o e-mail do cliente.

        Returns:
            str: Email do cliente.
        """
        return self._email

    def set_email(self, novo_email: str) -> None:
        """
        Altera o e-mail do cliente.
        
        Args:
            novo_email (str): Novo email a ser atribuído.
        
        Raises:
            ValueError: Se o e-mail for inválido.
        """
        validadores.validar_email(novo_email)
        self._email = novo_email

    def get_cpf(self) -> str:
        """
        Retorna o CPF do cliente.

        Returns:
            str: CPF do cliente.
        """
        return self._cpf

    def get_cep(self) -> str:
        """
        Retorna o CEP da residência do cliente.

        Returns:
            str: CEP atual.
        """
        return self._cep

    def set_cep(self, novo_cep: str) -> None:
        """
        Altera o CEP da residência do cliente.

        Args:
            novo_cep (str): Novo CEP a ser atribuído.
        
        Raises:
            ValueError: Se o CEP for inválido.
        """
        validadores.validar_cep(novo_cep)
        self._cep = novo_cep

    def get_numero_casa(self) -> str:
        """
        Retorna o número da casa do cliente.

        Returns:
            str: Número da casa.
        """
        return self._numero_casa

    def set_numero_casa(self, novo_numero: str) -> None:
        """
        Altera o número da casa do cliente.

        Args:
            novo_numero (str): Novo número da casa.
        
        Raises:
            ValueError: Se o número da casa for inválido.
        """
        validadores.validar_numero_casa(novo_numero)
        self._numero_casa = novo_numero

    def get_endereco(self) -> str:
        """
        Retorna o endereço completo do cliente.

        Returns:
            str: Endereço completo.
        """
        return self._endereco

    def set_endereco(self, novo_endereco: str) -> None:
        """
        Altera o endereço completo do cliente.

        Args:
            novo_endereco (str): Novo endereço completo a ser atribuído.
        """
        self._endereco = novo_endereco

    def __str__(self) -> str:
        """
        Retorna uma representação textual simples do cliente.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._cpf})"
