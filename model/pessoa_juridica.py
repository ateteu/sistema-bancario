from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_juridica import ValidarPessoaJuridica as Validar

class PessoaJuridica(Pessoa):
    """
    Representa uma pessoa jurídica com CNPJ e nome fantasia.
    """

    def __init__(self, nome: str, email: str, cnpj: str, cep: str, numero_endereco: str, endereco: str, telefone: str, nome_fantasia: str = ""):
        erros = Validar.todos_campos(nome, email, cnpj, cep, numero_endereco, telefone, nome_fantasia)
        if erros:
            raise ValueError("\n".join(erros))

        super().__init__(nome, email, cnpj, cep, numero_endereco, telefone)
        self._nome_fantasia = nome_fantasia
        

    def __str__(self):
        nome_exibicao = self._nome_fantasia if self._nome_fantasia else "Empresa sem nome fantasia"
        return f"{nome_exibicao} (CNPJ: {self._numero_documento})"


    def get_nome_fantasia(self) -> str:
        return self._nome_fantasia or ""
