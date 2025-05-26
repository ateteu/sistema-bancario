from utils.logger import logger
from dao.pessoa_dao import PessoaDAO
from dao.cliente_dao import ClienteDAO
from model.pessoa_fisica import PessoaFisica
from utils.validadores.validar_pessoa import ValidarPessoa as Validar


class PerfilController:
    """
    Controlador responsável pela visualização e atualização do perfil de um cliente.
    Permite consultar dados pessoais, editar campos mutáveis e alterar senha de acesso.
    """

    @staticmethod
    def obter_dados_perfil(documento: str) -> dict:
        """
        Retorna os dados do perfil do cliente com base em seu CPF/CNPJ.

        Args:
            documento (str): Documento do cliente.

        Returns:
            dict: Status da operação e dados ou mensagem de erro.
        """
        logger.info(f"Buscando dados de perfil para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {"status": "erro", "mensagem": "Cliente não encontrado."}

            pessoa = cliente.pessoa
            if not isinstance(pessoa, PessoaFisica):
                return {
                    "status": "erro",
                    "mensagem": "O usuário cadastrado não é uma Pessoa Física."
                }

            dados = {
                "nome": pessoa.get_nome(),
                "email": pessoa.get_email(),
                "numero_documento": pessoa.get_numero_documento(),
                "cep": pessoa.get_cep(),
                "numero_endereco": pessoa.get_numero_endereco(),
                "telefone": pessoa.get_telefone(),
                "data_nascimento": pessoa.get_data_nascimento().strftime("%d/%m/%Y")
            }

            return {"status": "sucesso", "dados": dados}

        except Exception as e:
            logger.error(f"Erro ao obter dados do perfil: {e}")
            return {"status": "erro", "mensagem": "Erro ao obter dados do perfil."}

    @staticmethod
    def atualizar_dados_perfil(documento: str, dados_atualizados: dict) -> dict:
        """
        Atualiza os dados pessoais de um cliente.

        Args:
            documento (str): Documento do cliente.
            dados_atualizados (dict): Dados a serem atualizados.

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
        logger.info(f"Iniciando atualização de dados do perfil para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {"status": "erro", "mensagem": "Cliente não encontrado."}

            pessoa = cliente.pessoa

            # Coleta os dados, mantendo os atuais como fallback
            nome = dados_atualizados.get("nome", pessoa.get_nome())
            email = dados_atualizados.get("email", pessoa.get_email())
            cep = dados_atualizados.get("cep", pessoa.get_cep())
            numero_endereco = dados_atualizados.get("numero_endereco", pessoa.get_numero_endereco())
            telefone = dados_atualizados.get("telefone", pessoa.get_telefone())

            # Validação dos campos
            erros = Validar._campos_comuns(nome, email, cep, numero_endereco, telefone)
            if erros:
                return {
                    "status": "erro",
                    "mensagem": "Erro(s) de validação:\n" + "\n".join(erros)
                }

            # Aplica alterações apenas nos campos modificados
            if "nome" in dados_atualizados:
                pessoa.set_nome(nome)
            if "email" in dados_atualizados:
                pessoa.set_email(email)
            if "cep" in dados_atualizados:
                pessoa.set_cep(cep)
            if "numero_endereco" in dados_atualizados:
                pessoa.set_numero_endereco(numero_endereco)
            if "telefone" in dados_atualizados:
                pessoa.set_telefone(telefone)

            # Persistência
            PessoaDAO().atualizar_objeto(pessoa)
            ClienteDAO().atualizar_objeto(cliente)

            return {"status": "sucesso", "mensagem": "Dados do perfil atualizados com sucesso."}

        except Exception as e:
            logger.error(f"Erro ao atualizar dados do perfil: {e}")
            return {"status": "erro", "mensagem": "Erro ao atualizar dados do perfil."}

    @staticmethod
    def alterar_senha(documento: str, senha_atual: str, nova_senha: str) -> dict:
        """
        Altera a senha de acesso de um cliente, validando a senha atual.

        Args:
            documento (str): Documento do cliente.
            senha_atual (str): Senha antiga informada pelo cliente.
            nova_senha (str): Nova senha desejada.

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
        logger.info(f"Solicitação de alteração de senha para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {"status": "erro", "mensagem": "Cliente não encontrado."}

            try:
                cliente.alterar_senha(senha_atual, nova_senha)
            except ValueError as e:
                return {"status": "erro", "mensagem": str(e)}

            ClienteDAO().atualizar_objeto(cliente)
            return {"status": "sucesso", "mensagem": "Senha alterada com sucesso."}

        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return {"status": "erro", "mensagem": "Erro inesperado ao tentar alterar senha."}