from funcoes import fun_qtd_apoios
from funcoes import momento_inercia
from funcoes import caracteristica_material
from funcoes import qtd_forcas
from funcoes import geracao_graficos
from funcoes import analise_viga

fun_qtd_apoios()
Ix, Iy = momento_inercia()
E, G = caracteristica_material()
analise_viga(Ix ,E)
qtd_forcas()
geracao_graficos()