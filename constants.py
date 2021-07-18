# variáveis globais para isso

# layout das colunas
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


#nome do banco de dados
DATABASE_NAME = 'speedio'

# nome da coleção 
COLLECTION_NAME = 'receita federal db'

# configurada para um limite específico de requisições
API_KEY = "AIzaSyC-14F94fZv_zJVE53S6xXaM15TIEFwi1g"

# quantidade de documentos que serão carregados por vez em memória
BATCH_SIZE = 1000

# número máximo de documentos que serão carregados (utilizado apenas para desenvolvimento). Valor None para ilimitado
LIMIT_OF_DOCUMENT_TO_LOAD = 30000
LIMIT_OF_DOCUMENT_TO_LOAD = None

# pasta que contém os arquivos baixados da receita federal
FOLDER = 'data'

# pasta onde será colocada a saída 
EXPORTS = 'exports'
