import os


class Config(object):
    """
    Configuración de la aplicación
    """
    DEBUG = True
    SECRET_KEY = 'r^Ic3@LoDbhnQ3kQr5t1vP6XZJdZ!!sc'
    # MongoDB
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'datos')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME', None)
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', None)
