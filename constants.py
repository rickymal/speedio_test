import os


# variáveis globais para isso
COLUMNS_LABEL = [
    'CNPJ básico',
    'cnpj ordem',
    'cnpj dv',
    'identificador matriz/filial',
    'nome fantasia',
    'situação cadastral',
    'data da situação cadastral',
    'motivo da situação cadastral',
    'nome da cidade no exterior',
    'pais',
    'data de inicio da atividade',
    'cnae fiscal principal',
    'cnae fiscal secundário',
    'tipo de logradouro',
    'logradouro',
    'número',
    'complemento',
    'bairro',
    'cep',
    'uf',
    'município',
    'ddd 1',
    'telefone 1',
    'ddd 2',
    'telefone 2',
    'ddd do fax',
    'fax',
    'correio eletrônico',
    'situação especial',
    'data da situação especial']

PATH = os.path.join('data','K3241.K03200Y0.D10612.ESTABELE')
COLLECTION_NAME = 'receita federal db'
DATABASE_NAME = 'speedio'
API_KEY = "AIzaSyC-14F94fZv_zJVE53S6xXaM15TIEFwi1g" # configurada para um limite específico de requisições
BATCH_SIZE = 1000
LIMIT_OF_DOCUMENT_TO_LOAD = 10000