from .pipeline_builder import pipeline
from datetime import datetime

@pipeline.pipe_function
def check_types(chunk : list[dict]):
    try:
        
        #lof : list of
        lof_data = list()
        for ind, data in enumerate(chunk):
            
            # checando cnpj básico
            t1 = data['CNPJ básico'].isnumeric() and len(data['CNPJ básico']) == 8
            
            # checando o formato das datas
            try:
                date_formated = datetime.strptime(data['data de inicio da atividade'],"%Y%m%d")
                
                # alguns dados estão com o ano acima do atual
                t2 = date_formated.year <= datetime.now().year
            except:
                t2 = False
                                
            t3 = data['situação cadastral'].isnumeric()
            t4 = data['cnae fiscal principal'].isnumeric() and len(data['cnae fiscal principal']) == 7
            
            
            # Se o dado não está com a formatação, descarta-lo
            if all([t1,t2,t3,t4]):
                lof_data.append(data)
            else:
                continue

        return lof_data
    except:
        raise Exception("erro no método 'data_converter' ")
        
    pass
