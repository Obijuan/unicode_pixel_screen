#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla 1x1. Contador de píxeles
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Tiempo de espera entre fotogramas
WAIT = 0.2

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


# ── Animación del contador. Recorrer todos los caracteres braile
# ── mostrándolo en la posión (0,0) y esperando un tiempo
for i in range(256):
    # ── Obtener el carácter unicode a partir de su codigo
    car = chr(0x2800 + i)

    # ── Mostrarlo en la pantalla
    stdscr.addstr(0, 0, car)
    stdscr.refresh()
    time.sleep(WAIT)

stdscr.addstr(2, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
