#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Ejemplo de dibujo de sprites en la pantalla
# ── Animación de un LED parpadeando
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Dimensiones de la pantalla en caracteres
WIDTH = 78
HEIGHT = 22

# ────── Dimensiones de la pantalla en píxeles
PIX_WIDTH = 2 * WIDTH
PIX_HEIGHT = 4 * HEIGHT

# ────── Tiempo de espera entre fotogramas
WAIT = 5

# ────── Pantalla virtual de WIDTH x HEIGHT caracteres
pantalla = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


# ────── Borrar la pantalla virtual
def pantalla_cls():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pantalla[y][x] = 0


# ────── Refrescar la pantalla en la pantalla de ncurses
def pantalla_refresh():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            stdscr.addstr(y, x, chr(0x2800 + pantalla[y][x]))

    stdscr.refresh()


# ──────────────────────────────────────────────────────────────────────
# ── Obtener el codigo unicode braile (byte) a partir de la posicion
# ── del pixel (x,y) dentro del carácter
# ── x ∈ [0, 1]
# ── y ∈ [0, 3]
# ──────────────────────────────────────────────────────────────────────
def braile_from_pos(x, y):

    # ──── La funcion tiene valores diferentes segun los casos
    # ──── Caso normal (y < 3)
    # ──── Caso especial (y=3)
    cod = 1 << (3*x + y) if y < 3 else 1 << (x + 6)
    return cod


# ──────────────────────────────────────────────────────────────────────
# ── Dibujar en la pantalla el pixel de la posicion (x,y)
# ── x ∈ [0, PIX_WIDTH-1]
# ── y ∈ [0, PIX_HEIGHT-1]
# ── El ploteado se hace en la pantalla virtual, y se combina con
# ── lo que ya hubiese antes
# ──────────────────────────────────────────────────────────────────────
def plot(x, y):

    # ── Obtener las coordenadas del carácter
    xc = x >> 1
    yc = y >> 2

    # ── Obtener las coordenadas locales
    xl = x & 0x01
    yl = y & 0x03

    # ── Obtener el byte a partir de (xl, yl)
    b = braile_from_pos(xl, yl)

    # ── Obtener el valor actual de la pantalla
    value = pantalla[yc][xc]

    # ── Calcular el nuevo valor
    value = value | b

    # ── Actualizar la pantalla virtual
    pantalla[yc][xc] = value

    # ── Mostrarlo en la pantalla real
    # pantalla_refresh()


def plot_sprite(x, y, sprite):
    sprite_width = len(sprite[0])
    sprite_height = len(sprite)
    for j in range(sprite_height):
        for i in range(sprite_width):
            if sprite[j][i] == 'x':
                plot(x + i, y + j)


# ────────────────
# ──     MAIN
# ────────────────

# ────── Constantes para determinar la visibilidad del cursor
ON = 2
OFF = 0

# ────── Sprite
manic1 = [
    "        ",
    "     xx ",
    "  xxxxx ",
    " xxxxx  ",
    "  xx x  ",
    "  xxxxx ",
    "  xxxx  ",
    "   xx   ",
    "  xxxx  ",
    " xx xxx ",
    " xx xxx ",
    " xx xxx ",
    " xxx xx ",
    "  xxxx  ",
    "   xx   ",
    "   xx   ",
    "   xxx  ",
    "        ",
]

manic2 = [
    "        ",
    "     xx ",
    "  xxxxx ",
    " xxxxx  ",
    "  xx x  ",
    "  xxxxx ",
    "  xxxx  ",
    "   xx   ",
    "  xxxx  ",
    " xxxxxx ",
    " xxxxxx ",
    "xxxx xxx",
    "xxxxx xx",
    "  xxxx  ",
    " xxx xx ",
    " xx xxx ",
    " xxx xxx",
    "         ",
]

manic3 = [
    "          ",
    "      xx  ",
    "   xxxxx  ",
    "  xxxxx   ",
    "   xx x   ",
    "   xxxxx  ",
    "   xxxx   ",
    "    xx    ",
    "   xxxx   ",
    "  xxxxxx  ",
    " xxxxxxxx ",
    "xxxxxxxxxx",
    "xx xxxx xx",
    "   xxxxx  ",
    "  xxx xx x",
    " xx    xxx",
    " xxx   xx ",
    "          ",
]

"""
Resultado:
⢀⣤⣴⠆⠀⢀⣤⣴⠆⠀⢀⣤⣴⠆ ⠀⣠⣤⡶
⠀⢿⡾⠂⠀⠀⢿⡾⠂⠀⠀⢿⡾⠂ ⠀⠸⣷⠗⠀
⣰⣿⢿⣆⠀⢰⡏⣿⡆⠀⣰⣿⢿⣆ ⣠⣾⣿⣷⣄
⢩⡿⣳⡍⠀⠈⢻⡞⠁⠀⢩⡿⣳⡍ ⢉⡼⠟⢷⣩
⠈⠉⠈⠉⠀⠀⠈⠉⠀⠀⠈⠉⠈⠉ ⠈⠉⠀⠈⠁⠀
"""

# ────── Inicializacion
stdscr = curses.initscr()

# ── Ocultar el cursor
curses.curs_set(OFF)

x = 0

for _ in range(10):
    pantalla_cls()
    plot_sprite(x, 0, manic1)
    pantalla_refresh()
    time.sleep(WAIT)

    pantalla_cls()
    plot_sprite(x+2, 0, manic2)
    pantalla_refresh()
    time.sleep(WAIT)

    pantalla_cls()
    plot_sprite(x+2, 0, manic3)
    pantalla_refresh()
    time.sleep(WAIT)

    pantalla_cls()
    plot_sprite(x+4, 0, manic2)
    pantalla_refresh()
    time.sleep(WAIT)

    x += 6

stdscr.addstr(5, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
