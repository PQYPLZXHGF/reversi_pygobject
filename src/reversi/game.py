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


class Field:
    """Re-define the matrix into fields

    Use "position in Field.NAME" to check if the position is on defined field

    """

    CORNER = [[0, 0], [0, 7], [7, 0], [7, 7]]

    BORDER_ADVANTAGE = [[0, 2], [0, 3], [0, 4], [0, 5],
                        [2, 0], [3, 0], [4, 0], [5, 0],
                        [7, 2], [7, 3], [7, 4], [7, 5],
                        [2, 7], [3, 7], [4, 7], [5, 7]]

    BORDER_DISADVANTAGE = [[0, 1], [0, 6], [1, 0], [1, 7],
                           [6, 0], [6, 7], [7, 1], [7, 6]]

    INNER_DISADVANTAGE = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5],
                          [2, 1], [3, 1], [4, 1], [5, 1], [6, 1],
                          [6, 2], [6, 3], [6, 4], [6, 5], [6, 6],
                          [1, 6], [2, 6], [3, 6], [4, 6], [5, 6]]

    INNER_NORMAL = [[2, 2], [2, 3], [2, 4], [2, 5],
                    [3, 2], [3, 3], [3, 4], [3, 5],
                    [4, 2], [4, 3], [4, 4], [4, 5],
                    [5, 2], [5, 3], [5, 4], [5, 5]]

    DIRECTION = [[-1, -1], [-1, 0], [-1, 1],
                 [0, -1], [0, 1],
                 [1, -1], [1, 0], [1, 1]]

    # Aliases
    BORDER = CORNER + BORDER_ADVANTAGE + BORDER_DISADVANTAGE
    ADVANTAGE = CORNER + BORDER_ADVANTAGE
    QUESTIONABLE = BORDER_DISADVANTAGE
    DISADVANTAGE = INNER_DISADVANTAGE + BORDER_DISADVANTAGE
    NORMAL = INNER_NORMAL


class Utilities:
    """
    Contains optional static methods as helpers

    """

    @staticmethod
    def calc_matrix_score(matrix):
        """Calculate the score of current matrix

        :matrix: matrix
        :returns: list of score [player, computer]

        """
        p_score = 0
        c_score = 0

        for row in range(8):
            for col in range(8):
                if matrix[row][col] == 1:
                    p_score += 1
                elif matrix[row][col] == 2:
                    c_score += 1

        return [p_score, c_score]

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
    def get_current_time(format="%H:%M:%S %d/%m/%Y"):
        return time.strftime(format)

    @staticmethod
    def get_random_number(start, end):
        """Get random integer number in given range

        :returns: Random integer number in given range

        """
        return random.randint(start, end)

    @staticmethod
    def sort_position_list(positions):
        """ Sort input positions to order: advantage > disadvantage > normal

        :positions: List of positions in format [x, y]
        :returns: Sorted list

        """
        sorted_list = []

        # Add cornered positions
        for p in positions:
            if p in Field.CORNER:
                sorted_list.append(p)
                positions.remove(p)

        # Add advantage positions
        for p in positions:
            if p in Field.BORDER_ADVANTAGE:
                sorted_list.append(p)
                positions.remove(p)

        # Add disadvantage positions of borders
        for p in positions:
            if p in Field.BORDER_DISADVANTAGE:
                sorted_list.append(p)
                positions.remove(p)

        # Add disadvantage positions
        for p in positions:
            if p in Field.DISADVANTAGE:
                sorted_list.append(p)
                positions.remove(p)

        # Add remains (normals)
        sorted_list += positions

        return sorted_list

    @staticmethod
    def calc_value(player, value):
        """Re-assign the value based on which player is on.

        :player: Player
        :value: Value of player
        :returns: Positive number if player is computer, else negative

        """
        return value if player == Player.COMPUTER else -value

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
        """ Deprecated """
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

        # Check for each direction and move forward to find the path
        for x_direction, y_direction in Field.DIRECTION:
            x_forward, y_forward = x, y
            x_forward += x_direction
            y_forward += y_direction

            if Game.is_on_matrix([x_forward, y_forward]) \
                    and matrix[x_forward][y_forward] == other_tile:
                x_forward += x_direction
                y_forward += y_direction

                if not Game.is_on_matrix([x_forward, y_forward]):
                    continue

                while matrix[x_forward][y_forward] == other_tile:
                    x_forward += x_direction
                    y_forward += y_direction

                    if not Game.is_on_matrix([x_forward, y_forward]):
                        break

                if not Game.is_on_matrix([x_forward, y_forward]):
                    continue

                if matrix[x_forward][y_forward] == tile:
                    while True:
                        x_forward -= x_direction
                        y_forward -= y_direction

                        if x_forward == x and y_forward == y:
                            break

                        flips.append([x_forward, y_forward])

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
    def get_nearby_borders(position, matrix):
        """Get nearby available positions which is on border

        :position: Position in format [x, y]
        :matrix: Current matrix

        """
        relatives = []

        for x_direction, y_direction in Field.DIRECTION:
            x, y = position[:]
            x_forward = x + x_direction
            y_forward = y + y_direction

            if Game.is_on_borderline(position) and \
                    matrix[x_forward, y_forward] == 0:
                relatives.append([x_forward, y_forward])

        return relatives

    @staticmethod
    def make_move(player, position, matrix):
        """Make move at the given position

        :player: Player who makes move
        :position: Position [x, y] to make move on
        :matrix: Matrix to make move on, can be virtual one
        :returns: Length of flipped pieces. False if move can't be made.

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
