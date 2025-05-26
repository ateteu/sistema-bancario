from utils.logger import logger
from dao.pessoa_dao import PessoaDAO
from dao.cliente_dao import ClienteDAO
from model.cliente import Cliente


class CadastroController:
    """
    Controlador responsável por gerenciar o cadastro de
    usuários no sistema (clientes).
    """

    @staticmethod
    def cadastrar_cliente(dados: dict) -> dict:
        """
        Cadastra um novo cliente no sistema a partir de dados fornecidos.

        Args:
            dados (dict): Dicionário com dados para criação do cliente.

        Returns:
            dict: Resultado da operação, com status e mensagem.
        """
        numero_documento = dados.get("numero_documento")
        email = dados.get("email")

        logger.info(f"Iniciando cadastro de cliente com documento: {numero_documento}")

        cliente_dao = ClienteDAO()

        # Verifica se já existe cliente com o mesmo documento
        if cliente_dao.buscar_por_id(numero_documento):
            return {
                "status": "erro",
                "mensagem": f"Já existe um cliente cadastrado com o documento {numero_documento}."
            }

        # Verifica se já existe cliente com o mesmo e-mail (evita criar pessoa antes disso)
        pessoas_raw = PessoaDAO()._ler_dados_do_json()
        email_em_uso = any(p.get("email") == email for p in pessoas_raw)

        if email_em_uso:
            return {
                "status": "erro",
                "mensagem": f"Já existe um cliente cadastrado com o e-mail {email}."
            }

        try:
            CadastroController._criar_pessoa(dados)
            CadastroController._criar_cliente(numero_documento, dados["senha"])
            return {
                "status": "sucesso",
                "mensagem": "Cadastro realizado com sucesso"
            }
        except ValueError as e:
            logger.warning(f"Erro de validação: {e}")
            return {"status": "erro", "mensagem": str(e)}
        except TypeError as e:
            logger.warning(f"Erro de tipagem: {e}")
            return {"status": "erro", "mensagem": str(e)}
        except Exception as e:
            logger.warning(f"Erro inesperado: {e}")
            return {"status": "erro", "mensagem": "Erro inesperado ao cadastrar cliente"}

    @staticmethod
    def _criar_pessoa(dados: dict) -> None:
        """
        Cria e salva um objeto Pessoa a partir de um dicionário de dados.
        A conversão e persistência são feitas por meio do PessoaDAO.
        """
        from copy import deepcopy
        pessoa_dao = PessoaDAO()

        dados_pessoa = deepcopy(dados)

        # Garante que nome_fantasia sempre exista
        dados_pessoa["nome_fantasia"] = dados_pessoa.get("nome_fantasia", "").strip()

        pessoa = pessoa_dao.criar_objeto(dados_pessoa)
        numero_documento = pessoa.get_numero_documento()

        pessoa_dao.salvar_objeto(pessoa)

    @staticmethod
    def _criar_cliente(numero_documento: str, senha: str) -> None:
        """
        Cria e salva um objeto Cliente a partir de um documento e senha.
        """
        pessoa = PessoaDAO().buscar_por_id(numero_documento)
        if pessoa is None:
            raise ValueError(f"Pessoa não encontrada para o documento [{numero_documento}] informado.")

        cliente = Cliente(pessoa=pessoa, senha=senha)
        cliente_dao = ClienteDAO()

        cliente_dao.salvar_objeto(cliente)
