# Trabalho de IA - buscas
# Gabrielly Christina Moreira; Marcos André Trajano da Silva Júnior e Yasmin de Oliveira Bonet
# rota das urnas no Amazonas

import time

import buscas
import mapa

TODOS = ["estrada", "estrada ruim", "barco", "aviao"]
SEM_AVIAO = ["estrada", "estrada ruim", "barco"]


def formatar_horas(h):
    # 37.5 -> 37h30
    horas = int(h)
    minutos = round((h - horas) * 60)
    if minutos == 60:
        horas += 1
        minutos = 0
    return f"{horas}h{minutos:02d}"


def caminho_com_transporte(caminho, tipos):
    texto = caminho[0]
    for i in range(len(caminho) - 1):
        tipo = mapa.tipo_do_trecho(caminho[i], caminho[i + 1], tipos)
        texto += f" -({tipo})-> {caminho[i + 1]}"
    return texto


def rodar_algoritmo(nome, funcao, grafo, *args):
    inicio = time.perf_counter()
    caminho, expandidos = funcao(grafo, *args)
    tempo_ms = (time.perf_counter() - inicio) * 1000
    return {
        "nome": nome,
        "caminho": caminho,
        "horas": buscas.custo_do_caminho(grafo, caminho),
        "expandidos": expandidos,
        "tempo": tempo_ms,
    }


def comparar(origem, destino, tipos=TODOS, limite_dls=3):
    grafo = mapa.montar_grafo(tipos)
    h = mapa.criar_heuristica(destino, tipos)

    resultados = [
        rodar_algoritmo("BFS", buscas.bfs, grafo, origem, destino),
        rodar_algoritmo("DFS", buscas.dfs, grafo, origem, destino),
        rodar_algoritmo(f"DLS (lim={limite_dls})", buscas.dls, grafo, origem, destino, limite_dls),
        rodar_algoritmo("IDS", buscas.ids, grafo, origem, destino),
        rodar_algoritmo("UCS", buscas.ucs, grafo, origem, destino),
        rodar_algoritmo("Gulosa", buscas.gulosa, grafo, origem, destino, h),
        rodar_algoritmo("A*", buscas.a_estrela, grafo, origem, destino, h),
    ]

    print()
    print(f"=== Levar urnas de {origem} ate {destino} ===")
    print(f"transportes: {', '.join(tipos)}")
    print(f"distancia em linha reta: {mapa.distancia_reta(origem, destino):.0f} km")
    print()
    print(f"{'Algoritmo':<13}{'tempo viagem':>13}{'trechos':>9}{'expand.':>9}{'cpu(ms)':>9}   caminho")
    print("-" * 120)

    for r in resultados:
        if r["caminho"] is None:
            print(f"{r['nome']:<13}{'-':>13}{'-':>9}{r['expandidos']:>9}{r['tempo']:>9.3f}   NAO ENCONTROU")
        else:
            print(f"{r['nome']:<13}{formatar_horas(r['horas']):>13}{len(r['caminho']) - 1:>9}"
                  f"{r['expandidos']:>9}{r['tempo']:>9.3f}   "
                  + caminho_com_transporte(r["caminho"], tipos))

    # A* e UCS tem que dar o mesmo tempo
    ucs, a = resultados[4]["horas"], resultados[6]["horas"]
    if ucs is not None and abs(ucs - a) > 0.001:
        print("\n!! ATENCAO: A* e UCS deram tempos diferentes, tem algo errado na heuristica")

    return resultados


def escolher_cidade(texto):
    cidades = list(mapa.coordenadas.keys())
    for i, c in enumerate(cidades):
        print(f"  {i:2d} - {c}")
    while True:
        op = input(texto)
        if op.isdigit() and 0 <= int(op) < len(cidades):
            return cidades[int(op)]
        print("Opcao invalida, tenta de novo.")


def menu_rota():
    origem = escolher_cidade("Numero da cidade de ORIGEM (o TRE fica em Manaus): ")
    destino = escolher_cidade("Numero do municipio de DESTINO: ")
    aviao = input("Tem aviao disponivel? (s/n): ").strip().lower()
    tipos = SEM_AVIAO if aviao == "n" else TODOS
    lim = input("Limite da DLS (enter = 3): ")
    lim = int(lim) if lim.isdigit() else 3
    comparar(origem, destino, tipos, lim)


def exemplos_prontos():
    # exemplos que usei no relatorio
    comparar("Manaus", "Eirunepe", TODOS)
    comparar("Manaus", "Coari", TODOS)
    comparar("Manaus", "Labrea", SEM_AVIAO)
    comparar("Manaus", "Sao Gabriel da Cachoeira", SEM_AVIAO, limite_dls=5)

    print("\n=== Efeito do limite na DLS (Manaus -> Eirunepe, com aviao) ===")
    grafo = mapa.montar_grafo(TODOS)
    for lim in range(0, 8):
        caminho, exp = buscas.dls(grafo, "Manaus", "Eirunepe", lim)
        if caminho:
            print(f"limite {lim}: achou, {formatar_horas(buscas.custo_do_caminho(grafo, caminho))}, "
                  f"{exp} nos expandidos")
        else:
            print(f"limite {lim}: nao achou ({exp} nos expandidos)")


def main():
    problemas = mapa.conferir_distancias()
    if problemas:
        print("Aviso: trechos menores que a linha reta (heuristica pode nao ser admissivel):")
        for p in problemas:
            print("  ", p)

    while True:
        print("\n========== TRABALHO - BUSCAS NAS ELEICOES ==========")
        print("1 - Rota das urnas ate um municipio (compara todos os algoritmos)")
        print("2 - Rodar exemplos prontos")
        print("0 - Sair")
        op = input("Opcao: ").strip()

        if op == "1":
            menu_rota()
        elif op == "2":
            exemplos_prontos()
        elif op == "0":
            print("Tchau!")
            break
        else:
            print("Opcao invalida")


if __name__ == "__main__":
    main()
