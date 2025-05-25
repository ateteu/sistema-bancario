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
        logger.info(f"Iniciando cadastro de cliente com documento: {dados.get('documento')}")
        try:
            CadastroController._criar_pessoa(dados)
            CadastroController._criar_cliente(dados["documento"], dados["senha"])
            return {
                "status"   : "sucesso",
                "mensagem" : "Cadastro realizado com sucesso"
            }
        except ValueError as e:
            logger.warning(f"Erro de validação: {e}")
            return {
                "status"   : "erro",
                "mensagem" : str(e)
            }
        except TypeError as e:
            logger.warning(f"Erro de tipagem: {e}")
            return {
                "status"   : "erro",
                "mensagem" : str(e)
            }
        except Exception as e:
            logger.warning(f"Erro inesperado: {e}")
            return {
                "status"   : "erro",
                "mensagem" : "Erro inesperado ao cadastrar cliente"
            }

    @staticmethod
    def _criar_pessoa(dados: dict) -> None:
        """
        Cria e salva um objeto Pessoa a partir de um dicionário de dados.
        A conversão e persistência são feitas por meio do PessoaDAO.

        Args:
            dados (dict): Dicionário com os dados pessoais obrigatórios.
        
        Raises:
            ValueError: Se falhar na criação da pessoa.
        """
        pessoa = PessoaDAO().from_dict(dados)
        PessoaDAO().adicionar_objeto(pessoa)

    @staticmethod
    def _criar_cliente(numero_documento: str, senha: str) -> None:
        """
        Cria e salva um objeto Cliente a partir de um documento e senha.

        Procura a Pessoa correspondente ao documento e associa à nova
        instância de Cliente.

        Args:
            numero_documento (str): Documento da pessoa (ex: CPF).
            senha (str): Senha definida para o cliente.

        Raises:
            ValueError: Se nenhuma Pessoa for encontrada para o documento.
            TypeError: Se 'pessoa não for uma instância de Pessoa
        """
        pessoa = PessoaDAO().buscar_por_id(numero_documento)
        if pessoa is None:
            raise ValueError("Pessoa não encontrada para o documento informado.")

        cliente = Cliente(pessoa=pessoa, senha=senha)
        ClienteDAO().adicionar_objeto(cliente)
