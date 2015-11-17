"""
Curses-based graphics
"""
import curses
from collections import namedtuple
import locale
from time import sleep


State = namedtuple('State', ('state', 'symbol', 'pair'))


def simulate(screen, automata, step_length, pixel_width=1):
    """
    Simulate a cellular automata
    """
    locale.setlocale(locale.LC_ALL, "")
    encoding = locale.getpreferredencoding()

    curses.curs_set(0)
    curses.start_color()
    for background in range(1, 256):
        curses.init_pair(background, 0, background)  # for now, black fg

    for y in range(automata.cells.height):
        for x, state in enumerate(automata.cells.row(y)):
            screen.addstr(
                y,
                x * pixel_width,
                state.symbol,
                curses.color_pair(state.pair)
            )
    screen.refresh()

    while True:
        sleep(step_length)

        changes = automata.step()

        for change in changes:
            screen.addstr(
                change.y,
                change.x * pixel_width,
                change.state.symbol,
                curses.color_pair(change.state.pair)
            )
        screen.refresh()
