
from .pipeline_builder import pipeline
from pandas import DataFrame as dataframe
from pandas import Series as series
from datetime import datetime
import requests
import re
import csv
from numpy import nan
from numpy import diag
from pandas import concat

import sys

sys.path.append('..')
from constants import COLUMNS_LABEL

# print
@pipeline.pipe_function  
def csv_to_dict_converter(chunk : list[str],):
    
    try:
        
        #lof : list of
        lof_data = list()
        for ind, raw_document in enumerate(chunk):
            
            """
            O Layout presente no site afirmar que a informação é separada 
            pelo caractere ';'. Todavia alguns documentos apresentam
            no atributo 'endereço' este caractere como não separador. 
            Levando este fator em consideração observei que utilizar regex
            (expressão regular) para separar o conteudo que esta entre aspas
            causa menos perda de informação.
            
            """
            
            document_as_list = re.findall('"([^"]*)"', raw_document)      
            document_converted_to_dict  = {
                key : value for key,value in zip(COLUMNS_LABEL,document_as_list)
                }
            
            lof_data.append(document_converted_to_dict)

        return lof_data
    except:
        raise Exception("erro no método 'csv_to_dict_converter' ")
    pass


@pipeline.pipe_function
def data_converter(chunk : list[dict]):
    try:
        
        #lof : list of
        lof_data = list()
        for ind, data in enumerate(chunk):
            vv = data['data de inicio da atividade']
            if isinstance(vv,str):
                date_formated = datetime.strptime(vv,"%Y%m%d")
                data['data de inicio da atividade'] = date_formated
            elif isinstance(vv,datetime):
                pass
            else:
                raise Exception("Formato não reconhecido")
            lof_data.append(data)
            
        return lof_data
    except:
        raise Exception("erro no método 'data_converter' ")
    pass

@pipeline.pipe_function
def data_year_creator(chunk : list[dict]):
    try:
        
        #lof : list of
        lof_data = list()
        for data in chunk:
            vv = data['data de inicio da atividade']
            
            data['ano de criação'] = vv.year
            lof_data.append(data)
            
        return lof_data 
    except:
        raise Exception("erro no método 'data_year_creator' ")
    pass

@pipeline.pipe_function    
def list_cnae_converter(chunk : list[dict]):
    try:
        
        #lof : list of
        lof_data = list()
        for data in chunk:
            cnae_sec = data['cnae fiscal secundário']
            cnae_sec_splitted = [x.strip() for x in cnae_sec.split(',') if x.strip().isdigit()]
            data['cnae fiscal secundário'] = cnae_sec_splitted
            lof_data.append(data)
            
        return lof_data 
    except:
        raise Exception("erro no método 'list_cnae_converter' ")

@pipeline.pipe_function
def all_cnae_creator(chunk : list[dict]):
    try:
        
        #lof : list of
        lof_data = list()
        for data in chunk:
            vv = data['cnae fiscal secundário']
            pp = data['cnae fiscal principal']
            vv.append(pp)
            
            data['todos os cnaes'] = vv
            lof_data.append(data)
            
        return lof_data 
    except:
        raise Exception("erro no método 'all_cnae_creator' ")
    pass
    

@pipeline.pipe_function
def convert_percentage_to_series(data):
    return series({'porcentagem das empresas ativas atualmente' : data})

@pipeline.pipe_function
def convert_nof_business_in_serie(data):
    return series({'número de negócios em um raio de 5km' : data})

@pipeline.pipe_function
def filter_data(chunk : list[dict]):
    try:
        lof = []
        for data in chunk:
            content_hashed_filted = {
            'situação cadastral' : data['situação cadastral'],
            'cep' : data['cep'],
            'data de inicio da atividade' : data['data de inicio da atividade'],
            'cnae fiscal principal' : data['cnae fiscal principal'],
            'ano de criação' : data['ano de criação'],
            'todos os cnaes' : data['todos os cnaes']
            }
            
            
            lof.append(content_hashed_filted)
            
        return lof 
    except:
        raise Exception("erro no método 'extract_unused_data' ")



@pipeline.pipe_function
def get_grouping(db):
    for_grouping  = db.aggregate([
        {
         "$unwind" : "$todos os cnaes"
        },
        { "$group": {
            "_id": {
                'primary' : '$cnae fiscal principal',
                'secondary' : '$todos os cnaes'
                
                },
            "quantidades": { "$count": {} },
            },
        },
    ])

    # operação bloqueante (resolver se tiver tempo: trabalhar em lotes)
    lof = []
    for r in for_grouping:
        lof.append(r)
    return lof


@pipeline.pipe_function
def convert_cna_corr_document_to_dataframe(data : list[dict]):
    
    qnt = dataframe.from_dict({
        'cnae principal' : x['_id']['primary'],
        'cnae secundário' : x['_id']['secondary'],
        'quantidades' : x['quantidades'],
        } for x in data)
        
    
    return qnt

@pipeline.pipe_function
def convert_business_result_in_dataframe(data):
    return dataframe(data)



@pipeline.pipe_function
def create_corr_table(data : dataframe):
    pivot_qnt = data.pivot(index = 'cnae principal',
                          columns = 'cnae secundário',
                          values = 'quantidades').replace(nan,0.0)
    
    
    # a primeira máscara filtra códigos que aparecem em ambos os cnaes
    
    mask_cnae_prim = pivot_qnt.index.values
    pair_table = pivot_qnt.loc[:,mask_cnae_prim]
    
    # a segunda máscara filtra todos os cnae's secundários que não se apresentam no cnae primário
    mask_cnae_sec = ~pivot_qnt.columns.isin(pivot_qnt.index)
    
    
    """
    A razão para eu ter separado em duas máscaras é puramente estético
    pois dessa forma pode-se observar na diagonal da primeira parte
    da tabela os valores 1 representando 100 % da ocorrência. Algo
    que não iria acontecer caso as máscaras não fossem feitas visto que
    a posição dos cnaes nas linhas e colunas da tabela são aleatórias
    """
    no_pair_table = pivot_qnt.loc[:,mask_cnae_sec]
    complete_data = series(diag(pair_table),index = pair_table.index)
    
    
    #  keys = ["códigos presentes em ambos os cnae's","códigos presentes apenas no cnae secundário"]
    
    all_data = concat([pair_table,no_pair_table],axis = 1)
    percentage_of_pair = all_data.apply(lambda x : x  / complete_data).round(decimals = 2)
    
    
    return percentage_of_pair

