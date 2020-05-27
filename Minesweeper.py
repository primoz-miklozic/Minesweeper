import random
import pygame
import time

ROWS = 20
COLS = 19
SQUARE = 30

MINES = 20

LIGHTGREEN = (50, 205, 50)
DARKGREEN = (0, 128, 0)
SILVER = (192, 192, 192)

pygame.init()

screen = pygame.display.set_mode((COLS * SQUARE, ROWS * SQUARE + 70))
screen.fill(SILVER)
pygame.display.set_caption("MineField")

myfont = pygame.font.SysFont("monospace", 20)
myfontBig = pygame.font.SysFont("arialblack", 30)


class Tile:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.visible = False
        self.flaged = False

    def __repr__(self):
        return self.value


def clamp(x, minn, maxx):
    '''function used to stay in field'''
    return x if x >= minn and x <= maxx else (minn if x < minn else maxx)


def showMineField(field):
    ''' print 2D list per rows'''
    for row in range(len(field)):
        print(field[row])


def createMineField(f_rows, f_cols, f_mines):
    ''' function to create a minefield (size f_rows x f_cols), populated with mines (f_mines= number of mines) '''

    # create a list with first elements with mines and rest 'empty', then shuffle it
    random_field = []
    for i in range(f_mines):
        random_field.append("x")
    for i in range(f_rows * f_cols - f_mines):
        random_field.append(None)
    random.shuffle(random_field)

    field = [[None] * f_cols for i in range(f_rows)]
    print(field)

    # move list into a 2-D list and populate it with class Tile
    for i in range(f_rows * f_cols):
        if random_field[i] == "x":
            field[i // f_cols][i % f_cols] = Tile(i // f_cols, i % f_cols, "x")
        else:
            field[i // f_cols][i % f_cols] = Tile(i // f_cols, i % f_cols, " ")

    # for tiles that are neighbours of mines calculate number of mines and set it as value of Tile
    for row in range(len(field)):
        for col in range(len(field[row])):
            if field[row][col].value == " ":
                r_min = clamp(row - 1, 0, f_rows - 1)
                r_max = clamp(row + 1, 0, f_rows - 1)
                c_min = clamp(col - 1, 0, f_cols - 1)
                c_max = clamp(col + 1, 0, f_cols - 1)
                print(c_min, c_max)
                mines = 0
                for x in range(c_min, c_max + 1):
                    for y in range(r_min, r_max + 1):
                        if field[y][x].value == "x":
                            mines += 1

                if mines > 0:
                    field[row][col].value = str(mines)

    showMineField(field)
    return field


def drawScreen():
    greenColor = LIGHTGREEN
    for y in range(ROWS):
        for x in range(COLS):
            if greenColor == LIGHTGREEN:
                greenColor = DARKGREEN
            else:
                greenColor = LIGHTGREEN
            pygame.draw.rect(screen, greenColor, (x * SQUARE, y * SQUARE, SQUARE, SQUARE))
    pygame.display.update()


def openTile(field, row, col):
    global running

    def drawTile(tile_row, tile_col):
        global flags, opened

        if field[tile_row][tile_col].visible == False:
            opened += 1
            if field[tile_row][tile_col].flaged == True:
                field[tile_row][tile_col].flaged = False
                flags -= 1
                print(flags)
            field[tile_row][tile_col].visible = True
            pygame.draw.rect(screen, SILVER, (tile_col * SQUARE, tile_row * SQUARE, SQUARE, SQUARE))
            text = field[tile_row][tile_col].value

            # render text
            if text != " " and text != "0":
                label = myfont.render(text, 1, (147, 112, 216))
                screen.blit(label, (tile_col * SQUARE+10, tile_row * SQUARE+5))
            pygame.display.update()

    def checkSq(sq_row, sq_col):
        r_min = clamp(sq_row - 1, 0, ROWS - 1)
        r_max = clamp(sq_row + 1, 0, ROWS - 1)
        c_min = clamp(sq_col - 1, 0, COLS - 1)
        c_max = clamp(sq_col + 1, 0, COLS - 1)

        for x in range(c_min, c_max + 1):
            for y in range(r_min, r_max + 1):
                drawTile(y, x)
                if field[y][x].value == " ":
                    field[y][x].value = "0"
                    checkSq(y, x)

    drawTile(row, col)
    if field[row][col].value.upper() == "X":
        showText("GAME OVER")
        time.sleep(2)
        print("GAME OVER")
        running = False
    if field[row][col].value == " ":
        checkSq(row, col)


def plantFlag(field, row, col):
    global flags

    if field[row][col].visible == False:
        if field[row][col].flaged == False:
            field[row][col].flaged = True
            flags += 1
            print(flags)
            pygame.draw.circle(screen, (255, 0, 0),
                               (col * SQUARE + round(SQUARE / 2), row * SQUARE + round(SQUARE / 2)), 6)
        else:
            field[row][col].flaged = False
            flags -= 1
            print(flags)
            if (row * COLS + col) % 2 == 1:
                pygame.draw.circle(screen, (LIGHTGREEN),
                                   (col * SQUARE + round(SQUARE / 2), row * SQUARE + round(SQUARE / 2)), 6)
            else:
                pygame.draw.circle(screen, (DARKGREEN),
                                   (col * SQUARE + round(SQUARE / 2), row * SQUARE + round(SQUARE / 2)), 6)
        pygame.display.update()


def score():
    global flags, opened, timer_started, running

    pygame.draw.rect(screen, SILVER, (0, ROWS * SQUARE, COLS * SQUARE, 70))

    text_planted = "Flaged fields: " + str(flags)
    label_planted = myfont.render(text_planted, 1, (0, 0, 0))
    screen.blit(label_planted, (30, COLS * SQUARE + 30))

    text_opened = "Fields to open: " + str((COLS * ROWS - opened) - MINES)
    label_planted = myfont.render(text_opened, 1, (0, 0, 0))
    screen.blit(label_planted, (300, COLS * SQUARE + 30))

    if timer_started:
        text_time = "Time: " + stopWatch(time_start,time.time())
    else:
        text_time="Time: 00:00"
    label_planted = myfont.render(text_time, 1, (0, 0, 0))
    screen.blit(label_planted, (200, COLS * SQUARE + 60))


    if (COLS * ROWS - opened) == MINES:
        time_to_solve = text_time[6:]

        text_win = "Finished in " + time_to_solve
        showText(text_win)

        print("YOU WON!")

        print(time_to_solve)
        timer_started = False
        time.sleep(2)
        running = False

    pygame.display.update()

def showText(text):
        label = myfontBig.render(text, 1, (255, 0, 0))
        label_len=len(text)*17
        screen.blit(label, (int(COLS*SQUARE/2-label_len/2),int(ROWS*SQUARE/2)))
        pygame.display.update()

def stopWatch(time_start, time_stop):

    time_lapsed = time_stop - time_start
    mins = int(time_lapsed // 60)
    secs = int(time_lapsed % 60)
    if mins < 10:
        mins_str = "0" + str(mins)
    else:
        mins_str = str(mins)
    if secs < 10:
        secs_str = "0" + str(secs)
    else:
        secs_str = str(secs)
    return (mins_str + ":" + secs_str)



mineField = createMineField(ROWS, COLS, MINES)
running = True
timer_started = False
drawScreen()
flags = 0
opened = 0

while running:

    score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            col = mousex // SQUARE
            row = mousey // SQUARE
            if timer_started == False:
                timer_started = True
                time_start = time.time()
            if event.button == 1:
                openTile(mineField, row, col)
                score()
                pygame.display.update()
            if event.button == 3:
                plantFlag(mineField, row, col)
                score()
