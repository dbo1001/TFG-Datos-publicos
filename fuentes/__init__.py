from fuentes.aeat import AeatRenta
from fuentes.municipios import Municipios
from fuentes.ine import InePoblacion
from fuentes.sepe import SepeContratos, SepeEmpleo, SepeParo
from fuentes.mir import MirElecciones, MirEleccionesGenerales
from fuentes.irpf2015 import Irpf2015
from fuentes.epa import Epa
from fuentes.turismo import Turismo
from fuentes.sklearn import Sklearn


# Lista de todas las fuentes disponibles
fuentes = [
    Municipios,
    Irpf2015,
    Epa,
    AeatRenta,
    InePoblacion,
    SepeContratos,
    SepeEmpleo,
    SepeParo,
    MirElecciones,
    MirEleccionesGenerales,
    Turismo,
    Sklearn
]
