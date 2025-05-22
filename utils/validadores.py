import re
import datetime
from utils.constantes import IDADE_MINIMA

def limpar_numeros(texto: str) -> str:
    """
    Remove todos os caracteres que não são dígitos da string.

    Args:
        texto (str): Texto a ser limpo.

    Returns:
        str: Texto contendo apenas dígitos.
    """
    return re.sub(r'\D', '', texto)

def validar_email(email: str) -> None:
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

def validar_cpf(cpf: str) -> None:
    """
    Valida o CPF, removendo caracteres não numéricos antes da validação.

    Args:
        cpf (str): CPF a ser validado.

    Raises:
        ValueError: Se o CPF estiver vazio.
        ValueError: Se o CPF não conter 11 dígitos numéricos após limpeza.
    """
    cpf_limpo = limpar_numeros(cpf)
    if not cpf_limpo:
        raise ValueError("O CPF não pode estar em branco.")

    if len(cpf_limpo) != 11:
        raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")

    # Aqui pode-se implementar a validação dos dígitos verificadores do CPF

def validar_cep(cep: str) -> None:
    """
    Valida o CEP, removendo caracteres não numéricos antes da validação.

    Args:
        cep (str): CEP a ser validado.

    Raises:
        ValueError: Se o CEP estiver vazio.
        ValueError: Se o CEP não conter 8 dígitos numéricos após limpeza.
    """
    cep_limpo = limpar_numeros(cep)
    if not cep_limpo:
        raise ValueError("O CEP não pode estar em branco.")

    if len(cep_limpo) != 8:
        raise ValueError("CEP inválido. Deve conter 8 dígitos numéricos.")

def validar_numero_casa(numero_casa: str) -> None:
    """
    Valida o número da casa, removendo caracteres não numéricos antes da validação.

    Args:
        numero_casa (str): Número da casa a ser validado.

    Raises:
        ValueError: Se o número da casa estiver vazio.
        ValueError: Se o número da casa não for composto somente por dígitos após limpeza.
    """
    numero_limpo = limpar_numeros(numero_casa)
    if not numero_limpo:
        raise ValueError("O número da casa não pode estar em branco.")

    if not numero_limpo.isdigit():
        raise ValueError("Número da casa inválido. Deve conter apenas dígitos.")

def validar_nome(nome: str) -> None:
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

def validar_senha(senha: str) -> None:
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

def validar_data_nascimento(data: datetime, idade_minima: int = IDADE_MINIMA) -> None:
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
