import sys

from random import choice, randint, uniform

from validador import atualiza_adjacentes


SETTINGS = {
    'agile': {
        'size': [2, 3, 4],
        'maxnotempty': 0.30
    },
    'satisficing': {
        'size': [i for i in range(6, 10)],
        'maxnotempty': 0.60
    },
    'optimal': {
        'size': [i for i in range(6, 20)],
        'maxnotempty': 0.50
    },
}

# TODO: New tiles? New configs?
TILES_CONFIGURATION = [
    ['1', 'e', '1', 'd', '2', 'c', '2', 'b', '0', 'e', '0', 'd', '0', 'c', '0', 'b'],  # + (track crossing)
    ['0', 'e', '0', 'd', '3', 'c', '3', 'b', '1', 'e', '1', 'd', '1', 'c', '1', 'b'],  # - (horizontal track)
    ['0', 'c', '0', 'b', '3', 'e', '3', 'd', '2', 'e', '2', 'd', '2', 'c', '2', 'b'],  # | (vertical track)
    ['1', 'c', '1', 'b', '2', 'e', '2', 'd', '3', 'e', '3', 'd', '3', 'c', '3', 'b'],  # . (grass tile)
]

POSSIBLE_TILES = [str(i) for i in range(len(TILES_CONFIGURATION))]

TILES_RESTRICTION = {
    tile: [
        f'{TILES_CONFIGURATION[int(tile)][r]}{TILES_CONFIGURATION[int(tile)][r+1]}'
        for r in range(0, len(TILES_CONFIGURATION[int(tile)]), 2)
    ]
    for tile in POSSIBLE_TILES
}


def generate_placed_tile(map_size, placedtiles):
    tiles = []

    map = [
        [(None, POSSIBLE_TILES) for _ in range(map_size)]
        for _ in range(map_size)
    ]

    while len(tiles) != placedtiles:
        x, y, t = randint(0, map_size-1), randint(0, map_size-1), choice(POSSIBLE_TILES)

        if map[x][y][0] or t not in map[x][y][1]:
            continue

        map[x][y] = (t, map[x][y][1])
        map = atualiza_adjacentes(x, y-1, 'd', t, map, TILES_RESTRICTION)
        map = atualiza_adjacentes(x, y+1, 'e', t, map, TILES_RESTRICTION)
        map = atualiza_adjacentes(x-1, y, 'b', t, map, TILES_RESTRICTION)
        map = atualiza_adjacentes(x+1, y, 'c', t, map, TILES_RESTRICTION)

        tiles.append(f'{x} {y} {t}')

    return tiles


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <track> <max_maps_qtd>")
        exit(1)

    if sys.argv[1] not in ['agile', 'satisficing', 'optimal']:
        print(f"Avaliable tracks: agile, satisficing, optimal")
        exit(1)

    settings = SETTINGS[sys.argv[1]]

    maps = {}

    for i in range(int(sys.argv[2])):
        map_file = []
        map_size = choice(settings['size'])

        map_file.append(f'{map_size} {map_size}')
        map_file.append('4')
        map_file += [' '.join(tile) for tile in TILES_CONFIGURATION]

        placedtiles = round((map_size * map_size) * (uniform(0, settings['maxnotempty'])))
        map_file.append(f'{placedtiles}')

        if placedtiles > 0:
            map_file += generate_placed_tile(map_size, placedtiles)

        maps['\n'.join(map_file)] = map_file

    for i, (map_to_write, map_to_name) in enumerate(maps.items()):
        map_name = f'map_{map_to_name[0].replace(" ", "x")}_{map_to_name[len(POSSIBLE_TILES)+2]}_{i}'

        with open(f'benchmark/mapas/{sys.argv[1]}/{map_name}', 'w') as f:
            f.write(map_to_write)


if __name__ == "__main__":
    main()
