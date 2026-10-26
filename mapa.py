# mapa das cidades do Amazonas pra levar as urnas
# as distancias sao aproximadas, peguei olhando no mapa

import math

coordenadas = {
    "Manaus":                    (-3.12, -60.02),
    "Manacapuru":                (-3.29, -60.62),
    "Novo Airao":                (-2.62, -60.94),
    "Presidente Figueiredo":     (-2.03, -60.02),
    "Itacoatiara":               (-3.14, -58.44),
    "Maues":                     (-3.38, -57.72),
    "Parintins":                 (-2.63, -56.74),
    "Borba":                     (-4.39, -59.59),
    "Manicore":                  (-5.81, -61.30),
    "Humaita":                   (-7.51, -63.02),
    "Labrea":                    (-7.26, -64.80),
    "Coari":                     (-4.08, -63.14),
    "Tefe":                      (-3.35, -64.71),
    "Fonte Boa":                 (-2.51, -66.09),
    "Carauari":                  (-4.88, -66.90),
    "Eirunepe":                  (-6.66, -69.87),
    "Tabatinga":                 (-4.25, -69.94),
    "Benjamin Constant":         (-4.38, -70.03),
    "Barcelos":                  (-0.97, -62.92),
    "Santa Isabel do Rio Negro": (-0.41, -65.02),
    "Sao Gabriel da Cachoeira":  (-0.13, -67.09),
}

# velocidade media em km/h
velocidades = {
    "estrada": 60,
    "estrada ruim": 15,   # BR-319 na chuva
    "barco": 18,
    "aviao": 350,
}
TEMPO_EMBARQUE_AVIAO = 1.0  # 1h pra carregar/descarregar o aviao

# (cidade, cidade, transporte, km)
trechos = [
    # estradas
    ("Manaus", "Manacapuru", "estrada", 85),
    ("Manaus", "Presidente Figueiredo", "estrada", 125),
    ("Manaus", "Itacoatiara", "estrada", 270),
    ("Manacapuru", "Novo Airao", "estrada", 115),
    ("Manaus", "Humaita", "estrada ruim", 680),
    ("Humaita", "Labrea", "estrada", 210),

    # rios
    ("Manaus", "Itacoatiara", "barco", 200),
    ("Itacoatiara", "Parintins", "barco", 240),
    ("Itacoatiara", "Maues", "barco", 180),
    ("Parintins", "Maues", "barco", 200),
    ("Manaus", "Borba", "barco", 220),
    ("Itacoatiara", "Borba", "barco", 200),
    ("Borba", "Manicore", "barco", 260),
    ("Manicore", "Humaita", "barco", 300),
    ("Manaus", "Coari", "barco", 420),
    ("Manacapuru", "Coari", "barco", 330),
    ("Manacapuru", "Labrea", "barco", 1100),  # pelo rio Purus
    ("Coari", "Tefe", "barco", 230),
    ("Tefe", "Fonte Boa", "barco", 260),
    ("Fonte Boa", "Tabatinga", "barco", 600),
    ("Tabatinga", "Benjamin Constant", "barco", 25),
    ("Tefe", "Carauari", "barco", 520),
    ("Fonte Boa", "Carauari", "barco", 420),
    ("Carauari", "Eirunepe", "barco", 650),
    ("Manaus", "Novo Airao", "barco", 190),
    ("Novo Airao", "Barcelos", "barco", 330),
    ("Barcelos", "Santa Isabel do Rio Negro", "barco", 280),
    ("Santa Isabel do Rio Negro", "Sao Gabriel da Cachoeira", "barco", 300),

    # voos
    ("Manaus", "Parintins", "aviao", 375),
    ("Manaus", "Tefe", "aviao", 525),
    ("Manaus", "Tabatinga", "aviao", 1110),
    ("Manaus", "Sao Gabriel da Cachoeira", "aviao", 860),
    ("Manaus", "Humaita", "aviao", 600),
    ("Tefe", "Eirunepe", "aviao", 690),
]


def tempo_do_trecho(tipo, km):
    horas = km / velocidades[tipo]
    if tipo == "aviao":
        horas += TEMPO_EMBARQUE_AVIAO
    return round(horas, 2)


def montar_grafo(tipos_permitidos=None):
    # grafo[cidade][vizinho] = horas
    # se tiver dois jeitos de ir entre as mesmas cidades fica o mais rapido
    if tipos_permitidos is None:
        tipos_permitidos = list(velocidades.keys())

    grafo = {cidade: {} for cidade in coordenadas}
    for a, b, tipo, km in trechos:
        if tipo not in tipos_permitidos:
            continue
        horas = tempo_do_trecho(tipo, km)
        if b not in grafo[a] or horas < grafo[a][b]:
            grafo[a][b] = horas
            grafo[b][a] = horas
    return grafo


def tipo_do_trecho(a, b, tipos_permitidos=None):
    # so pra mostrar na tela qual transporte foi usado
    if tipos_permitidos is None:
        tipos_permitidos = list(velocidades.keys())
    melhor = None
    for x, y, tipo, km in trechos:
        if {x, y} == {a, b} and tipo in tipos_permitidos:
            h = tempo_do_trecho(tipo, km)
            if melhor is None or h < melhor[1]:
                melhor = (tipo, h)
    return melhor[0]


def distancia_reta(cidade1, cidade2):
    # haversine, distancia em linha reta em km
    lat1, lon1 = coordenadas[cidade1]
    lat2, lon2 = coordenadas[cidade2]
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def criar_heuristica(destino, tipos_permitidos=None):
    # h = linha reta / velocidade do transporte mais rapido
    # nunca passa do tempo real, entao e admissivel
    if tipos_permitidos is None:
        tipos_permitidos = list(velocidades.keys())
    vmax = max(velocidades[t] for t in tipos_permitidos)

    def h(cidade):
        return distancia_reta(cidade, destino) / vmax
    return h


def conferir_distancias():
    # se algum trecho for menor que a linha reta tem dado errado
    problemas = []
    for a, b, tipo, km in trechos:
        reta = distancia_reta(a, b)
        if km < reta:
            problemas.append((a, b, tipo, km, round(reta)))
    return problemas
