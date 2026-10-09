# Sudoku for the TI-84 Evo
# Fill the board so every row, column and 3x3 box has 1-9 once.
# Keys: arrows = move, 1-9 = write, del or 0 = erase,
#       enter = next number (1, 2 ... 9, empty), clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep

LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
QUIT = (9, 45)                # clear
ERASE = (23, 102)             # del, 0
NUMBER_KEYS = {92: 1, 93: 2, 94: 3, 82: 4, 83: 5, 84: 6, 72: 7, 73: 8, 74: 9}

C = 22                        # cell size with its line
X0 = 4
Y0 = (SH - (9 * C + 4)) // 2
TX = X0 + 9 * C + 4 + 6       # text panel (black, so text is fine)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT = (220, 220, 220)
GIVEN = (0, 0, 0)             # numbers from the puzzle
MINE = (0, 60, 230)           # your numbers
WRONG = (220, 0, 0)           # same number twice in a row, column or box
YELLOW = (255, 220, 0)
LEVELS = ["Easy", "Medium", "Hard"]

# Puzzles made on the PC, each with exactly one solution (0 = empty).
# Every game shuffles digits, rows and columns, so they look different.
PUZZLES = [
 ["235060104009307000010254960050006237980003005300000806020098301860002009000405602",
  "030020800700008615800700002100076289600053701070002536360504007200069000940037100",
  "000000709807090150000504320090405000031007860720068904100640500069050082070280613",
  "040830090300197004009600081760304059492000000001900406050716902604000007000053618"],
 ["080105090510890020490030000008703000000019000369000040000000064900200503630001072",
  "040170800020490050018003000006010000000206100750804209172000600000302000490700080",
  "001960000060054000050380000000800627328400150000509830040030006100090080086000010",
  "000006795008900021000030406024009000906184007007000009780300604502600000003000050"],
 ["000000006800501000102800009004610290009070000000400008000040020320000040007063080",
  "400000000003462008009000050000000040840009700970200100000006087198300002005000000",
  "073000008002500000400002900080000001310000000054680000000810400006704020040090080",
  "140000000900800023000400906850700200006002300209080000300000105001900000000200004"]]

# Digits 1-9 as 3 x 5 block pictures (text can't sit on light squares)
DIGITS = [".#.", "##.", ".#.", ".#.", "###",
          "##.", "..#", ".#.", "#..", "###",
          "##.", "..#", ".#.", "..#", "##.",
          "#.#", "#.#", "###", "..#", "..#",
          "###", "#..", "##.", "..#", "##.",
          ".##", "#..", "###", "#.#", "###",
          "###", "..#", ".#.", ".#.", ".#.",
          "###", "#.#", "###", "#.#", "###",
          "###", "#.#", "###", "..#", "##."]

grid = [0] * 81
given = [False] * 81

def paint():
    if paint_buffer:
        paint_buffer()

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

def text(row, s, col=WHITE):           # right panel, rows 30 px high
    set_color(*BLACK)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

# Solved puzzles are saved in the calculator list SUDOK: [easy, medium, hard]
def load_stats():
    try:
        l = recall_list("SUDOK")
        return [int(l[0]), int(l[1]), int(l[2])]
    except:
        return [0, 0, 0]

def save_stats(s):
    try:
        store_list("SUDOK", s)
    except:
        pass

# The Evo's random module has no shuffle(), so we mix a list ourselves
def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = random.randrange(i + 1)
        lst[i], lst[j] = lst[j], lst[i]

def shuffled(p):                       # same puzzle, new look
    d = list(range(1, 10))
    shuffle(d)
    def order():                       # mix the 3 groups and the lines inside them
        groups = [0, 1, 2]
        shuffle(groups)
        out = []
        for g in groups:
            inside = [0, 1, 2]
            shuffle(inside)
            out += [g * 3 + i for i in inside]
        return out
    rows, cols = order(), order()
    flip = random.random() < 0.5
    out = []
    for r in range(9):
        for c in range(9):
            rr, cc = (cols[c], rows[r]) if flip else (rows[r], cols[c])
            v = int(p[rr * 9 + cc])
            out.append(d[v - 1] if v else 0)
    return out

def pos(i):                            # pixel of row/column i (thick line every 3)
    return i * C + (i // 3) * 2

def peers(i):                          # same row, column or box
    r, c = divmod(i, 9)
    br, bc = r // 3 * 3, c // 3 * 3
    s = set(range(r * 9, r * 9 + 9)) | set(range(c, 81, 9))
    s |= {(br + a) * 9 + bc + b for a in range(3) for b in range(3)}
    s.discard(i)
    return list(s)                     # a list uses less memory than a set

PEERS = [peers(i) for i in range(81)]

def wrong(i):
    v = grid[i]
    return v and any(grid[j] == v for j in PEERS[i])

def digit(d, x, y):
    for r in range(5):
        row = DIGITS[(d - 1) * 5 + r]
        c = 0
        while c < 3:
            if row[c] == "#":
                e = c
                while e < 3 and row[e] == "#":
                    e += 1
                fill_rect(x + c * 3, y + r * 3, (e - c) * 3, 3)
                c = e
            else:
                c += 1

def cell(i, cursor=False):
    r, c = divmod(i, 9)
    x, y = X0 + pos(c), Y0 + pos(r)
    set_color(*LIGHT)
    fill_rect(x, y, C - 1, C - 1)
    if grid[i]:
        set_color(*(GIVEN if given[i] else WRONG if wrong(i) else MINE))
        digit(grid[i], x + 6, y + 3)
    if cursor:                         # thick yellow frame
        set_color(*YELLOW)
        fill_rect(x, y, C - 1, 3)
        fill_rect(x, y + C - 4, C - 1, 3)
        fill_rect(x, y, 3, C - 1)
        fill_rect(x + C - 4, y, 3, C - 1)

def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(*BLACK)
    fill_rect(0, 64, SW, SH - 64)
    set_color(*WHITE)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(*BLACK)
            fill_rect(x - 20, 64 + i * 28, 200, 27)
            set_color(*(YELLOW if i == choice else (150, 150, 150)))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

def start_screen(stats):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    x = SW // 2 - 80
    set_color(*MINE)
    write(x + 30, 25, "SUDOKU")
    set_color(*WHITE)
    write(x, 55, "Solved " + str(stats[0]) + " / " + str(stats[1]) + " / " + str(stats[2]))
    return menu(LEVELS, 0, "UP/DOWN + ENTER")

def game(level):                       # returns True when solved
    p = shuffled(random.choice(PUZZLES[level]))
    for i in range(81):
        grid[i] = p[i]
        given[i] = p[i] != 0
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    cur = 40                           # start in the middle
    for i in range(81):
        cell(i, i == cur)
    text(0, "SUDOKU")
    text(1, LEVELS[level])
    text(3, "1-9: write")
    text(4, "DEL: erase")
    text(5, "ENTER: +1")
    text(6, "CLEAR:quit")
    while True:
        paint()
        k = key()
        if not k:
            sleep(0.03)
            continue
        if k in QUIT:
            return False
        old = cur
        r, c = divmod(cur, 9)
        if k in LEFT:
            c = (c - 1) % 9
        elif k in RIGHT:
            c = (c + 1) % 9
        elif k in UP:
            r = (r - 1) % 9
        elif k in DOWN:
            r = (r + 1) % 9
        elif not given[cur]:
            before = grid[cur]
            if k in NUMBER_KEYS:
                grid[cur] = NUMBER_KEYS[k]
            elif k in ERASE:
                grid[cur] = 0
            elif k in OK:
                grid[cur] = (grid[cur] + 1) % 10
            if grid[cur] != before:
                # squares with the old or new number may turn red or blue
                for j in PEERS[cur]:
                    if grid[j] and grid[j] in (before, grid[cur]) and not given[j]:
                        cell(j)
                cell(cur, True)
                if 0 not in grid and not any(wrong(i) for i in range(81)):
                    return True
        cur = r * 9 + c
        if cur != old:
            cell(old)
            cell(cur, True)

# --- start ---
stats = load_stats()
level = start_screen(stats)
while level >= 0:
    if not game(level):
        break
    stats[level] += 1
    save_stats(stats)
    text(2, "SOLVED!", YELLOW)
    text(5, "ENTER:again")
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
