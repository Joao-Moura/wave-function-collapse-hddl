# Wave Function Collapse HDDL Solution

Domínio, gerador de problema, benchmark, validador e criador de mapas para o algoritmo de WFC:

Baseado em: https://github.com/mxgmn/WaveFunctionCollapse

## Gerando problema e executável

```bash
$ ./build.sh [flags para o planejador]
```

## Gerando resultado intermediário antes do validador

```bash
$ ./build.sh [flags para o planejador]
$ python wfc.py3 [stdout(PandaPI)|arquivo(PandaDealer)] < benchmark/mapas/track/mapa
```

## Gerando novos mapas para o benchmark

```bash
$ python benchmark/benchmark.py [agile|satisficing|optimal] [stdout(PandaPI)|arquivo(PandaDealer)] [planner_args]
```

## Executando o benchmark

```bash
$ python benchmark/gerador.py [agile|satisficing|optimal] [qtd_mapas]
```
