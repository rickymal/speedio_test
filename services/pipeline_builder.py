
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class pipeline(BaseEstimator,TransformerMixin):
    def __init__(self, *args, **kwargs):
        pass
    
    def fit(self,data_to_fit, Y = None):
        return self
        pass
    
    def transform(self, data_to_transform, *args , **kwargs):
        raise NotImplementedError("precisa ser sobrescrito pelo decorador pipe_funtion")
        pass
    
    
    @classmethod
    def pipe_function(cls, function):
        
    
        new_instance = cls()
        new_instance.transform = function
        
        return new_instance
  
