from ib111 import week_05  # noqa
from typing import List, Tuple


# «Connect Four¹» je hra pro dva hráče, v češtině někdy nazývaná Cestovní nebo
# Padající piškvorky. Každý hráč má žetony v jedné barvě; vyhrává ten, kdo jako
# první vytvoří nepřerušenou řadu «přesně čtyř» svých žetonů (horizontální,
# vertikální, diagonální). Hrací deska je přitom postavena vertikálně tak, že
# žetony padají směrem dolů, dokud nenarazí na jiný žeton nebo spodní rám
# desky. Hráč si tedy při svém tahu volí pouze sloupec, do nějž žeton hodí.
# (Na rozdíl od klasických piškvorek, kde si hráč volí přesné souřadnice
# a nic nikam nepadá.)
#
# ¹ ‹https://en.wikipedia.org/wiki/Connect_Four›
#
# Pro reprezentaci žetonů hráčů budeme v tomto úkolu používat znaky ‹X› a ‹O›.
# Hrací desku bude představovat seznam seznamů žetonů – vnitřní seznamy jsou
# postupně jednotlivé sloupce desky seřazené zdola nahoru. Tedy např. seznam
# ‹[['X'], [], ['O', 'X'], [], ['X', 'O', 'O'], [], []]›
# popisuje následující situaci:
#
#  ┌───┬───┬───┬───┬───┬───┬───┐
#  │   │   │   │   │ O │   │   │
#  ├───┼───┼───┼───┼───┼───┼───┤
#  │   │   │ X │   │ O │   │   │
#  ├───┼───┼───┼───┼───┼───┼───┤
#  │ X │   │ O │   │ X │   │   │
#  └───┴───┴───┴───┴───┴───┴───┘
#    0   1   2   3   4   5   6
#
# V naší reprezentaci přitom nemáme žádnou maximální výšku. Do sloupce
# s indexem 4 tedy je možno přidat další žeton a celá herní deska se tak
# nadstaví o další řádek.
#
# Pro hrací desku používáme typový alias ‹Grid›.

Grid = List[List[str]]


# Nejprve implementujte proceduru ‹draw›, která zadanou herní desku ‹grid›
# textově vykreslí podobně jako výše, přičemž čáry kreslete pomocí znaků ‹+›
# (pro křížení a rohy), ‹-› (pro vodorovné čáry), ‹|› (pro svislé čáry).
# Znaky pro žetony jsou od svislých čar odděleny z každé strany jednou
# mezerou, čísla jsou zarovnána na střed sloupců, pravostranné mezery se
# ignorují. Smíte přitom předpokládat, že sloupců nebude více než 10.
# Vykreslete vždy jen tolik řádků herní desky, kolik je potřeba (tedy žádné
# zcela prázdné řádky).
#
# Výše uvedenou situaci tedy vykreslete takto:
#     +---+---+---+---+---+---+---+
#     |   |   |   |   | O |   |   |
#     +---+---+---+---+---+---+---+
#     |   |   | X |   | O |   |   |
#     +---+---+---+---+---+---+---+
#     | X |   | O |   | X |   |   |
#     +---+---+---+---+---+---+---+
#       0   1   2   3   4   5   6
def get_element(grid: Grid, col: int, row: int) -> str:
    return grid[col][row]


def get_longest_column(grid: Grid) -> int:
    longest_column = 0
    for slope in grid:
        if len(slope) > longest_column:
            longest_column = len(slope)
    return longest_column


def get_separator(length: int) -> str:
    separator = "+"
    for i in range(length):
        separator = separator + "---+"
    return separator


def get_indexes_of_columns(length: int) -> str:
    str_indexes = " "
    for i in range(length):
        str_indexes = str_indexes + " " + str(i) + "  "
    return str_indexes


def draw(grid: Grid) -> None:
    num_column = len(grid)
    longest_column = get_longest_column(grid)

    print(get_separator(num_column))

    for i in range(longest_column, 0, -1):
        print("|", end="")
        for n_column, column in enumerate(grid):
            if len(column) >= i:
                print(" " + grid[n_column][i - 1] + " |", end="")
            else:
                print("   |", end="")
        print()

        print(get_separator(num_column))

    print(get_indexes_of_columns(num_column))

# Dále pak implementujte proceduru ‹play›, která provede do zadané herní desky
# ‹grid› vhození žetonu hráče ‹player› do sloupce ‹column›. Předpokládejte
# přitom, že herní deska je ve stavu, kdy ještě nikdo nevyhrál, ‹player› je
# buďto ‹'X'› nebo ‹'O'› a ‹column› je validní index sloupce. Procedura vrátí
# ‹True›, pokud tímto tahem hráč vyhrál; ‹False› jinak.
#
# Pro jistotu připomínáme, že za výhru považujeme pouze situaci, kdy má některý
# z hráčů nepřerušenou řadu «přesně čtyř» svých žetonů. Pokud tedy vhozením
# žetonu vznikne nepřerušená řada více než čtyř žetonů, o výhru se nejedná.


def play(grid: Grid, player: str, column: int) -> bool:

    grid[column].append(player)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for direction in directions:
        if check(grid, player, column, direction):
            return True

    return False


def check(grid: Grid, player: str, column: int,
          direction: Tuple[int, int]) -> bool:

    num_in_direction = 1
    y_new_el = len(grid[column]) - 1
    x_difference, y_difference = direction

    # for not counting player again , we will start from
    # first following elemenet in the direction.
    i = x_difference
    j = y_difference
    while (
       -5 < i < 5
       and -5 < j < 5
       and column + i < len(grid)
       and len(grid[column + i]) - 1 >= y_new_el + j >= 0
       and get_element(grid, column + i, y_new_el + j) == player
    ):

        num_in_direction += 1
        i += x_difference
        if y_difference != 0:
            j += y_difference

    k = - x_difference
    m = - y_difference
    while (
       -5 < k < 5
       and -5 < m < 5
       and column + k >= 0
       and len(grid[column + k]) - 1 >= y_new_el + m >= 0
       and get_element(grid, column + k, y_new_el + m) == player
    ):

        num_in_direction += 1
        k -= x_difference
        if y_difference != 0:
            m -= y_difference

    return num_in_direction == 4

# V zadání máte připravenu jednoduchou implementaci celé hry v proceduře
# ‹run_game›. Tuto proceduru můžete (poté, co implementujete ‹draw› a ‹play›)
# použít k jednoduchému testování, zda vaše implementace fungují správně.
# Parametr ‹size› je počet sloupců herní desky.


def main() -> None:
    grid: Grid = [['X'], [], ['O', 'X'], [], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'X', 3)
    assert grid == [['X'], [], ['O', 'X'], ['X'], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'O', 3)
    assert grid == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'X', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], ['X'], []]

    assert not play(grid, 'O', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], ['X', 'O'], []]

    assert not play(grid, 'X', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'],
            ['X', 'O', 'O'], ['X', 'O', 'X'], []]

    assert play(grid, 'O', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'],
            ['X', 'O', 'O'], ['X', 'O', 'X', 'O'], []]


def run_game(size: int) -> None:
    player = 'O'
    grid: Grid = [[] for _ in range(size)]
    draw(grid)
    over = False
    while not over:
        player = 'X' if player == 'O' else 'O'
        column = int(input("\nPlayer " + player + ": "))
        print()
        over = play(grid, player, column)
        draw(grid)
    print("\nGame over, player", player, "won.")


if __name__ == '__main__':
    main()
    run_game(9)  # uncomment to play the game
