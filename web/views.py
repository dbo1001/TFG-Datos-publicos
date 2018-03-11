from flask import render_template
from web import app, mongo
import pandas as pd


@app.route('/')
def index():
    """
    Página de inicio
    """
    return render_template('index.html')
