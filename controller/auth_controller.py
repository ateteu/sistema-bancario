from dao.cliente_dao import ClienteDAO
from utils.logger import logger

class AuthController:
    """
    Controlador responsável por autenticação de usuários:
    login e logout.

    Mantém uma sessão simples em memória através de um dicionário que associa
    identificadores de usuário a objetos Cliente autenticados.
    """

    sessao_ativa = {}

    @staticmethod
    def login(numero_documento: str, senha: str) -> dict:
        """
        Realiza login de um cliente com base no documento e senha.

        Args:
            numero_documento (str): CPF ou identificador da pessoa.
            senha (str): Senha informada pelo usuário.

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
        logger.info(f"Tentando login com documento: {numero_documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(numero_documento)

            if cliente is None:
                logger.warning(f"Cliente não encontrado: {numero_documento}")
                return {
                    "status"   : "erro",
                    "mensagem" : "Cliente não encontrado."
                }

            if not cliente.verificar_senha(senha):
                logger.warning("Senha incorreta para cliente.")
                return {
                    "status"   : "erro",
                    "mensagem" : "Senha incorreta."
                }

            AuthController.sessao_ativa[numero_documento] = cliente

            logger.info("Login realizado com sucesso.")
            return {
                "status"     : "sucesso",
                "mensagem"   : "Login realizado com sucesso.",
                "usuario_id" : numero_documento
            }
        except Exception as e:
            logger.warning(f"Erro durante login: {e}")
            return {
                "status"   : "erro",
                "mensagem" : "Erro inesperado ao tentar login."
            }

    @staticmethod
    def logout(usuario_id: str) -> dict:
        """
        Realiza logout de um cliente.

        Args:
            usuario_id (str): Identificador do cliente (documento).

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
        logger.info(f"Logout solicitado para ID: {usuario_id}")

        if usuario_id in AuthController.sessao_ativa:
            del AuthController.sessao_ativa[usuario_id]
            logger.info("Logout bem-sucedido.")
            return {
                "status"   : "sucesso",
                "mensagem" : "Logout realizado com sucesso."
            }
        else:
            logger.warning("Tentativa de logout para sessão inexistente.")
            return {
                "status"   : "erro",
                "mensagem" : "Usuário não está logado."
            }
