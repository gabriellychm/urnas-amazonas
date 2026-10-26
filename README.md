# Trabalho de IA - Algoritmos de Busca

Gabrielly Christina Moreira, Marcos André Trajano da Silva Júnior e Yasmin de Oliveira Bonet

## Tema

Como é ano de eleição, escolhemos o problema de levar as urnas eletrônicas do TRE em Manaus até as cidades do interior do Amazonas. Onde muitas cidades não têm estrada, então a urna vai de barco ou de avião. O programa procura a rota mais rápida (em horas) usando os algoritmos vistos em aula.

Bibliotecas usadas: `collections.deque`, `heapq`, `math` e `time`.

## Arquivos

- `mapa.py`: cidades, trechos (estrada, barco, avião) e a heurística
- `buscas.py`: BFS, DFS, DLS, IDS, UCS, Gulosa e A*
- `main.py`: menu e comparação dos algoritmos

## Como rodar

```bash
python main.py
```

Opção 1 escolhe origem e destino e roda todos os algoritmos. Opção 2 roda os exemplos que estão aqui embaixo.

## Como montamos o problema

- Cada cidade é um nó (21 cidades)
- Cada trecho é uma aresta, com custo em horas = distância / velocidade
- Velocidades: estrada 60 km/h, BR-319 na chuva 15 km/h, barco 18 km/h, avião 350 km/h + 1h para carregar
- Se tiver dois jeitos de ir entre duas cidades, fica o mais rápido
- Dá para rodar sem avião, para simular quando não tem aeronave

Heurística (Gulosa e A*): distância em linha reta até o destino dividida pela velocidade do transporte mais rápido. Ela nunca é maior que o tempo real, então é admissível.

As distâncias são aproximadas. Fizemos uma função que confere se algum trecho ficou menor que a linha reta, e ela achou um erro nosso em Manaus - Presidente Figueiredo, que a gente corrigiu.

No começo o mapa tinha poucas ligações e todos os algoritmos davam o mesmo caminho. Então colocamos mais rotas (rio Purus, rio Juruá, voo Tefé - Eirunepé etc.) para ter caminhos alternativos.

## Resultados

Manaus até Eirunepé (com avião):

| Algoritmo | Tempo | Trechos | Nós expandidos |
|-----------|-------|---------|----------------|
| BFS | 5h28 | 2 | 19 |
| DFS | 106h25 | 6 | 13 |
| DLS (limite 3) | 39h05 | 3 | 35 |
| IDS | 5h28 | 2 | 43 |
| UCS | 5h28 | 2 | 11 |
| Gulosa | 96h56 | 4 | 6 |
| A* | 5h28 | 2 | 6 |

Manaus até Coari (com avião):

| Algoritmo | Tempo | Trechos | Nós expandidos |
|-----------|-------|---------|----------------|
| BFS | 23h20 | 1 | 7 |
| DFS | 19h45 | 2 | 7 |
| UCS | 15h17 | 2 | 16 |
| Gulosa | 23h20 | 1 | 2 |
| A* | 15h17 | 2 | 16 |

Manaus até Lábrea (sem avião):

| Algoritmo | Tempo | Trechos | Nós expandidos |
|-----------|-------|---------|----------------|
| BFS | 62h32 | 2 | 9 |
| DFS | 62h32 | 2 | 14 |
| UCS | 46h50 | 4 | 15 |
| Gulosa | 48h50 | 2 | 3 |
| A* | 46h50 | 4 | 14 |

DLS de Manaus até Eirunepé mudando o limite: com limite 0 e 1 não acha, com 2 acha 5h28, com 3 acha 39h05, com 5 acha 97h32 e com 6 acha 106h25.

## O que percebemos

- UCS e A* sempre acharam o menor tempo. O A* expandiu menos nós em alguns casos (6 contra 11 em Eirunepé), mas em outros deu igual (16 e 16 em Coari). Achamos que é porque a heurística usa a velocidade do avião, que é muito maior que a do barco, então ela fica muito baixa e ajuda pouco.
- A BFS acha o caminho com menos trechos, não o mais rápido. Em Coari ela foi de barco direto (23h), mas ir de avião até Tefé e voltar de barco dava 15h.
- A Gulosa errou feio em Eirunepé: foi de avião para Tabatinga porque fica mais perto em linha reta, mas de lá não tem voo e o resto foi de barco (97h). Em Lábrea ela foi pela BR-319, que é mais reta, mas na chuva é lenta.
- A DFS depende da ordem dos vizinhos. Às vezes acerta, mas em Eirunepé deu mais de 100h.
- Na DLS, aumentar o limite deixou o resultado pior. Isso acontece porque ela devolve o primeiro caminho que encontra dentro do limite, e com limite maior ela consegue ir mais fundo pelo primeiro vizinho antes de testar o avião.
- A IDS acha o mesmo caminho da BFS, mas expande bem mais nós porque recomeça a cada limite.
- O tempo de execução ficou abaixo de 1 ms em tudo, então comparamos pelo número de nós expandidos.

## Conclusão

Para esse problema o melhor foi o A*, porque acha a rota mais rápida igual à UCS e às vezes olha menos cidades. A Gulosa é rápida mas pode escolher um caminho muito ruim. BFS e IDS só servem se o objetivo for ter menos trechos, e DFS e DLS não garantem uma rota boa.
