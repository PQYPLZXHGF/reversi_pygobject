#!/usr/bin/env python3

import random
import datetime
import time


class GameStatus:
    NONE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Player:
    NONE = 0
    PLAYER = 1
    COMPUTER = 2


class Utilities:
    """
    Contains optional static methods as helpers

    """

    @staticmethod
    def clone_matrix(matrix):
        """Clone the given matrix to an independent matrix

        :matrix: Matrix to clone.
        :returns: An independent matrix.

        """
        return [row[:] for row in matrix]

    @staticmethod
    def convert_time(s):
        return str(datetime.timedelta(seconds=s))

    @staticmethod
    def get_player():
        return random.randint(Player.PLAYER, Player.COMPUTER)

    @staticmethod
    def get_current_time(time_format="%H:%M:%S %d/%m/%Y"):
        return time.strftime(time_format)

    @staticmethod
    def get_random_number(start, end):
        """Get random integer number in given range

        :returns: Random integer number in given range

        """
        return random.randint(start, end)

    @staticmethod
    def sort_position_list(positions):
        """ Sort input positions to order: advantage > normal > disadvantage

        :positions: List of positions in format [x, y]
        :returns: Sorted list

        """

        # TODO implement
        return positions


class Game:
    @staticmethod
    def calc_val_of_move(player, position, matrix):
        """Calculate the value of the given move on the matrix. Do not make
        the actual move.

        :player: Player who's making the move
        :position: Position of [x, y]
        :matrix: Matrix
        :returns: Value (score) of current move, based on how many pieces
        flipped, including the current move.

        """
        flip = Game.get_flip_traces(player, position, matrix)

        if len(flip) == 0:
            return 0

        return len(flip) + 1

    @staticmethod
    def get_available_moves(player, matrix):
        """Get available list of possible moves for the current player on the
        given matrix.

        :player: Player
        :matrix: matrix to calculate
        :returns: List of positions which is possible to make moves on, in
        format [[x1, y1], [x2, y2], [x3, y3], ...]

        """
        moves = []

        for row in range(8):
            for col in range(8):
                if matrix[row][col] != 0:
                    continue

                if len(Game.get_flip_traces(player, [row, col], matrix)) != 0:
                    moves.append([row, col])

        return moves

    @staticmethod
    def get_move_with_highest_score(result_list):
        """Calculate and give the move with highest score.
        If there's more than one move with highest score, the chosen one
        will be randomized from the list of highest scores.

        :result_list: list of moves in format [[[x1, y1], val1],
        [[x2, y2], val2], [[x3, y3], val3], ...]
        :returns: The best move in format [[x, y], val], which have highest
        value or chosen randomly from the list which have the same (highest)
        values.

        """
        i_max = None
        val_max = None
        list_max = []

        for i, move in enumerate(result_list[:]):
            if val_max is None or move[1] > val_max:
                i_max = i
                val_max = move[1]

                # Update list of max values
                del list_max[:]
                list_max.append(move)

            elif move[1] == val_max:
                # Append the move which have the same value to the list
                list_max.append(move)

        # Return the highest val
        if len(list_max) == 1:
            return result_list[i_max]

        # Return random highest val
        return list_max[Utilities.get_random_number(0, len(list_max) - 1)]

    @staticmethod
    def get_flip_traces(player, position, matrix):
        """ Get the list of flip traces as position for the current player on
        the given position. Does not make the actual move.

        :player: Player
        :position: Position [x, y] on matrix, must be a valid move
        :matrix: matrix to make move on.
        :returns: List of position which can be flipped for scoring, in list
        format of [[x1, y1], [x2, y2], [x3, y3], ...]

        """

        flips = []
        x, y = position[:]

        # Return empty list if x, y refer to invalid position
        if matrix[x][y] != 0 or not Game.is_on_matrix(position):
            return flips

        tile = player

        if tile == Player.PLAYER:
            other_tile = Player.COMPUTER
        elif tile == Player.COMPUTER:
            other_tile = Player.PLAYER

        for x_direction, y_direction in [[-1, -1], [-1, 0], [-1, 1],
                                         [0, -1], [0, 1],
                                         [1, -1], [1, 0], [1, 1]]:
            x_start, y_start = x, y
            x_start += x_direction
            y_start += y_direction

            if Game.is_on_matrix([x_start, y_start]) \
                    and matrix[x_start][y_start] == other_tile:
                x_start += x_direction
                y_start += y_direction

                if not Game.is_on_matrix([x_start, y_start]):
                    continue

                while matrix[x_start][y_start] == other_tile:
                    x_start += x_direction
                    y_start += y_direction

                    if not Game.is_on_matrix([x_start, y_start]):
                        break

                if not Game.is_on_matrix([x_start, y_start]):
                    continue

                if matrix[x_start][y_start] == tile:
                    while True:
                        x_start -= x_direction
                        y_start -= y_direction

                        if x_start == x and y_start == y:
                            break

                        flips.append([x_start, y_start])

        return flips

    @staticmethod
    def is_on_matrix(position):
        """Check if current position is on matrix.

        :position: pair of [x, y] position on matrix
        :returns: True if the given position is on matrix. Otherwise, False.

        """
        x, y = position[:]

        if x < 0 or y < 0 or x > 7 or y > 7:
            return False

        return True

    @staticmethod
    def is_on_advantage_zone(position):
        """Check if current position is on "advantage zone"
        (border minus 8 disadvantage positions)

        :position: Position in format [x, y] to check
        :returns: True if condition of "advantage zone" satisfied.

        """
        x, y = position[:]

        # Position is on corner
        if x == 0 or y == 0 or x == 7 or y == 7:
            # Check if position is on "disadvantage zone" of corner
            if isinstance([x, y], [[0, 1], [0, 6], [1, 0], [1, 7],
                                   [6, 0], [6, 7], [7, 1], [7, 6]]):
                return False

            # Position is on normal corner zone
            return True

        # Position is not on corner
        return False

    @staticmethod
    def is_on_disadvantage_zone(position):
        """ Check if current position is on "disadvantage zone"
        (all positions which is next to borders, including 8 positions next to
        4 corners)

        :position: Position in format [x, y] to check
        :returns: True if condition of "disadvantage zone" satisfied

        """
        x, y = position[:]

        if x == 1 or x == 6 or y == 1 or y == 6:
            return True

        return False

    @staticmethod
    def is_on_normal_zone(position):
        """Check if current position is on "normal zone" (not on any special
         zones)

         :position: Position in format [x, y] to check
         :returns: True if none of the special conditions met

        """

        if Game.is_on_advantage_zone(position) or \
                Game.is_on_disadvantage_zone(position):
            return False

        return True

    @staticmethod
    def get_nearby_borders(position, matrix):
        """Get nearby available positions which is on border

        :position: Position in format [x, y]
        :matrix: Current matrix

        """
        relatives = []

        for x_direction, y_direction in [[-1, -1], [-1, 0], [-1, 1],
                                         [0, -1], [0, 1],
                                         [1, -1], [1, 0], [1, 1]]:
            x, y = position[:]
            x_forward = x + x_direction
            y_forward = y + y_direction

            # TODO recheck condition
            if ((x_forward == 0 and y_forward in range(8)) or \
                (x_forward == 7 and y_forward in range(8)) or \
                (y_forward == 0 and x_forward in range(8)) or \
                (y_forward == 7 and x_forward in range(8))
               ) and matrix[x_forward, y_forward] == 0:
                relatives.append([x_forward, y_forward])

        return relatives

    @staticmethod
    def make_move(player, position, matrix):
        """Make move at the given position. You should check if the position
        is valid itself before passing to this method.

        :player: Player who makes move
        :position: Position [x, y] to make move on
        :matrix: Matrix to make move on, can be virtual one
        :returns: Length of flipped pieces. False if no moves made (0 flips)

        """
        row, col = position[:]

        # Get flip list for current movement
        flip_stack = Game.get_flip_traces(player, position, matrix)

        if len(flip_stack) == 0:
            return False

        # Fill the flip list and player moves in matrix
        for i in range(len(flip_stack)):
            x, y = flip_stack[i][:]
            matrix[x][y] = player

        matrix[row][col] = player

        return len(flip_stack)
