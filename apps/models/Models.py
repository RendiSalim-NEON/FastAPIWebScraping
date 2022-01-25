from apps.models import Model 

class Carsome(Model):
    __table__ = 'CarsomeScraping'
    __primary_key__ = 'ID'
    __timestamps__ = False