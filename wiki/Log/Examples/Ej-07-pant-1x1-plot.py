#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla 1x1. Funcion de plot
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Tiempo de espera entre fotogramas
WAIT = 0.4


# ──────────────────────────────────────────────────────────────────────
# ── Obtener el codigo unicode braile (byte) a partir de la posicion
# ── del pixel (x,y) dentro del carácter
# ── x ∈ [0,1]
# ── y ∈ [0,3]
# ──────────────────────────────────────────────────────────────────────
def braile_from_pos(x, y):

    # ──── La funcion tiene valores diferentes segun los casos
    # ──── Caso normal (y<3)
    # ──── Caso especial (y=3)
    cod = 1 << (3*x + y) if y < 3 else 1 << (x + 6)
    return cod


# ──────────────────────────────────────────────────────────────────────
# ── Dibujar en la pantalla 1x1 el pixel de la posicion (x,y)
# ── x ∈ [0,1]
# ── y ∈ [0,3]
# ── Al dibujar un pixel se borra el anterior
# ──────────────────────────────────────────────────────────────────────
def plot(x, y):
    # -- Obtener el byte a partir de (x,y)
    b = braile_from_pos(x, y)

    # ── Obtener el carácter unicode a partir de su codigo
    car = chr(0x2800 + b)

    # ── Mostrarlo en la pantalla
    stdscr.addstr(0, 0, car)
    stdscr.refresh()


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


# ── Animacion horizontal para cada linea
for y in range(4):

    # ── Repetir la animacion horizontal
    for _ in range(3):

        # ── Animación en horizontal
        for x in range(2):
            plot(x, y)
            time.sleep(WAIT)


stdscr.addstr(2, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
