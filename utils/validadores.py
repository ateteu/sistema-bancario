import re
from datetime import datetime
from utils.constantes import IDADE_MINIMA, TAMANHO_MIN_NUMERO_CONTA

class Validar():
    """
    Classe utilitária para validações comuns de dados de entrada.

    Esta classe fornece métodos estáticos para validar diversos tipos de dados,
    como email, senha, data de nascimento, entre outros.

    Exemplo de uso: Validar.email("usuario@email.com")
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
        telefone_limpo = Validar._limpar_numeros(telefone)

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
        numero_documento_limpo = Validar._limpar_numeros(numero_documento)

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
    def numero_conta(numero_conta: str) -> None:
        """
        Valida o número da conta.

        Verifica se o valor fornecido é uma string composta apenas por dígitos,
        com comprimento mínimo definido por 'TAMANHO_MIN_NUMERO_CONTA'.

        Args:
            numero_conta (str): Número da conta a ser validado.

        Raises:
            TypeError: Se o número da conta não for uma string.
            ValueError: Se o número da conta estiver vazio.
            ValueError: Se o número da conta contiver caracteres não numéricos.
            ValueError: Se o número da conta for menor que o comprimento mínimo exigido.
        """
        if not isinstance(numero_conta, str):
            raise TypeError("Número da conta deve ser uma string.")
        if numero_conta == "":
            raise ValueError("Número da conta não pode ser vazio.")
        if not numero_conta.isdigit():
            raise ValueError("Número da conta deve conter apenas dígitos.")
        if len(numero_conta) < TAMANHO_MIN_NUMERO_CONTA:
            raise ValueError("Número da conta muito curto.")

    @staticmethod
    def _verificacoes_basicas_saldo(saldo: float) -> None:
        """
        Verifica se o saldo é um número real válido e finito.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN (não é um número) ou infinito.
        """
        if not isinstance(saldo, (int, float)):
            raise TypeError("O saldo deve ser um número.")
        if not (saldo == saldo and saldo != float("inf") and saldo != float("-inf")):
            raise ValueError("O saldo não pode ser NaN ou infinito.")

    @staticmethod
    def saldo_positivo_ou_zero(saldo: float) -> None:
        """
        Valida que o saldo é numérico, finito e não-negativo.

        Essa validação é usada em operações que não permitem saldo negativo,
        como transferências bancárias.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
            ValueError: Se o saldo for negativo.
        """
        Validar._verificacoes_basicas_saldo(saldo)
        if saldo < 0:
            raise ValueError("O saldo não pode ser negativo.")

    @staticmethod
    def saldo_livre(saldo: float) -> None:
        """
        Valida que o saldo é numérico e finito, permitindo valores negativos.

        Essa validação é usada em situações onde saldos negativos são aceitáveis,
        como atualizações mensais de cobrança.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
        """
        Validar._verificacoes_basicas_saldo(saldo)

    @staticmethod
    def historico(historico: list) -> None:
        """
        Valida se o histórico da conta é uma lista de strings.

        Args:
            historico (list): Lista que representa o histórico a ser validado.

        Raises:
            TypeError: Se o histórico não for uma lista.
            TypeError: Se algum item da lista não for uma string.
        """
        if not isinstance(historico, list):
            raise TypeError("Histórico da conta deve ser uma lista.")
        for item in historico:
            if not isinstance(item, str):
                raise TypeError("Cada item do histórico da conta deve ser uma string.")

    @staticmethod
    def estado_da_conta(estado: bool) -> None:
        """
        Valida se o estado da conta é um valor booleano.

        Args:
            estado (bool): Valor booleano que representa o estado da conta.

        Raises:
            TypeError: Se o estado informado não for do tipo booleano.
        """
        if not isinstance(estado, bool):
            raise TypeError("O estado da conta deve ser um valor booleano.")
