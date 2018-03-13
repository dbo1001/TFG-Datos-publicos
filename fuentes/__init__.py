from fuentes.aeat import AeatRenta
from fuentes.codigos import CodigosMunicipios
from fuentes.ine import InePoblacion
from fuentes.sepe import SepeContratos, SepeEmpleo, SepeParo


# Lista de todas las fuentes disponibles
fuentes = [
    CodigosMunicipios,
    AeatRenta,
    InePoblacion,
    SepeContratos, SepeEmpleo, SepeParo
]
