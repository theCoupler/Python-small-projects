from ib111 import week_06  # noqa
from typing import Dict, Set, Tuple, List, Optional


# Představte si, že máme plán ve tvaru neomezené čtvercové sítě, na níž jsou
# položeny čtvercové dílky s nákresy ulic či křižovatek (něco jako kartičky ve
# hře Carcassone). Tyto dílky budeme reprezentovat jako množiny směrů, kterými
# je možné dílek opustit. Tedy např. dílek ‹{NORTH, SOUTH}› je ulice, která
# vede severojižním směrem, dílek ‹{EAST, SOUTH, WEST}› je křižovatka ve
# tvaru T, dílek ‹{EAST}› je slepá ulice (z toho dílku je možné se posunout
# pouze na východ, ale nikam jinam). Dovolujeme i prázdnou množinu, což je
# dílek, z nějž se nedá pohnout nikam.

Heading = int
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
Tile = Set[Heading]

# Situaci na čtvercové síti popisujeme pomocí slovníku, jehož klíči jsou
# souřadnice a hodnotami dílky. Na souřadnicích, které ve slovníku nejsou,
# se žádný dílek nenachází. Souřadnice jsou ve formátu ‹(x, y)›, přičemž
# ‹x› se zvyšuje směrem na východ a ‹y› směrem na jih.

Position = Tuple[int, int]
Plan = Dict[Position, Tile]


# Napište nejprve predikát ‹is_correct›, který vrátí ‹True› právě tehdy, pokud
# na sebe všechny položené dílky správně navazují. Tedy je-li možno dílek
# nějakým směrem opustit, pak v tomto směru o jednu pozici vedle leží další
# dílek, a navíc je z tohoto dílku možné se zase vrátit.
def headings_of_tile(plan: Plan, heading: Heading,
                     position: Optional[Tuple[int, int]]) -> Optional[Tile]:

    x, y = position
    neighbouring_tiles: Dict [int, Tuple[int,int]] = {NORTH: (x, y - 1), EAST: (x + 1, y),
                          SOUTH: (x, y + 1), WEST: (x - 1, y)}

    neighbouring_tile_position = neighbouring_tiles.get(heading)

    return plan.get(neighbouring_tile_position)


def is_correct(plan: Plan) -> bool:
    possible_headings = {NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}

    for position, headings in plan.items():

        num_of_exits = False
        if len(headings) == 0:
            continue

        for heading, opposite_heading in possible_headings.items():

            if heading in headings:
                tile_to_check = headings_of_tile(plan, heading, position)
                if tile_to_check is None:
                    return False

                if tile_to_check is not None and \
                   opposite_heading in tile_to_check:

                    num_of_exits = True
                else:
                    return False

        if not num_of_exits:
            return False

    return True


# Dále implementujte čistou funkci ‹run›, která bude simulovat pohyb robota
# po plánu a vrátí jeho poslední pozici. Předpokládejte přitom, že plán je
# korektní (ve smyslu predikátu ‹is_correct› výše) a že robotova počáteční
# pozice je na některém z položených dílků. Robot se pohybuje podle
# následujících pravidel:
#
# • Na počáteční pozici si robot vybere první ze směrů, kterým je možné se
#   pohnout z počátečního dílku, a to v pořadí sever, východ, jih, západ.
#   Pokud se z počáteční pozice není možné pohnout vůbec, funkce končí.
# • V dalších krocích robot preferuje setrvat v původním směru (tj. pokud může
#   jít rovně, půjde rovně). Není-li to možné, pohne se robot jiným ze směrů na
#   aktuálním dílku – nikdy se ovšem nevrací směrem, kterým přišel (pokud dojde
#   do slepé ulice, zastaví) a má-li více možností, vybere si tu, která pro něj
#   znamená otočení doprava.
# • Pokud robot přijde na dílek, kde už někdy v minulosti byl, zastaví.

def run(plan: Plan, start: Position) -> Position:
    start_directions = plan.get(start)
    visited_positions: Set[Position] = set()

    for direction in range(4):
        if direction in start_directions:
            return robot_run(plan, start, direction, visited_positions)

    return start


def robot_run(plan: Plan, position: Position, direction: int,
              visited_positions: Set[Position]) -> Position:
    if position in visited_positions:
        return position

    x, y = position
    visited_positions.add(position)
    actual_tile_directions = plan.get(position)

    if not actual_tile_directions:
        return position

    for new_direction in (direction, direction + 1, direction + 3):
        new_direction %= 4
        if new_direction in actual_tile_directions:
            if NORTH == new_direction and plan.get((x, y - 1)) is not None \
                    and direction != SOUTH:
                new_position = (x, y - 1)
                position = robot_run(plan, new_position, new_direction,
                                     visited_positions)
                break

            if EAST == new_direction and plan.get((x + 1, y)) is not None \
                    and direction != WEST:
                new_position = (x + 1, y)
                position = robot_run(plan, new_position, new_direction,
                                     visited_positions)
                break

            if SOUTH == new_direction and plan.get((x, y + 1)) is not None \
                    and direction != NORTH:
                new_position = (x, y + 1)
                position = robot_run(plan, new_position, new_direction,
                                     visited_positions)
                break

            if WEST == new_direction and plan.get((x - 1, y)) is not None \
                    and direction != EAST:
                new_position = (x - 1, y)
                position = robot_run(plan, new_position, new_direction,
                                     visited_positions)
                break

        else:
            new_direction = (new_direction + 1) % 4

    return position


def main() -> None:
    assert is_correct({})
    assert is_correct({(1, 1): set()})
    assert is_correct({(1, 1): {NORTH}, (1, 0): {SOUTH}})
    assert is_correct({
        (3, 3): {NORTH, WEST},
        (2, 2): {SOUTH, EAST},
        (3, 2): {SOUTH, WEST},
        (2, 3): {NORTH, EAST},
    })
    assert not is_correct({(0, 0): {NORTH, EAST}, (0, -1): {SOUTH}})
    assert not is_correct({(0, 0): {NORTH}, (0, 1): set()})
    assert not is_correct({(7, 7): {WEST}})
    assert not is_correct({(7, 7): {WEST}, (6, 7): set()})
    assert not is_correct({
        (3, 3): {NORTH, WEST},
        (2, 2): {SOUTH, EAST},
        (3, 2): {SOUTH, WEST},
        (2, 3): {NORTH},
    })

    plan = {
        (-2, -2): {EAST, SOUTH},
        (-1, -2): {EAST, WEST},
        (0, -2): {SOUTH, WEST},
        (-5, -1): {SOUTH},
        (-2, -1): {NORTH, SOUTH},
        (0, -1): {NORTH, SOUTH},
        (5, -1): {EAST, SOUTH},
        (6, -1): {SOUTH, WEST},
        (-5, 0): {NORTH, EAST, SOUTH},
        (-4, 0): {EAST, WEST},
        (-3, 0): {EAST, WEST},
        (-2, 0): {NORTH, EAST, WEST},
        (-1, 0): {EAST, WEST},
        (0, 0): {NORTH, EAST, SOUTH, WEST},
        (1, 0): {EAST, WEST},
        (2, 0): {EAST, SOUTH, WEST},
        (3, 0): {EAST, WEST},
        (4, 0): {EAST, WEST},
        (5, 0): {NORTH, EAST, WEST},
        (6, 0): {NORTH, WEST},
        (-5, 1): {NORTH},
        (0, 1): {NORTH, SOUTH},
        (2, 1): {NORTH, SOUTH},
        (-1, 2): {EAST},
        (0, 2): {NORTH, EAST, WEST},
        (1, 2): {EAST, WEST},
        (2, 2): {NORTH, WEST},
    }

    assert run({(0, 0): set()}, (0, 0)) == (0, 0)
    assert run({(1, 1): {NORTH}, (1, 0): {SOUTH}}, (1, 1)) == (1, 0)
    assert run({(1, 1): {NORTH}, (1, 0): {SOUTH}}, (1, 0)) == (1, 1)

    assert is_correct(plan)

    assert run(plan, (0, 0)) == (-5, -1)
    assert run(plan, (-5, -1)) == (-5, 1)
    assert run(plan, (-4, 0)) == (5, 0)
    assert run(plan, (0, 1)) == (-5, -1)
    assert run(plan, (-1, 2)) == (5, 0)

    plan[2, 0] = {WEST, SOUTH}
    plan[3, 0] = {EAST}

    assert is_correct(plan)

    assert run(plan, (-4, 0)) == (-1, 2)
    assert run(plan, (1, 2)) == (-5, -1)


if __name__ == '__main__':
    main()
