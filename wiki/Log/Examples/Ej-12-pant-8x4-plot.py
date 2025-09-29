#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla genérica de WIDTH x HEIGHT caracteres
# ── Funcion de plot persistente
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Dimensiones de la pantalla en caracteres
WIDTH = 8
HEIGHT = 4

# ────── Dimensiones de la pantalla en píxeles
PIX_WIDTH = 2 * WIDTH
PIX_HEIGHT = 4 * HEIGHT

# ────── Tiempo de espera entre fotogramas
WAIT = 10 / (PIX_WIDTH * PIX_HEIGHT)

# ────── Pantalla virtual de WIDTH x HEIGHT caracteres
pantalla = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


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
    pantalla_refresh()


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

# ── Imprimir las coordenadas x de caracteres en la parte inferior
for i in range(WIDTH):
    stdscr.addstr(HEIGHT, i, str(i))

# ── Imprimir las coordenadas y de caracteres en la parte derecha
for i in range(HEIGHT):
    stdscr.addstr(i, WIDTH, str(i))

# ───────── Dibujar todos los pixeles

# ── Para cada linea...
for y in range(PIX_HEIGHT):

    # ── Dibujar pixeles en la linea actual
    for x in range(PIX_WIDTH):
        plot(x, y)
        time.sleep(WAIT)


stdscr.addstr(HEIGHT+1, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
