# 7 columns of height 6
# Red = 1, Yellow = -1
#    0000000
#    000R000
#    00YY000
# j  00RY000
# ^  00RRY00
# |  00RYYR0
# + - > i
# is [[], [], [1, 1, 1, -1], [-1, 1, -1, -1, 1], [-1, -1], [1], []]

from random import choice

LENGTH = 7
HEIGHT = 6
RED = 1
YELLOW = -1
DRAW = -2
NOT_TERMINAL = 0

def legal_plays(grid):
    plays = []
    for i in range(LENGTH):
        if len(grid[i]) < HEIGHT:
            plays.append(i)
    return plays


# THIS DOES NOT CHECK IF THE PLAY IS LEGAL
def do_play(grid, i, player):
    grid[i].append(player)


def owns_stone(grid, i, j, player):
    return len(grid[i]) > j and grid[i][j] == player


# TODO: optimize (ie if i, j+2 is not ok we can skip to i, j+3)
def has_won(grid, player):
    # horizontal
    for j in range(HEIGHT):
        for i in range(LENGTH-3):
            ok = True
            for ii in range(i, i+4):
                if not owns_stone(grid, ii, j, player):
                    ok = False
            if ok:
                return True

    # vertical
    for i in range(LENGTH):
        for j in range(HEIGHT-3):
            ok = True
            for jj in range(j, j+4):
                if not owns_stone(grid, i, jj, player):
                    ok = False
            if ok:
                return True

    # diagonal: bottom left -> top right
    for i in range(LENGTH-3):
        for j in range(HEIGHT-3):
            ok = True
            for k in range(4):
                if not owns_stone(grid, i+k, j+k, player):
                    ok = False
            if ok:
                return True

    # diagonal: top left -> bottom right
    for i in range(LENGTH-3):
        for j in range(HEIGHT-1, 2, -1):
            ok = True
            for k in range(4):
                if not owns_stone(grid, i+k, j-k, player):
                    ok = False
            if ok:
                return True

    return False


def is_full(grid):
    for i in range(LENGTH):
        if len(grid[i]) < HEIGHT:
            return False

    return True


def get_state(grid):
    if has_won(grid, RED):
        return RED

    if has_won(grid, YELLOW):
        return YELLOW

    if is_full(grid):
        return DRAW

    return NOT_TERMINAL


def next_player(previous_player):
    return -previous_player


def monte_carlo(grid, computer, tries = 200):
    score = 0
    for k in range(tries):
        player = next_player(computer)
        grid2 = [L[:] for L in grid]
        while get_state(grid2) == NOT_TERMINAL:
            do_play(grid2, choice(legal_plays(grid2)), player)
            player = next_player(player)

        state = get_state(grid2)
        if state == computer:
            score += 1
        if state == next_player(computer):
            score -= 1

    return score


def choose_play(grid):
    for i in legal_plays(grid):
        grid2 = [L.copy() for L in grid]
        do_play(grid2, i, YELLOW)
        if get_state(grid2) == YELLOW:
            do_play(grid, i, YELLOW)
            return

    for i in legal_plays(grid):
        grid2 = [L.copy() for L in grid]
        do_play(grid2, i, RED)
        if get_state(grid2) == RED:
            do_play(grid, i, YELLOW)
            return

    best = (-1, -9000)
    for i in legal_plays(grid):
        score = monte_carlo(grid, YELLOW)
        if score > best[1]:
            best = (i, score)

    do_play(grid, best[0], YELLOW)


def get_color(player):
    if player == RED:
        return '\033[91m'
    if player == YELLOW:
        return '\033[93m'
    return '\033[0m'


def display_grid(grid):
    lines = [""] * HEIGHT
    for j in range(HEIGHT-1, -1, -1):
        for i in range(LENGTH):
            if len(grid[i]) > j:
                lines[j] += get_color(grid[i][j]) + "#"
            else:
                lines[j] += get_color(DRAW) + "O"

    print("\n\n")

    for line in lines:
        print(line)


def turn(grid, first_player):
    state = get_state(grid)
    if state == DRAW:
        print("Match nul !")
        return False
    if state == RED:
        print("Rouge gagne !")
        return False
    if state == YELLOW:
        print("Jaune gagne !")
        return False

    if first_player == RED:
        display_grid(grid)
        i = int(input("Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        while i not in legal_plays(grid):
            display_grid(grid)
            i = int(input("Coup invalide. Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        do_play(grid, i, RED)

        choose_play(grid)

    else:
        choose_play(grid)

        i = int(input("Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        while i not in legal_plays(grid):
            display_grid(grid)
            i = int(input("Coup invalide. Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        do_play(grid, i, RED)

    return True


grid_ = [[] for _ in range(LENGTH)]
while turn(grid_, RED):
    continue

