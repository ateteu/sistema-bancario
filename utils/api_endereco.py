import requests

def buscar_endereco_por_cep(cep: str, numero: str) -> str:
    cep = ''.join(filter(str.isdigit, cep))

    # Validação de segurança do CEP
    if len(cep) != 8:
        raise ValueError("CEP inválido. Deve conter 8 dígitos numéricos.")

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Erro ao buscar o endereço. Tente novamente mais tarde.")

    data = response.json()
    if "erro" in data:
        raise ValueError("CEP não encontrado.")

    logradouro = data["logradouro"]
    bairro     = data["bairro"]
    localidade = data["localidade"]
    uf         = data["uf"]

    return f"{logradouro}, {numero} - {bairro}, {localidade} - {uf}, {cep}"
