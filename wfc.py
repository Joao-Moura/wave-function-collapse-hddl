import subprocess
import random
import sys
import re


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

    x_inicial = tiles_posicionados[26:28] if tiles_posicionados else f'x{random.randrange(0, altura)}'
    y_inicial = tiles_posicionados[29:31] if tiles_posicionados else f'y{random.randrange(0, largura)}'

    subtasks = '\n'.join(
        tiles_posicionados + [
            f'(buildmapabstract {x_inicial} {y_inicial})'
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


def filtra_resultado(retorno):
    saida = []
    retorno = retorno.split('\n')[1:]

    for r in retorno:
        if 'root' in r:
            break

        if 'placetile' not in r and 'updatetile' not in r:
            continue

        x = re.findall(r'x\d{1,2}?', r)[0][1]
        y = re.findall(r'y\d{1,2}?', r)[0][1]
        t = re.findall(r't\d{1,2}?', r)[0][1]
        d = re.findall(r'd[edbc]', r)

        linha = f'{r.split(" ")[1].upper()[0]} {x} {y} {t}'

        if d:
            linha += f' {d[0][1]}'
        saida.append(linha)

    print('\n'.join(saida))


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <saida_sas>")
        exit(1)

    if sys.argv[1] not in ['stdout', 'arquivo']:
        print(f"Avaliable read methods: stdout, arquivo")
        exit(1)

    escreve_dominio()
    escreve_problema(*le_entrada())

    retorno = subprocess.run(
        PLANEJADOR + ['<alterar_local_dominio>'[6:], '<alterar_local_problema>'[6:]],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./tmp'
    )

    stdout_ou_arquivo = sys.argv[1]

    if stdout_ou_arquivo == 'stdout':
        retorno_stdout = retorno.stdout.decode('utf-8')
    else:
        with open('<alterar_local_solucao>', 'r') as f:
            retorno_stdout = f.read()
    filtra_resultado(retorno_stdout)


if __name__ == "__main__":
    main()
