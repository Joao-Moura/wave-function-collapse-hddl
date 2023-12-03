import subprocess
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


def filtra_resultado(retorno):
    saida = []
    retorno = retorno.split('\n')[1:]

    for r in retorno:
        if 'root' in r:
            break

        valores = r.split(' ')[1:]
        linha = f'{valores[0].upper()[0]} {valores[1][1]} {valores[2][1]} {valores[3][1]}'

        if valores[0][0] == 'u':
            linha += f' {valores[4][1]}'
        saida.append(linha)

    print('\n'.join(saida))


def main():
    escreve_dominio()
    escreve_problema(*le_entrada())

    retorno = subprocess.run(
        PLANEJADOR + ['<alterar_local_dominio>'[6:], '<alterar_local_problema>'[6:]],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./tmp'
    )

    retorno_stdout = retorno.stdout.decode('utf-8')
    filtra_resultado(retorno_stdout)


if __name__ == "__main__":
    main()
