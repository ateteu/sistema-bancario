import requests
from utils.validadores import Validar

class API():
    """
    Classe utilitária responsável por consultar e compor endereços a partir de CEPs,
    utilizando a API pública ViaCEP.
    """

    def buscar_endereco_por_cep(cep: str, numero: str) -> str:
        """
        Consulta o endereço completo a partir de um CEP e número do imóvel,
        utilizando a API pública ViaCEP.

        Args:
            cep (str): CEP brasileiro, com ou sem formatação (serão considerados apenas os dígitos).
            numero (str): Número do imóvel a ser incluído na composição do endereço.

        Returns:
            str: Endereço formatado no padrão: "logradouro, número - bairro, localidade - UF, CEP".

        Raises:
            ValueError: Se o CEP for inválido ou não encontrado.
            ValueError: Se o número do endereço for inválido.
            ValueError: Se houver erro na consulta.
        """
        Validar.cep(cep)
        Validar.numero_endereco(numero)

        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError("Erro ao buscar o endereço. Tente novamente mais tarde.")

        data = response.json()
        if "erro" in data:
            raise ValueError("CEP não encontrado. Verifique se está digitado corretamente.")

        logradouro = data["logradouro"]
        bairro     = data["bairro"]
        localidade = data["localidade"]
        uf         = data["uf"]

        return f"{logradouro}, {numero} - {bairro}, {localidade} - {uf}, {cep}"
