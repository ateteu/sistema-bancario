import re
import datetime
from utils.constantes import IDADE_MINIMA

class Validar():
    """
    Classe utilitária para validações comuns de dados de entrada.

    Esta classe fornece métodos estáticos para validar diversos tipos de dados,
    como email, senha, data de nascimento, entre outros.

    Exemplos de uso:
        Validar.email("usuario@email.com")
        Validar.cpf("12345678900")
        Validar.data_nascimento(datetime(2000, 5, 20))

    Métodos:
        email(email: str) -> None
        cpf(cpf: str) -> None
        cep(cep: str) -> None
        nome(nome: str) -> None
        senha(senha: str) -> None
        numero_casa(numero: str) -> None
        data_nascimento(data: datetime, idade_minima: int = IDADE_MINIMA) -> None
        _limpar_numeros(texto: str) -> str
    """
    @staticmethod
    def _limpar_numeros(texto: str) -> str:
        """
        Remove todos os caracteres que não são dígitos da string.

        Args:
            texto (str): Texto a ser limpo.

        Returns:
            str: Texto contendo apenas dígitos.
        """
        return re.sub(r'\D', '', texto)

    @staticmethod
    def email(email: str) -> None:
        """
        Valida o formato do email.

        Args:
            email (str): Email a ser validado.

        Raises:
            ValueError: Se o email estiver vazio.
            ValueError: Se o email não corresponder ao formato esperado.
        """
        if not email or email.strip() == "":
            raise ValueError("O email não pode estar em branco.")

        # Regex simples para validar email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise ValueError("Email inválido.")

    @staticmethod
    def cpf(cpf: str) -> None:
        """
        Valida o CPF, removendo caracteres não numéricos antes da validação.

        Args:
            cpf (str): CPF a ser validado.

        Raises:
            ValueError: Se o CPF estiver vazio.
            ValueError: Se o CPF não conter 11 dígitos numéricos após limpeza.
        """
        cpf_limpo = Validar._limpar_numeros(cpf)
        if not cpf_limpo:
            raise ValueError("O CPF não pode estar em branco.")

        if len(cpf_limpo) != 11:
            raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")

        # Aqui pode-se implementar a validação dos dígitos verificadores do CPF

    @staticmethod
    def cep(cep: str) -> None:
        """
        Valida o CEP, removendo caracteres não numéricos antes da validação.

        Args:
            cep (str): CEP a ser validado.

        Raises:
            ValueError: Se o CEP estiver vazio.
            ValueError: Se o CEP não conter 8 dígitos numéricos após limpeza.
        """
        cep_limpo = Validar._limpar_numeros(cep)
        if not cep_limpo:
            raise ValueError("O CEP não pode estar em branco.")

        if len(cep_limpo) != 8:
            raise ValueError("CEP inválido. Deve conter 8 dígitos numéricos.")

    @staticmethod
    def numero_endereco(numero_casa: str) -> None:
        """
        Valida o número do endereço, removendo caracteres não numéricos antes da validação.

        Args:
            numero_casa (str): Número do endereço a ser validado.

        Raises:
            ValueError: Se o número do endereço estiver vazio.
            ValueError: Se o número do endereço não for composto somente por dígitos após limpeza.
        """
        numero_limpo = Validar._limpar_numeros(numero_casa)
        if not numero_limpo:
            raise ValueError("O número do endereço não pode estar em branco.")

        if not numero_limpo.isdigit():
            raise ValueError("Número do endereço inválido. Deve conter apenas dígitos.")

    @staticmethod
    def nome(nome: str) -> None:
        """
        Valida o nome, garantindo que não esteja vazio e que contenha apenas letras e espaços.

        Args:
            nome (str): Nome a ser validado.

        Raises:
            ValueError: Se o nome estiver vazio.
            ValueError: Se o nome contiver caracteres inválidos.
        """
        if not nome or nome.strip() == "":
            raise ValueError("O nome não pode estar em branco.")

        padrao = r'^[A-Za-zÀ-ÿ\s]+$'  # aceita letras (inclusive acentuadas) e espaços
        if not re.match(padrao, nome):
            raise ValueError("Nome inválido. Deve conter apenas letras e espaços.")

    @staticmethod
    def senha(senha: str) -> None:
        """
        Valida a força da senha. A senha deve conter pelo menos:
        - 8 caracteres
        - Uma letra maiúscula
        - Uma letra minúscula
        - Um número
        - Um caractere especial

        Raises:
            ValueError: Se a senha não atender aos critérios.
        """
        if (
            len(senha) < 8
            or not re.search(r"[A-Z]", senha)
            or not re.search(r"[a-z]", senha)
            or not re.search(r"[0-9]", senha)
            or not re.search(r"[\W_]", senha)
        ):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
            )

    @staticmethod
    def data_nascimento(data: datetime, idade_minima: int = IDADE_MINIMA) -> None:
        """
        Valida uma data de nascimento.

        Verifica se a data não é futura e se a pessoa tem a idade mínima.

        Args:
            data (datetime): Data de nascimento a validar.
            idade_minima (int, opcional): Idade mínima exigida.

        Raises:
            ValueError: Se a data for no futuro ou a idade for inferior à mínima.
        """
        hoje = datetime.today()

        if data > hoje:
            raise ValueError("A data de nascimento não pode estar no futuro.")

        idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))

        if idade < idade_minima:
            raise ValueError(f"A pessoa deve ter pelo menos {idade_minima} anos.")

    @staticmethod
    def saldo(valor: float) -> None:
        """
        Valida o valor do saldo.

        Args:
            valor (float): Valor a ser validado.

        Raises:
            ValueError: Se o valor não for um número real válido ou for negativo.
            TypeError: Se o valor não for numérico.
        """
        if not isinstance(valor, (int, float)):
            raise TypeError("O saldo deve ser um número.")
        
        if not (valor == valor and valor != float("inf") and valor != float("-inf")):
            raise ValueError("O saldo não pode ser NaN ou infinito.")
        
        if valor < 0:
            raise ValueError("O saldo não pode ser negativo.")

    @staticmethod
    def estado_da_conta(valor: bool) -> None:
        """
        Valida se o estado da conta é um valor booleano.

        Args:
            valor (bool): Valor booleano que representa o estado da conta.

        Raises:
            TypeError: Se o valor informado não for do tipo booleano.
        """
        if not isinstance(valor, bool):
            raise TypeError("O estado da conta deve ser um valor booleano.")

    @staticmethod
    def historico(valor: list) -> None:
        """
        Valida se o histórico da conta aé uma lista de strings.

        Args:
            valor (list): Lista que representa o histórico a ser validado.

        Raises:
            TypeError: Se o valor não for uma lista.
            TypeError: Se algum item da lista não for uma string.
        """
        if not isinstance(valor, list):
            raise TypeError("Histórico da conta deve ser uma lista.")
        for item in valor:
            if not isinstance(item, str):
                raise TypeError("Cada item do histórico da conta deve ser uma string.")