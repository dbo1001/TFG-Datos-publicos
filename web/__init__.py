from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from config import Config


# Servidor Flask
app = Flask(__name__)

# Configura con el archivo de configuración
app.config.from_object(Config)

# Plugin Bootstrap
Bootstrap(app)

mongo = PyMongo(app)

# Importa las vistas
import web.views
