from datetime import datetime

def data_hora_atual_str() -> str:
    """
    Retorna a data e hora atual formatada como string.

    Returns:
        str: Data e hora no formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
