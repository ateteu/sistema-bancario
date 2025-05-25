# Responsável pela criação de novos usuários (pessoa física, futura pessoa jurídica).
# Métodos:
#     cadastrar_pessoa(dados: dict)
#     (futuro) cadastrar_pessoa_juridica(dados: dict)

from model.pessoa import Pessoa
from model.pessoa_fisica import PessoaFisica
from dao.pessoa_dao import PessoaDAO

def cadastrar_pessoa(dados: dict):
    try:
        pessoa = PessoaFisica.from_dict(dados)
        PessoaDAO.salvar(pessoa)
        return {"status": "sucesso", "mensagem": "Conta criada com sucesso"}
    
    except ValueError as e:
        return {"status": "erro", "mensagem": str(e)}

    except Exception as e:
        return {"status": "erro", "mensagem": "Erro inesperado ao cadastrar pessoa"}
    