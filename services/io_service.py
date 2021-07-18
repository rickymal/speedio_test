

from services.pipeline_builder import pipeline
from pymongo import MongoClient
import pymongo
import requests
import requests
import csv
import time
from pandas import ExcelWriter
import os
import sys


sys.path.append('..')
from constants import EXPORTS
# print


def get_collection_of_mongo_db(database_name, collection_name):
    client = MongoClient()
    return client[database_name][collection_name]


def load_local_data(folder, batch_size: int = 10000, limit: int = None):
    append_limit = 0
    if (limit is not None) and (limit < batch_size):
        raise Exception("o tamanho do lote é maior que o limite definido")

    for data_as_csv_name in os.listdir(folder):
        with open(os.path.join(folder, data_as_csv_name), 'r') as file:
            raw_chunk = list()
            ind = 0

            iter_ = iter(enumerate(file, start=1))
            while True:
                try:

                    # Lendo uma linha (ind: número de documentos lido do arquivo), (raw_document : o conteúdo em si)
                    ind, raw_document = next(iter_)

                    # ultrapassou o limite definido?
                    if limit is not None and (ind + append_limit) >= limit:
                        break

                    raw_chunk.append(raw_document)

                    # aqui deveria ser (indice + append_limit) em vez de (ind)
                    # para retornar sempre o batch no mesmo tamanho, mas isto não interfere no programa
                    if (ind % batch_size) == 0:
                        yield raw_chunk
                        raw_chunk = list()

                except Exception as ext:
                    exc_type, _, _ = sys.exc_info()

                    if exc_type.__name__ == 'StopIteration':
                        # não há mais linhas para lerem lidas no arquivo
                        break
                    elif exc_type.__name__ == 'UnicodeDecodeError':
                        # alguns dados não são lidos por um erro de 'codec', byte 8f não reconhecido, pode ser algum encoding errado
                        # ignorado
                        continue
                    else:
                        raise
                    pass
                pass
            if len(raw_chunk) > 0:
                yield raw_chunk

            append_limit += ind
            break

            pass
        pass
    return


def send_to_db(chunk: list[dict], db):
    db.insert_many(chunk)
    return True


@pipeline.pipe_function
def get_percentage_of_active_business(db):
    all_occurrences = db.count_documents({})
    if all_occurrences == 0:
        return 0.0
    actives = db.count_documents({'situação cadastral': "02"})
    percentage = (actives * 100 / all_occurrences)
    return percentage


@pipeline.pipe_function
def get_restaurant_opened_by_year(db):
    result = db.aggregate([
        {
            '$match': {
                'cnae fiscal principal': {'$regex': '^561'}
            }
        },
        {"$group": {
            "_id": '$ano de criação',
            "quantidades abertas": {"$count": {}},
        },
        },
    ])

    lof_opened_business = []
    for r in result:
        lof_opened_business.append({
            'ano': r['_id'],
            'quantidade': r['quantidades abertas']
        })
        pass
    return lof_opened_business


@pipeline.pipe_function
def get_numbers_of_business_by_radius(api_key):

    # Obtido no Google Maps
    cep_reference_latitude = -23.56747
    cep_reference_longitude = -46.65692
    cep_reference_address = 'Afonso Pena, São José dos Pinhais - PR, 83050-060, Brazil'

    location_as_query_string_format = f'{cep_reference_latitude},{cep_reference_longitude}'

    npt = ""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    result_content = []
    while True:
        payload = {"key": api_key,
                   "location": location_as_query_string_format,
                   "radius": "5000",
                   "pagetoken": npt
                   }

        response = requests.get(url=url,
                                params=payload, timeout=5)

        data = response.json()

        if response.status_code != 200:
            raise Exception("resposta do servidor diferente de 200")

        for value in data['results']:

            # não é um negócio?
            if 'business_status' not in value:
                continue

            result_content.append({
                'status': value['business_status'],
                'name': value['name'],
            })

        # há ainda conteudo para ser buscado na página? se não...
        if 'next_page_token' not in data or data['next_page_token'] == None:
            break

        npt = data['next_page_token']

        # existe um delay entre o token fornecido pelo google maps e a capacidade de seu uso (fonte: documentação)
        time.sleep(2)

    length_of_business_around = len(result_content)
    return length_of_business_around

# não utilizado


def export_mongo_data_to_excel(db, output_name):
    columns_lbl = db.find_one().keys()
    db_all = db.find({})
    try:
        with open(os.path.join(EXPORTS, f'{output_name}.xlsx'), 'w', newline='') as xlsfile:
            spamwriter = csv.writer(xlsfile, dialect='excel')
            spamwriter.writerow(columns_lbl)

            for r in db_all:
                spamwriter.writerow(str(r) for r in r.values())
                pass
            pass
        return True

    except:
        return False


def export_answers_to_excel(data: dict, output_name: str):
    try:
        with ExcelWriter(os.path.join(EXPORTS, f'{output_name}.xlsx'), engine='openpyxl', mode='w') as writer:
            for sheet_name, answer in data.items():
                answer.to_excel(writer, sheet_name=sheet_name)
                pass
            pass
        return True
    except:
        return False
