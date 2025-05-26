"""
Definições visuais reutilizáveis do sistema bancário.

Este módulo centraliza ícones, cores e tamanhos de fonte,
facilitando a consistência visual e a manutenção.
"""

# Ícones padrão para campos de entrada
ICONES_CAMPOS = {
    "nome": "person",
    "cpf": "badge",
    "telefone": "call",
    "email": "mail",
    "senha": "lock",
    "cep": "location_on",
    "numero": "pin",
    "data_nascimento": "calendar_today",
}

# Paleta de cores do sistema
CORES = {
    "fundo": "#f8f9fa",     # Cor de fundo clara para páginas
    "primaria": "#0077cc",  # Azul padrão para botões e destaques
    "erro": "#e53935",      # Vermelho para mensagens de erro
    "sucesso": "#2e7d32",   # Verde para confirmações
    "texto": "#212121",     # Cor padrão para textos escuros
}

# Tamanhos de fonte padronizados
FONTES = {
    "titulo": 22,    # Fontes de títulos principais
    "normal": 16,    # Texto padrão
    "pequena": 13,   # Texto auxiliar ou informativo
}
