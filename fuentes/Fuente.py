from abc import abstractmethod
from functools import wraps
import pandas as pd


class Fuente:
    """
    Clase abstracta que deben implementar todas las fuentes.
    """

    def __init__(self, fuente, tabla, descripcion=''):
        self._fuente = fuente
        self._tabla = tabla
        self._descripcion = descripcion
        super().__init__()

    @abstractmethod
    def carga(self):
        """
        Devuelve un dataframe después de descargar los datos
        """
        pass

    def coleccion(self):
        """
        Devuelve el nombre de la colección
        """
        return '_'.join([self._fuente, self._tabla])

    @abstractmethod
    def descripcion(self):
        """
        Devuelve la descripción de la fuente
        """
        return self._descripcion


def to_numeric(f):
    """
    Decorador que convierte todas las columnas
    que sean números (como strings) a números.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs).apply(pd.to_numeric, errors='ignore')
    return wrapper


def rename(columnas):
    """
    Decorador que renombra los nombres de las columnas.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs).rename(columns=columnas)
        return wrapper
    return decorator
