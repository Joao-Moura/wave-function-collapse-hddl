import re
import sys
import subprocess
import glob
import random

PLANEJADOR = "<alterar_planejador>".strip().split(' ')


def le_entrada():
    restricoes_tiles = {}
    tiles_posicionados = []

    dimensao = input().split(' ')
    largura, altura = int(dimensao[0]), int(dimensao[1])
    tiles = int(input())

    for tile in range(tiles):
        entrada = input().split(' ')
        restricoes_tiles[f't{tile}'] = [
            (f't{entrada[r]}', f'd{entrada[r+1]}')
            for r in range(0, len(entrada), 2)
        ]

    qtd_posicionados = int(input()) 
    if qtd_posicionados > 0:
        for _ in range(qtd_posicionados):
            entrada = input().split(' ')
            tiles_posicionados.append(
                f'(buildmapwithtileabstract x{entrada[0]} y{entrada[1]} t{entrada[2]})')

    return largura, altura, restricoes_tiles, tiles_posicionados


def escreve_dominio():
    with open('<alterar_local_dominio>', 'w') as f:
        f.write('<alterar_dominio>')


def escreve_problema(largura, altura, restricoes_tiles, tiles_posicionados):
    linhas = [f'x{l}' for l in range(altura)]
    colunas = [f'y{c}' for c in range(largura)]
    tiles = list(restricoes_tiles.keys())

    objects = ' '.join(linhas + colunas) + ' - location\n' + ' '.join(tiles) + ' - tile'

    subtasks = '\n'.join(
        tiles_posicionados + [
            f'(buildmapabstract x{random.randrange(0, altura)} y{random.randrange(0, largura)})'
        ]
    )

    inits = []
    goals = []

    for tile, adjtiles in restricoes_tiles.items():
        for adjtile in adjtiles:
            inits.append(f'(connect {tile} {adjtile[0]} {adjtile[1]})')

    for l in range(0, altura-1):
        inits.append(f'(dec x{l} x{l+1})')
        inits.append(f'(inc x{l+1} x{l})')

    for c in range(0, largura-1):
        inits.append(f'(dec y{c} y{c+1})')
        inits.append(f'(inc y{c+1} y{c})')

    inits.append(f'(up-border x{0})')
    inits.append(f'(down-border x{altura-1})')
    inits.append(f'(left-border y{0})')
    inits.append(f'(right-border y{largura-1})')

    for l in linhas:
        for c in colunas:
            for t in restricoes_tiles.keys():
                inits.append(f'(possible {l} {c} {t})')
            inits.append(f'(empty {l} {c})')
            goals.append(f'(not (empty {l} {c}))')

    inits = '\n'.join(inits)
    goals = '\n'.join(goals)

    with open('<alterar_local_problema>', 'w') as f:
        f.write(f"""
            (define (problem wfc-problem)
                (:domain wfc)
                (:objects {objects})

                (:htn
                    :parameters ()
                    :ordered-subtasks (and
                        {subtasks}
                    )
                )
                (:init
                    {inits}
                )

                (:goal
                    (and
                        {goals}
                    )
                )
            )
            """)


def main():
    escreve_dominio()
    escreve_problema(*le_entrada())

    # subprocess.run(PLANEJADOR + ['<alterar_local_dominio>', '<alterar_local_problema>'], stdout=subprocess.DEVNULL)

    # files = glob.glob('<alterar_local_sas_plan>' + '*')
    # files.sort()

    # if len(files) == 0:
    #     sys.exit(120)

    # resposta = []
    # with open(files[-1], 'r') as f:
    #     for line in f.readlines():
    #         if 'apertar' not in line.lower():
    #             continue

    #         x = re.findall(r'x\d{1,2}?', line)
    #         y = re.findall(r'y\d{1,2}?', line)

    #         for valor_x, valor_y in zip(x, y):
    #             clique = f"({valor_x[1:]}, {valor_y[1:]})"
    #             apertar(mapa, int(valor_x[1:]), int(valor_y[1:]))
    #             resposta.append(clique)

    # for linha in range(len(mapa)):
    #     for coluna in range(len(mapa)):
    #         if mapa[linha][coluna] in ['l', 'L']:
    #             sys.exit(120)

    # print(';'.join(resposta))


if __name__ == "__main__":
    main()
