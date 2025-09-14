#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla 4x1. Funcion de plot persistente
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Tiempo de espera entre fotogramas
WAIT = 0.1

# ────── Pantalla virtual de 4x1 pixeles
pantalla = [
    [0, 0, 0, 0],   # ── y = 0
]


# ────── Refrescar la pantalla 4x1 en la pantalla de ncurses
def pantalla_refresh():

    for x in range(4):
        stdscr.addstr(0, x, chr(0x2800 + pantalla[0][x]))

    stdscr.refresh()


# ──────────────────────────────────────────────────────────────────────
# ── Obtener el codigo unicode braile (byte) a partir de la posicion
# ── del pixel (x,y) dentro del carácter
# ── x ∈ [0,7]
# ── y ∈ [0,3]
# ──────────────────────────────────────────────────────────────────────
def braile_from_pos(x, y):

    # ──── La funcion tiene valores diferentes segun los casos
    # ──── Caso normal (y<3)
    # ──── Caso especial (y=3)
    cod = 1 << (3*x + y) if y < 3 else 1 << (x + 6)
    return cod


# ──────────────────────────────────────────────────────────────────────
# ── Dibujar en la pantalla 2x1 el pixel de la posicion (x,y)
# ── x ∈ [0,7]
# ── y ∈ [0,3]
# ── El ploteado se hace en la pantalla virtual, y se combina con
# ── lo que ya hubiese antes
# ──────────────────────────────────────────────────────────────────────
def plot(x, y):

    # ── Obtener las coordenadas del carácter
    xc = x >> 1
    yc = y >> 2

    # ── Obtener las coordenadas locales
    xl = x & 0x01
    yl = y

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

stdscr.addstr(1,  0, "0123")
# ───────── Dibujar todos los pixeles

# ── Para cada linea...
for y in range(4):

    # ── Dibujar pixeles en la linea actual
    for x in range(8):
        plot(x, y)
        time.sleep(WAIT)


stdscr.addstr(2, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
