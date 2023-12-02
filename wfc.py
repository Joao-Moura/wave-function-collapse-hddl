import re
import sys
import subprocess
import glob

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
            tiles_posicionados.append((entrada[0], entrada[1], f't{entrada[2]}'))

    return largura, altura, restricoes_tiles, tiles_posicionados


def main():
    print(le_entrada())

    # with open('<alterar_local_problema>', 'w') as f:
    #     f.write(f"""
    #         (define (problem lightsoutproblem)
    #             (:domain lightsout)
    #             (:objects {objects})
    #             (:init
    #                 (verdadeiro)
    #                 {init}
    #             )
    #             (:goal
    #                 (and
    #                     {goals}
    #                 )
    #             )
    #         )
    #         """)

    # with open('<alterar_local_dominio>', 'w') as f:
    #     f.write("""
    #         <alterar_dominio>
    #     """)

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
