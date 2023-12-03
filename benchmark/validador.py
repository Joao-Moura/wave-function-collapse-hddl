def extrai_entrada(entrada):
    restricoes_tiles = {}

    largura, altura = int(entrada[0][0]), int(entrada[0][2])
    tiles = int(entrada[1])

    for tile in range(tiles):
        entrada_tile = entrada[2+tile].split(' ')
        restricoes_tiles[str(tile)] = [
            f'{entrada_tile[r]}{entrada_tile[r+1]}'
            for r in range(0, len(entrada_tile), 2)
        ]

    return largura, altura, restricoes_tiles


def atualiza_restricoes(t, direcao, restricoes):
    novas_regras = []

    for tile, restricao in restricoes.items():
        for res in restricao:
            if res == f'{t}{direcao}':
                novas_regras.append(tile)

    return novas_regras


def atualiza_adjacentes(novo_x, novo_y, direcao, t, mapa, restricoes):
    if novo_x < 0 or novo_y < 0 or novo_x >= len(mapa) or novo_y >= len(mapa[0]):
        return mapa

    mapa[novo_x][novo_y] = (mapa[novo_x][novo_y][0], atualiza_restricoes(t, direcao, restricoes))
    return mapa


def valida_jogadas(entrada, linhas):
    entrada = entrada.split('\n')
    linhas = linhas.split('\n')

    largura, altura, restricoes_tiles = extrai_entrada(entrada)

    mapa = [
        [(None, list(restricoes_tiles.keys())) for _ in range(largura)]
        for _ in range(altura)
    ]

    for linha in linhas:
        linha = linha.split(' ')
        if linha[0] == 'U':
            continue

        x, y, t = int(linha[1]), int(linha[2]), linha[3]

        if mapa[x][y][0]:
            return False
        elif t not in mapa[x][y][1]:
            return False

        mapa[x][y] = (t, mapa[x][y][1])
        mapa = atualiza_adjacentes(x, y-1, 'd', t, mapa, restricoes_tiles)
        mapa = atualiza_adjacentes(x, y+1, 'e', t, mapa, restricoes_tiles)
        mapa = atualiza_adjacentes(x-1, y, 'b', t, mapa, restricoes_tiles)
        mapa = atualiza_adjacentes(x+1, y, 'c', t, mapa, restricoes_tiles)
    return True


if __name__ == "__main__":
    ...
