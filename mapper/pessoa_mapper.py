from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica
from utils.constantes import TIPO_PFISICA, TIPO_PJURIDICA

class PessoaMapper:
    @staticmethod
    def from_dict(dados: dict):
        """
        Cria uma instância de Pessoa (física ou jurídica) a partir de um dicionário de dados.

        Args:
            dados (dict): Dicionário com os dados da pessoa.

        Returns:
            Pessoa: Instância de PessoaFisica ou PessoaJuridica.

        Raises:
            ValueError: Se o tipo for desconhecido ou dados forem inválidos.
        """
        tipo = dados.get("tipo", "").strip().lower()

        if tipo == TIPO_PFISICA.lower():
            return PessoaFisica(
                nome=dados["nome"],
                email=dados["email"],
                numero_documento=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                data_nascimento=dados["data_nascimento"]
            )

        elif tipo == TIPO_PJURIDICA.lower():
            return PessoaJuridica(
                nome=dados["nome"],
                email=dados["email"],
                numero_documento=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                nome_fantasia=dados.get("nome_fantasia") or ""

            )

        else:
            raise ValueError(f"Tipo de pessoa desconhecido: {tipo}")

    @staticmethod
    def to_dict(pessoa):
        """
        Converte uma instância de PessoaFisica ou PessoaJuridica em um dicionário.
        """
        dados = {
            "nome": pessoa.get_nome(),
            "email": pessoa.get_email(),
            "numero_documento": pessoa.get_numero_documento(),
            "cep": pessoa.get_cep(),
            "numero_endereco": pessoa.get_numero_endereco(),
            "endereco": pessoa.get_endereco(),
            "telefone": pessoa.get_telefone(),
            "tipo": pessoa.get_tipo()
        }

        if pessoa.get_tipo() == TIPO_PFISICA:
            dados["data_nascimento"] = pessoa.get_data_nascimento().strftime("%d/%m/%Y")

        elif pessoa.get_tipo() == TIPO_PJURIDICA:
            nome_fantasia = pessoa.get_nome_fantasia()
            if nome_fantasia.strip():
                dados["nome_fantasia"] = nome_fantasia


        return dados