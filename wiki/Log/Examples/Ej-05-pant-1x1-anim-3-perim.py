#!/usr/bin/env python3
# ──────────────────────────────────────────────────────
# ── Pantalla 1x1. Animaciones sencillas
# ──────────────────────────────────────────────────────
import curses
import time

# ────── Tiempo de espera entre fotogramas
WAIT = 0.2


# ────────────────────────────────────────────────────────────
# ── Generar la animacion a partir de la lista de caracteres
# ────────────────────────────────────────────────────────────
def animate(anim):

    # ── Numero de veces a repetir la animacion
    for _ in range(5):

        # ── Animación de los caracteres dados
        for car in anim:

            # ── Mostrar caracter actual y esperar
            stdscr.addstr(0, 0, car)
            stdscr.refresh()
            time.sleep(WAIT)


# ────────────────
# ──     MAIN
# ────────────────

# ────── Caracteres de la animación
anim = ['⠁', '⠈', '⠐', '⠠', '⢀', '⡀', '⠄', '⠂']


anim1 = ['⠁', '⠂', '⠄', '⡀']
anim2 = ['⠈', '⠐', '⠠', '⢀']

# ────── Constantes para determinar la visibilidad del cursor
ON = 2
OFF = 0

# ────── Inicializacion
stdscr = curses.initscr()

# ── Ocultar el cursor
curses.curs_set(OFF)

animate(anim)

stdscr.addstr(2, 0, "Pulsa una tecla")

# ── Esperar a que el usuario apriete una tecla
stdscr.getch()

# ── Volver a enseñar el cursor antes de terminar
curses.curs_set(ON)

# ── Terminar. Volver a la pantalla original del terminal
curses.endwin()
