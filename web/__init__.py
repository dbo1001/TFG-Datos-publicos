from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo


# Servidor Flask
app = Flask(__name__)

# Plugin Bootstrap
Bootstrap(app)

mongo = PyMongo(app)


# Importa las vistas
import web.views
