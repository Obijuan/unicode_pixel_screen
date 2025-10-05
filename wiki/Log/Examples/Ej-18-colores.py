#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla 1 del Manic Miner
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Dimensiones de la pantalla en caracteres
WIDTH = 80
HEIGHT = 23

# ────── Dimensiones de la pantalla en píxeles
PIX_WIDTH = 2 * WIDTH
PIX_HEIGHT = 4 * HEIGHT

# ────── Tiempo de espera entre fotogramas
WAIT = 0.1

# ────── Pantalla virtual de WIDTH x HEIGHT caracteres
pantalla = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# ────── Atributos de la pantalla
pantalla_attr = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


# ────── Borrar la pantalla virtual
def pantalla_cls():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pantalla[y][x] = 0


# ────── Refrescar la pantalla en la pantalla de ncurses
def pantalla_refresh():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            attr = pantalla_attr[y][x]
            stdscr.addstr(y, x, chr(0x2800 + pantalla[y][x]), attr)

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
def plot(x, y, attr=0):

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
    pantalla_attr[yc][xc] = attr

    # ── Mostrarlo en la pantalla real
    # pantalla_refresh()


def plot_sprite(x, y, sprite, attr=0):
    sprite_width = len(sprite[0])
    sprite_height = len(sprite)
    for j in range(sprite_height):
        for i in range(sprite_width):
            if sprite[j][i] == 'x':
                plot(x + i, y + j, attr)


# ────────────────
# ──     SPRITES
# ────────────────
ladrillos = [
    "xx xxx x",
    "        ",
    " xxx xxx",
    "        ",
    "xx xxx x",
    "        ",
    " xxx xxx",
    "        ",
]

suelo = [
    "xxxxxxxx",
    "xxxxxxxx",
    "xx xx xx",
    " xx xxx ",
    "xx   x x",
    " x      ",
    "        ",
    "        ",
]

llave = [
    "  xx    ",
    " x  x   ",
    "x   x   ",
    "x  x    ",
    " xx x   ",
    "     x  ",
    "    x x ",
    "     x  ",
]

estalactita = [
    "xxxxxxxx",
    "xxxxxxx ",
    " xxxxxx ",
    " xxxxx  ",
    " x  xx  ",
    " x  xx  ",
    "    x   ",
    "    x   ",
]


# ────────────────────────────────────────────────
# ──  Dibujo del escenario de la pantalla 1
# ────────────────────────────────────────────────
def dibujar_escenario():

    col_red = curses.color_pair(2)
    col_ladrillos = curses.color_pair(3)
    col_yellow = curses.color_pair(4)
    col_cyan = curses.color_pair(5)
    col_green = curses.color_pair(7)

    # ── Dibujo de los muros laterales
    for y in range(14):
        plot_sprite(0, y*4, ladrillos, col_ladrillos)
        plot_sprite(152, y*4, ladrillos, col_ladrillos)

    # ── Dibujo del suelo
    for x in range(18):
        plot_sprite(x*8 + 8, 8 * 5, suelo, col_red)

    # ── Dibujo de la estalactita
    plot_sprite(44, 0, estalactita, col_cyan)
    plot_sprite(64, 0, estalactita, col_cyan)

    # ── Dibujo de la llave
    plot_sprite(36, 0, llave, col_cyan)
    plot_sprite(64, 8, llave, col_magenta)
    plot_sprite(116, 0, llave, col_yellow)
    plot_sprite(96, 32, llave, col_green)


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

# ────── Sprites para la animacion del personaje
personaje = [manic2, manic1, manic2, manic3]

# ────── Incremento del personaje (en pixeles) asociado
# ────── a cada fotograma
personaje_inc = [2, 2, 0, 2]


# ────────────────────────────────────────────────
# ──   Dibujar el personnaje
# ── ENTRADA: Numero de fotograma: 0,1,2,3,4,5....
# ── SALIDA: Incremento en pixeles del personaje
# ────────────────────────────────────────────────
def dibujar_personaje(fotograma):

    col_default = curses.color_pair(1)

    # ── Dibujo del Manic Miner
    plot_sprite(xp, yp, personaje[fotograma % 4], col_default)

    return personaje_inc[fotograma % 4]


# ────────────────
# ──     MAIN
# ────────────────

# ────── Constantes para determinar la visibilidad del cursor
ON = 2
OFF = 0

# ────── Inicializacion
stdscr = curses.initscr()

# ── Ocultar el cursor
curses.curs_set(OFF)

# ── Inicializar los colores
curses.start_color()

# ── Color por defecto (Tinta=blanco y papel=Negro)
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
col_default = curses.color_pair(1)

# ── Definir resto de colores
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
col_red = curses.color_pair(2)
col_ladrillos = curses.color_pair(3)
col_yellow = curses.color_pair(4)
col_cyan = curses.color_pair(5)
col_magenta = curses.color_pair(6)
col_green = curses.color_pair(7)

# ── Posicion inicial del personaje
xp = 8
yp = 23

for i in range(90):
    pantalla_cls()
    dibujar_escenario()

    # ── Dibujo del Manic Miner
    xinc = dibujar_personaje(i)

    # ── Incrementar posicion del personaje
    # ── en el eje x, en funcion del fotograma
    xp += xinc

    pantalla_refresh()
    stdscr.addstr(12, 5, "¡Manic Miner en modo Texto!", col_yellow)
    stdscr.refresh()
    time.sleep(WAIT)


stdscr.addstr(14, 5, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
