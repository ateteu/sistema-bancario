import re
from abc import ABC

class ValidarPessoa(ABC):
    """
    Classe utilitária para validações comuns de dados de entrada.

    Esta classe fornece métodos estáticos para validar diversos tipos de dados,
    como email, senha, data de nascimento, entre outros.

    Exemplo de uso: ValidarPessoa.email("usuario@email.com")
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
        if not email.strip():
            raise ValueError("O email não pode estar em branco.")

        # Regex simples para validar email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise ValueError("Email inválido.")

    @staticmethod
    def telefone(telefone: str) -> None:
        """
        Valida o número de telefone brasileiro.

        Args:
            telefone (str): Número de telefone com ou sem formatação.

        Raises:
            ValueError: Se o telefone estiver vazio.
            ValueError: Se o telefone for inválido.
            ValueError: Se o telefone não tiver a quantia certa de dígitos.
        """
        telefone_limpo = ValidarPessoa._limpar_numeros(telefone)

        if not telefone_limpo:
            raise ValueError("O telefone não pode estar em branco.")
        elif len(telefone_limpo) == 10:
            # fixo: DDD + número (ex: 3133345678)
            if not re.match(r'^[1-9]{2}[2-5]\d{7}$', telefone_limpo):
                raise ValueError("Telefone fixo inválido.")
        elif len(telefone_limpo) == 11:
            # celular: DDD + 9 + número (ex: 31999999999)
            if not re.match(r'^[1-9]{2}9\d{8}$', telefone_limpo):
                raise ValueError("Telefone celular inválido.")
        else:
            raise ValueError("Número de telefone deve conter 10 ou 11 dígitos.") 
    
    @staticmethod
    def numero_documento(numero_documento: str) -> None:
        """
        Valida se o número de documento é válido (CPF ou CNPJ).
        Aceita strings com ou sem pontos/traços.

        Args:
            numero_documento (str): Número de documento a ser validado.

        Raises:
            ValueError: Se o número de documento estiver vazio.
            ValueError: Se não contiver apenas números.
            ValueError: Se não tiver 11 (CPF) ou 14 (CNPJ) dígitos.
        """
        numero_documento_limpo = ValidarPessoa._limpar_numeros(numero_documento)

        if not numero_documento_limpo:
            raise ValueError("O número de documento não pode estar em branco.")

        if not numero_documento_limpo.isdigit():
            raise ValueError("Número de documento deve conter apenas dígitos.")
        
        if len(numero_documento_limpo) not in (11, 14):
            raise ValueError("Número de documento deve ter 11 dígitos (CPF) ou 14 (CNPJ).")

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
        cep_limpo = ValidarPessoa._limpar_numeros(cep)
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
        numero_limpo = ValidarPessoa._limpar_numeros(numero_casa)
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
        if not nome.strip():
            raise ValueError("O nome não pode estar em branco.")

        padrao = r'^[A-Za-zÀ-ÿ\s]+$'  # aceita letras (inclusive acentuadas) e espaços
        if not re.match(padrao, nome):
            raise ValueError("Nome inválido. Use apenas letras e espaços, sem números ou símbolos.")
