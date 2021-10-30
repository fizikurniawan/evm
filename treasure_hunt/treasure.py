#!/bin/python3
"""
Simple Treasure Hunt Game
"""
import random


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def is_equal_to(self, pt):
        if pt == None:
            return False

        if self.x == pt.x and self.y == pt.y:
            return True

        return False

    def is_adjacent_to(self, pt):
        if (self.y < pt.y - 1) or (self.y > pt.y + 1):
            return False

        if (self.x < pt.x - 1) or (self.x > pt.x + 1):
            return False

        return True


POSITION_TREASURE = None
POSSIBLE_TREASURE_COORDINATE = [
    Point(3, 1),
    Point(4, 1),
    Point(5, 1),
    Point(6, 1),
    Point(1, 2),
    Point(2, 2),
    Point(3, 2),
    Point(5, 2),
    Point(1, 3),
    Point(5, 3),
    Point(6, 3),
    Point(1, 4),
    Point(2, 4),
    Point(3, 4),
    Point(4, 4),
    Point(5, 4),
    Point(6, 4),
]
PLAYER_POSITION = Point(1, 1)


def show_introduce():
    print(
        """
    Map of treasure

    Find a treasure. Available command
    1. u -> up a step(s)
    2. r -> right a step(s)
    3. d -> down a step(s)
    4. ? -> current location
    5. q -> quit game

    ########
    #......#
    #.###..#
    #...#.##
    #X#....#
    ########

    Legends:
    1. # -> obstacle
    2. . clear path and possible treasue has burried
    3. X is your start point (1, 1)

    """
    )


def generate_treasure_coordinate():
    index_treasure = random.randrange(16)
    global POSSIBLE_TREASURE_COORDINATE, POSITION_TREASURE
    POSITION_TREASURE = POSSIBLE_TREASURE_COORDINATE[index_treasure]

    adjacent = [POSITION_TREASURE.to_string()]
    for possible in POSSIBLE_TREASURE_COORDINATE:
        if possible.is_equal_to(POSITION_TREASURE):
            continue

        if possible.is_adjacent_to(POSITION_TREASURE):
            adjacent.append(possible.to_string())

    adjacent_str = ", ".join(adjacent)
    print(f"The treasure might be located in {adjacent_str}")


def check_before_move(pt):
    for possible in POSSIBLE_TREASURE_COORDINATE:
        if possible.is_equal_to(pt):
            return True
    return False


def find_treasure(pt):
    """
    Find treasure by location
    """
    global POSITION_TREASURE
    if pt.is_equal_to(POSITION_TREASURE):
        return True
    return False


def execute_command():
    global PLAYER_POSITION
    input_command = input("What do you want? (u, r, d, ?, q): ")

    if input_command not in ["u", "r", "d", "?", "q"]:
        print("Move not valid")
        execute_command()

    if input_command == "q":
        return False

    if input_command == "?":
        print(f"Your current Position: {PLAYER_POSITION.to_string()}")
        execute_command()

    total_step = int(input("How much step?: "))

    if input_command == "r":
        axis_type = "+x"
        new_point = Point(PLAYER_POSITION.x + total_step, PLAYER_POSITION.y)
    elif input_command == "d":
        axis_type = "-y"
        new_point = Point(PLAYER_POSITION.x, PLAYER_POSITION.y - total_step)
    else:
        axis_type = "+y"
        new_point = Point(PLAYER_POSITION.x, PLAYER_POSITION.y + total_step)

    is_valid = False
    max_step = 0
    for i in range(total_step):
        start_x = PLAYER_POSITION.x
        start_y = PLAYER_POSITION.y

        if axis_type == "+x":
            point_to_check = Point(start_x + i + 1, start_y)
        elif axis_type == "-y":
            point_to_check = Point(start_x, start_y - (i + 1))
        elif axis_type == "+y":
            point_to_check = Point(start_x, start_y + i + 1)

        is_valid = check_before_move(point_to_check)
        max_step = i
        if not is_valid:
            break

    if not is_valid:
        print(f"Can not execute command, max move is {max_step}")
        return True
    else:
        PLAYER_POSITION = new_point
        print(f"Your location {new_point.to_string()}")

    treasure_found = find_treasure(PLAYER_POSITION)
    if treasure_found:
        print("Congratulation! You got the treasure!")
        return False

    return True


if __name__ == "__main__":
    show_introduce()
    generate_treasure_coordinate()

    loop = True
    while loop:
        loop = execute_command()
