import os


class Config(object):
    """
    Configuración de la aplicación
    """
    DEBUG = True
    SECRET_KEY = 'r^Ic3@LoDbhnQ3kQr5t1vP6XZJdZ!!sc'
    # MongoDB
    MONGO_HOST = os.environ.get('DATA_DB_HOST', 'localhost')
    MONGO_PORT = int(os.environ.get('DATA_DB_PORT', 27017))
    MONGO_DBNAME = os.environ.get('DATA_DB_NAME', 'datos')
    MONGO_USERNAME = os.environ.get('DATA_DB_USER', None)
    MONGO_PASSWORD = os.environ.get('DATA_DB_PASS', None)
