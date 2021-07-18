from services.pipeline_builder import pipeline
from pymongo import MongoClient
import pymongo
import requests
import requests
import csv
import time
from pandas import ExcelWriter
import os
def get_collection_of_mongo_db(database_name, collection_name):
    # CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"
    client = MongoClient()
    return client[database_name][collection_name]

def load_local_data(path,batch_size : int = 10000, limit : int = None):
    PATH = path
    with open(PATH,'r') as file:
        try:
            raw_chunk = list()
            for ind, raw_document in enumerate(file,start = 1):
                raw_chunk.append(raw_document)
                if (ind % batch_size) == 0:
                    yield raw_chunk
                    raw_chunk = list()
                    
                    
                if limit is not None and ind > limit:
                    break
            if len(raw_chunk) > 0:
                yield raw_chunk
                return 
        except IOError:
            print("[ERROR]",IOError.message)
            raise IOError("Error")
    return

def send_to_db(chunk : list[dict], db):
    db.insert_many(chunk)
    return True



@pipeline.pipe_function
def get_percentage_of_active_business(db):
    
    all_occurrences = db.count_documents({})
    
    # obtendo as ocorrências com situação cadastral 02
    actives = db.count_documents({'situação cadastral' : "02"})
    percentage = (actives * 100 / all_occurrences)
    print(f'percentage: {percentage:2f} %' )    
    return percentage


@pipeline.pipe_function
def get_restaurant_opened_by_year(db):
    result = db.aggregate([
        {
         '$match' : {
             'cnae fiscal principal' : {'$regex' : '^561'}
             }
        },
        { "$group": {
            "_id": '$ano de criação',
            "quantidades abertas": { "$count": {} },
            },
        },
    ])
    
    lof_opened_business = []
    for r in result:
        lof_opened_business.append({
            'ano' : r['_id'],
            'quantidade' : r['quantidades abertas']
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
        payload = {"key":api_key,
                   "location": location_as_query_string_format,
                   "radius" : "5000",
                   "pagetoken" : npt
                   }
    
        response = requests.get(url=url,
                            params=payload,timeout=5) 
            
        data = response.json()
        
        if response.status_code != 200:
            break
        
        for value in data['results']:    
            
            # é um negócio?
            if 'business_status' not in value:
                continue
                
            result_content.append({
                'status' : value['business_status'],
                'name' : value['name'],
                })
    
        # há ainda conteudo para ser buscado na página? se não...
        if 'next_page_token' not in data or data['next_page_token'] == None:
            break
        
        npt = data['next_page_token']
        time.sleep(2)
        
        
    length_of_business_around = len(result_content)
    return length_of_business_around

def export_mongo_data_to_excel(db, output_name):
    columns_lbl = db.find_one().keys()
    db_all = db.find({})
    try:
        
        with open(os.path.join('exports',f'{output_name}.xlsx'), 'w', newline='') as xlsfile:
            spamwriter = csv.writer(xlsfile, dialect = 'excel')
            spamwriter.writerow(columns_lbl)
            
            for r in db_all:
                spamwriter.writerow(str(r) for r in r.values())
                
                pass
            pass
        return True
    
    except:
        return False
    

def export_answers_to_excel(data : dict,output_name : str):
    try:
        with ExcelWriter(os.path.join('exports',f'{output_name}.xlsx'),engine = 'openpyxl', mode = 'w') as writer:
            for sheet_name, answer in data.items():
                answer.to_excel(writer,sheet_name = sheet_name)
                pass
            pass
        return True
    except:
        return False

