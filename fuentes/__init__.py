from fuentes.aeat import AeatRenta
from fuentes.municipios import Municipios
from fuentes.ine import InePoblacion
from fuentes.sepe import SepeContratos, SepeEmpleo, SepeParo
from fuentes.mir import MirElecciones


# Lista de todas las fuentes disponibles
fuentes = [
    Municipios,
    AeatRenta,
    InePoblacion,
    SepeContratos,
    SepeEmpleo,
    SepeParo,
    MirElecciones
]
