#!/usr/bin/env python3.5
"""
The command-line interface for pica.
"""
from argparse import ArgumentParser
import curses

from pica.automata import Automata
from pica.conditions import Equals, Not, And, Or, If, InRange
from pica.graphics import State, simulate
from pica.rules import Requirement, Rule

WIDTH = 8
HEIGHT = 8

STEP_LENGTH = 0.25


def conway(width, height):
    """
    A conway's game of life simulation
    """
    alive = State('alive', '  ', 15)
    dead = State('dead', '  ', 0)

    neighbors = [
        Equals(x, y, alive)
        for x in range(-1, 2) for y in range(-1, 2)
        if x != 0 or y != 0
    ]

    rules = [
        Requirement(
            alive, dead, Not(InRange(*neighbors, lower=2, upper=3))
        ),
        Requirement(
            dead, alive, InRange(*neighbors, lower=3, upper=3)
        ),
        Rule(alive, dead, Equals(0, 0, alive), 1),
        Rule(dead, alive, Equals(0, 0, dead), 1),
    ]

    automata = Automata(width, height, dead, *rules)
    automata.randomize((dead, alive))

    return automata


def city(width, height):
    field = State('field', '  ', 2)
    tree = State('tree', '🌲 ', 2)

    vertical_road = State('road|', '| ', 7)
    horizontal_road = State('road-', '--', 7)
    crossroad = State('road+', '+-', 7)

    house = State('house', '🏠 ', 2)
    derelict_house = State('derelict house', '🏚 ', 2)

    states = (field, tree, vertical_road, horizontal_road, crossroad, house)
    roads = (vertical_road, horizontal_road, crossroad)

    spontaneous_road = 0.001
    continued_road = 0.05

    rules = (
        ###
        # field
        ###
        Rule(field, field, Equals(0, 0, field), 0.9),

        Rule(field, tree, Equals(0, 0, field), 0.002),
        Rule(
            field,
            tree,
            InRange(
                Equals(-1, -1, tree),
                Equals(-1, 0, tree),
                Equals(-1, 1, tree),
                Equals(0, -1, tree),
                Equals(0, 1, tree),
                Equals(1, -1, tree),
                Equals(1, 0, tree),
                Equals(1, 1, tree),
                lower=3,
            ),
            0.05
        ),
        Rule(
            field,
            house,
            Or(
                Equals(-1, 0, vertical_road),
                Equals(1, 0, vertical_road),
                Equals(0, -1, horizontal_road),
                Equals(0, 1, horizontal_road),
            ),
            0.05
        ),

        # vertical road
        Requirement(
            field, vertical_road,
            Not(
                Or(
                    Equals(-1, 0, *roads),
                    Equals(1, 0, *roads),
                    Equals(0, -1, horizontal_road),
                    Equals(0, 1, horizontal_road),
                )
            )
        ),
        Rule(
            field,
            vertical_road,
            Not(And(Equals(0, -1, *states), Equals(0, 1, *states))),
            spontaneous_road
        ),
        Rule(
            field,
            vertical_road,
            Equals(0, -1, vertical_road),
            continued_road
        ),
        Rule(
            field,
            vertical_road,
            Equals(0, 1, vertical_road),
            continued_road
        ),
        Rule(
            field,
            vertical_road,
            Equals(0, -1, crossroad),
            continued_road * 2
        ),
        Rule(
            field,
            vertical_road,
            Equals(0, 1, crossroad),
            continued_road * 2
        ),

        # horizontal road
        Requirement(
            field, horizontal_road,
            Not(
                Or(
                    Equals(-1, 0, vertical_road),
                    Equals(1, 0, vertical_road),
                    Equals(0, -1, *roads),
                    Equals(0, 1, *roads),
                )
            )
        ),
        Rule(
            field,
            horizontal_road,
            Not(And(Equals(-1, 0, *states), Equals(1, 0, *states))),
            spontaneous_road
        ),
        Rule(
            field,
            horizontal_road,
            Equals(-1, 0, horizontal_road),
            continued_road
        ),
        Rule(
            field,
            horizontal_road,
            Equals(1, 0, horizontal_road),
            continued_road
        ),
        Rule(
            field,
            horizontal_road,
            Equals(-1, 0, crossroad),
            continued_road * 2
        ),
        Rule(
            field,
            horizontal_road,
            Equals(1, 0, crossroad),
            continued_road * 2
        ),

        # crossroad
        Requirement(
            field, crossroad,
            Not(
                Or(
                    Equals(-1, 0, vertical_road, crossroad),
                    Equals(1, 0, vertical_road, crossroad),
                    Equals(0, -1, horizontal_road, crossroad),
                    Equals(0, 1, horizontal_road, crossroad),
                )
            )
        ),
        Rule(
            field,
            crossroad,
            Equals(-1, 0, horizontal_road),
            continued_road
        ),
        Rule(
            field,
            crossroad,
            Equals(1, 0, horizontal_road),
            continued_road
        ),
        Rule(
            field,
            crossroad,
            Equals(0, -1, vertical_road),
            continued_road
        ),
        Rule(
            field,
            crossroad,
            Equals(0, 1, vertical_road),
            continued_road
        ),

        ###
        # road
        ###
        Rule(
            horizontal_road,
            horizontal_road,
            Equals(0, 0, horizontal_road), 0.9
        ),
        Requirement(
            horizontal_road, crossroad,
            Not(
                Or(
                    Equals(-1, 0, vertical_road, crossroad),
                    Equals(1, 0, vertical_road, crossroad),
                    Equals(0, -1, horizontal_road, crossroad),
                    Equals(0, 1, horizontal_road, crossroad),
                )
            )
        ),
        Rule(
            horizontal_road,
            crossroad,
            Or(Equals(-1, 0, horizontal_road), Equals(1, 0, horizontal_road)),
            spontaneous_road
        ),
        Rule(
            horizontal_road,
            field,
            Equals(0, 0, horizontal_road), spontaneous_road / 10
        ),

        Rule(vertical_road, vertical_road, Equals(0, 0, vertical_road), 0.9),
        Requirement(
            vertical_road, crossroad,
            Not(
                Or(
                    Equals(-1, 0, vertical_road, crossroad),
                    Equals(1, 0, vertical_road, crossroad),
                    Equals(0, -1, horizontal_road, crossroad),
                    Equals(0, 1, horizontal_road, crossroad),
                )
            )
        ),
        Rule(
            vertical_road,
            crossroad,
            Or(Equals(0, -1, vertical_road), Equals(0, 1, vertical_road)),
            spontaneous_road
        ),
        Rule(
            vertical_road,
            field,
            Equals(0, 0, vertical_road), spontaneous_road / 10
        ),
        Rule(crossroad, crossroad, Equals(0, 0, crossroad), 0.9),
        Rule(
            crossroad,
            field,
            Equals(0, 0, crossroad), spontaneous_road / 10
        ),

        ###
        # tree
        ###
        Rule(tree, tree, Equals(0, 0, tree), 0.9),
        Rule(tree, field, Equals(0, 0, tree), 0.01),
        Rule(
            tree,
            field,
            Or(
                Equals(-1, 0, horizontal_road, crossroad),
                Equals(1, 0, horizontal_road, crossroad),
                Equals(0, -1, vertical_road, crossroad),
                Equals(0, 1, vertical_road, crossroad),
            ),
            0.05
        ),

        Rule(house, house, Equals(0, 0, house), 0.9),
        Requirement(
            house, house,
            Or(
                Equals(-1, 0, vertical_road),
                Equals(1, 0, vertical_road),
                Equals(0, -1, horizontal_road),
                Equals(0, 1, horizontal_road),
            )
        ),
        Rule(house, derelict_house, Equals(0, 0, house), 0.01),
        Rule(
            house, derelict_house,
            Or(
                Equals(-1, -1, derelict_house),
                Equals(-1, 0, derelict_house),
                Equals(-1, 1, derelict_house),
                Equals(0, -1, derelict_house),
                Equals(0, 1, derelict_house),
                Equals(1, -1, derelict_house),
                Equals(1, 0, derelict_house),
                Equals(1, 1, derelict_house),
            ),
            0.05
        ),
        Rule(
            house, derelict_house,
            Or(
                Equals(-1, -1, tree),
                Equals(-1, 0, tree),
                Equals(-1, 1, tree),
                Equals(0, -1, tree),
                Equals(0, 1, tree),
                Equals(1, -1, tree),
                Equals(1, 0, tree),
                Equals(1, 1, tree),
            ),
            -0.05
        ),

        Rule(
            derelict_house,
            derelict_house,
            Equals(0, 0, derelict_house),
            0.9
        ),
        Requirement(
            derelict_house, house,
            Or(
                Equals(-1, 0, vertical_road),
                Equals(1, 0, vertical_road),
                Equals(0, -1, horizontal_road),
                Equals(0, 1, horizontal_road),
            )
        ),
        Rule(
            derelict_house,
            house,
            Equals(0, 0, derelict_house),
            0.05
        ),
        Rule(
            derelict_house, house,
            Or(
                Equals(-1, -1, tree),
                Equals(-1, 0, tree),
                Equals(-1, 1, tree),
                Equals(0, -1, tree),
                Equals(0, 1, tree),
                Equals(1, -1, tree),
                Equals(1, 0, tree),
                Equals(1, 1, tree),
            ),
            0.05
        ),
        Rule(
            derelict_house,
            field,
            Equals(0, 0, derelict_house),
            spontaneous_road
        ),
    )

    automata = Automata(width, height, field, *rules)

    return automata


def main():
    """
    Run pica from the command line.
    """
    parser = ArgumentParser(description='cellular automata')
    parser.add_argument('--width', default=8, type=int)
    parser.add_argument('--height', default=8, type=int)
    parser.add_argument('--time', default=STEP_LENGTH, type=float)
    parser.add_argument('simulation', choices=('conway', 'city'))

    args = parser.parse_args()

    if args.simulation == 'conway':
        automata = conway(args.width, args.height)
    else:
        automata = city(args.width, args.height)

    curses.wrapper(simulate, automata, args.time, 2)


if __name__ == '__main__':
    main()
