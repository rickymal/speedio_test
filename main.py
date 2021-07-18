# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:18:56 2021

@author: Henrique Mauler
"""
import os
from sklearn.pipeline import Pipeline

from services import io_service as io
from services import transform_service  as transform
from services import check_type_service as check_type


from constants import PATH
from constants import COLLECTION_NAME
from constants import DATABASE_NAME
from constants import API_KEY
from constants import BATCH_SIZE
from constants import LIMIT_OF_DOCUMENT_TO_LOAD




# Obtém ou cria uma coleção no db definido como 'speedio'
# A varivável 'db' representa a coleção
db = io.get_collection_of_mongo_db(database_name = DATABASE_NAME,collection_name = COLLECTION_NAME)
db.delete_many({}) # para testes

# pipeline de transformação
pipe = Pipeline([
                ('converter para dicionario', transform.csv_to_dict_converter),
                ('checagem de tipo',check_type.check_types),
                ('converter datas', transform.data_converter),
                ('criando o atributo \'ano\'',transform.data_year_creator),
                ('converter cnae secundário para lista ', transform.list_cnae_converter),
                ('criando atributo \'todos os cnaes\'',transform.all_cnae_creator),
                ('limpeza dos dados', transform.filter_data),
                ],
            verbose = False)
        



# 'chunk' é equivalente ao 'batch size'
# em loop: extração dos dados -> processamento (pipeline) -> envio ao banco de dados
for i,chunk in enumerate(io.load_local_data(path = PATH ,batch_size= BATCH_SIZE, limit = LIMIT_OF_DOCUMENT_TO_LOAD), start = 1): # primeira etapa
    data_formated = pipe.fit_transform(chunk) #segunda etapa
    io.send_to_db(data_formated,db)  # terceira etapa
    print('enviando chunk',i,'para o banco',)
    

# quarta questão letra 'a'

pipe = Pipeline([
    ('obtendo porcentagem das empresas ativas',io.get_percentage_of_active_business),
    ('convertendo para formato dataframe',transform.convert_percentage_to_series),   
])

percentage = pipe.fit_transform(db)


# quarta questão letra 'b'

pipe = Pipeline([
    ('obtendo número de restaurantes abertos por ano',io.get_restaurant_opened_by_year),
    ('convertendo para formato dataframe',transform.convert_business_result_in_dataframe),   
])

number_of_restaurants_opened_by_year = pipe.fit_transform(db)


# quarta questão letra 'c'


pipe = Pipeline([
    ('obtendo número de negócios em um raio de 5km',io.get_numbers_of_business_by_radius),
    ('convertendo para serie',transform.convert_nof_business_in_serie),   
])


length_of_business_around =  pipe.fit_transform(API_KEY)

# quarta questão letra 'd'

pipe = Pipeline([
                ('agrupando os dados', transform.get_grouping),
                ('convertendo dados recebidos para um dataframe',transform.convert_cna_corr_document_to_dataframe),
                ('criando matriz de correlação', transform.create_corr_table),
                ],
                verbose = False)
            

correlations_between_cnaes = pipe.fit_transform(db)
# Quinta questão

from pandas import DataFrame as dataframe
from pandas import Series as series




was_exported = io.export_answers_to_excel({
    'quarta questão letra a' : percentage,
    'quarta questão letra b' : number_of_restaurants_opened_by_year,
    'quarta questão letra c' : length_of_business_around,
    'quarta questão letra d' : correlations_between_cnaes,
}, output_name = "answers")

if was_exported:
    print('[log] programa finalizado com sucesso, o resultado pode ser visto na pasta exports')

# não precisava
#is_exported = io.export_mongo_data_to_excel(db, output_name = 'all_data_in_db')

# https://exceptionshub.com/python-append-dataframe-to-excel-with-pandas.html

 