#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Impresion de dibujos en modo texto
# ──────────────────────────────────────────────────────
import curses

# ────── Constantes para determinar la visibilidad del cursor
ON = 2
OFF = 0

# ────── Inicializacion
stdscr = curses.initscr()

# ── Ocultar el cursor
curses.curs_set(OFF)

# ── Mostrar todos los píxeles de la pantalla
for y in range(23):
    stdscr.addstr(y, 0, "⣿" * 80)


# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
