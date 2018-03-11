from abc import abstractmethod


class Fuente:
    """
    Clase abstracta que deben implementar todas las fuentes.
    """

    def __init__(self, fuente, tabla):
        self._fuente = fuente
        self._tabla = tabla
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
