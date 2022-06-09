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
SIMULATION = 3
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


def monte_carlo(grid, computer, tries = 1000):
    score = 0
    for k in range(tries):
        player = next_player(computer)
        plays = []
        
        for _ in range(8):
            if get_state(grid) != NOT_TERMINAL:
                break
            
            has_played = False
            
            for i in legal_plays(grid):
                grid2 = [L.copy() for L in grid]
                do_play(grid2, i, player)
                if get_state(grid2) == player:
                    do_play(grid, i, player)
                    has_played = True
                    break
            
            if has_played:
                break
            
            play = choice(legal_plays(grid))
            do_play(grid, play, player)
            plays.append(play)
            player = next_player(player)
        
        for play in plays:
            grid[play].pop()

        state = get_state(grid)
        if state == computer:
            score += 1
        if state == next_player(computer):
            score -= 1

    return score


def choose_play(grid, t, computer):
    for i in legal_plays(grid):
        grid2 = [L.copy() for L in grid]
        do_play(grid2, i, computer)
        if get_state(grid2) == computer:
            do_play(grid, i, computer)
            return

    for i in legal_plays(grid):
        grid2 = [L.copy() for L in grid]
        do_play(grid2, i, next_player(computer))
        if get_state(grid2) == next_player(computer):
            do_play(grid, i, computer)
            return

    best = (-1, -9000)
    for i in legal_plays(grid):
        if t <= 4 and i not in [2, 3, 4]:
            continue
        grid2 = [L.copy() for L in grid]
        do_play(grid2, i, computer)
        score = monte_carlo(grid2, computer)
        if score > best[1]:
            best = (i, score)

    do_play(grid, best[0], computer)


from colorama import Fore

def get_color(player):
    if player == RED:
        return Fore.RED
    if player == YELLOW:
        return Fore.YELLOW
    return Fore.BLACK
    


def display_grid(grid):
    lines = ["|"] * HEIGHT
    for j in range(HEIGHT-1, -1, -1):
        for i in range(LENGTH):
            if len(grid[i]) > j:
                lines[HEIGHT-1-j] += get_color(grid[i][j]) + "#" + get_color(DRAW) + "|"
            else:
                lines[HEIGHT-1-j] += get_color(DRAW) + "O" + get_color(DRAW) + "|"

    print("\n\n")

    for line in lines:
        print(line)
    
    print("\n")


def check_state(grid):
    state = get_state(grid)
    if state == DRAW:
        display_grid(grid)
        print("Match nul !")
        return False
    if state == RED:
        display_grid(grid)
        print("Rouge gagne !")
        return False
    if state == YELLOW:
        display_grid(grid)
        print("Jaune gagne !")
        return False
    
    return True


def turn(grid, first_player, t):
    if first_player == SIMULATION:
        display_grid(grid)
        
        choose_play(grid, t, RED)
        
        if not check_state(grid):
            return False

        choose_play(grid, t, YELLOW)
        
        if not check_state(grid):
            return False
    
    if first_player == RED:
        display_grid(grid)
        
        i = int(input("Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        while i not in legal_plays(grid):
            display_grid(grid)
            i = int(input("Coup invalide. Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        do_play(grid, i, RED)
        
        if not check_state(grid):
            return False

        choose_play(grid, t, YELLOW)
        
        if not check_state(grid):
            return False

    if first_player == YELLOW:
        choose_play(grid, t, YELLOW)
        
        if not check_state(grid):
            return False

        display_grid(grid)
        i = int(input("Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        while i not in legal_plays(grid):
            display_grid(grid)
            i = int(input("Coup invalide. Où jouer (0-" + str(LENGTH - 1) + ") ? "))
        do_play(grid, i, RED)
        
        if not check_state(grid):
            return False

    return True


grid_ = [[] for _ in range(LENGTH)]
counter = 1
while turn(grid_, RED, counter):
    counter += 1
