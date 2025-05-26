from dao.cliente_dao import ClienteDAO
from model.pessoa_fisica import PessoaFisica
from utils.logger import logger

class PerfilController:
    @staticmethod
    def obter_dados_perfil(documento: str) -> dict:
        logger.info(f"Buscando dados de perfil para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {"status": "erro", "mensagem": "Cliente não encontrado."}

            pessoa = cliente.pessoa

            dados = {
                "nome": pessoa.get_nome(),
                "documento_formatado": (
                    f"CPF: {pessoa.get_numero_documento()}" if pessoa.get_tipo() == "fisica"
                    else f"CNPJ: {pessoa.get_numero_documento()}"
                ),
                "email": pessoa.get_email(),
                "cep": pessoa.get_cep(),
                "numero_endereco": pessoa.get_numero_endereco(),
                "telefone": pessoa.get_telefone(),
                "endereco": pessoa.get_endereco(),
                "contas": cliente.contas,
                "data_nascimento": pessoa.get_data_nascimento().strftime("%d/%m/%Y")
                    if isinstance(pessoa, PessoaFisica) else None
            }

            return {"status": "sucesso", "dados": dados}

        except Exception as e:
            logger.error(f"Erro ao obter dados do perfil: {e}")
            return {"status": "erro", "mensagem": "Erro ao obter dados do perfil."}
