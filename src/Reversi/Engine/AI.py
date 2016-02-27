#!/usr/bin/env python3

from copy import deepcopy
from Reversi.Engine.Game import Player


class Algorithm():

    def __init__(self):
        pass

    def do_alpha_beta_pruning(self, max_depth, matrix, avail_moves):
        """Using alpha-beta pruning algorithm to search for the best move
        for the computer

        :max_depth: max depth
        :matrix: matrix
        :avail_moves: available moves for the current matrix
        :returns: move in format list [x, y]

        """
        return self.__get_max_algorithm(max_depth, 1, matrix, avail_moves)

    def __get_max_algorithm(self, max_depth, depth, matrix, avail_moves):
        """Get max value of given matrix

        :max_depth: max depth to check
        :depth: current depth level
        :matrix: matrix to check
        :*avail_moves: available moves for the given matrix
        :returns: [[x, y] val]

        """
        print("==========GET_MAX_ALG==========")
        print("depth", depth)
        print("avail_moves", avail_moves[:])

        if len(avail_moves) == 0:
            return False

        if depth == max_depth:
            result_list = []

            for move in avail_moves[:]:
                print("for move in avail_moves")
                val = self.__calc_matrix_val(move, Player.COMPUTER, matrix)
                print("move", move, "val", val)
                result_list.append([move, val])

            print("result_list", result_list)

            if len(result_list) == 0:
                return False

            return self.__get_pair_with_highest_score(result_list)

        result_list = []

        for move in avail_moves[:]:
            print("for move in avail moves")
            print("move", move, "depth", depth)
            matrix_new = deepcopy(matrix)
            self.make_move(Player.COMPUTER, move, matrix_new)
            print("matrix_new", matrix[:])
            avail_moves_new = self.get_available_moves(matrix_new,
                                                       Player.PLAYER)

            if len(avail_moves_new) == 0:
                return False

            print("avail_moves_new", avail_moves_new[:])
            min_pair = self.__get_min_algorithm(max_depth, depth + 1,
                                                matrix_new, avail_moves_new)
            print("min_pair", min_pair[:])

            if min_pair is not False:
                result_list.append([move, min_pair[1]])

        print("result_list", result_list[:])

        return self.__get_pair_with_highest_score(result_list)  # TODO debug

    def __get_min_algorithm(self, max_depth, depth, matrix, avail_moves):
        """Get min value of given matrix

        :max_depth: max depth to check
        :depth: current depth level
        :matrix: matrix to check
        :*avail_moves: available moves for the given matrix
        :returns: [[x, y], val]

        """
        if len(avail_moves) == 0:
            return False

        if depth == max_depth:
            result_list = []

            for move in avail_moves[:]:
                val = self.__calc_matrix_val(move, Player.PLAYER, matrix)
                result_list.append([move, val])

            return self.__get_pair_with_lowest_score(result_list)

        result_list = []

        for move in avail_moves[:]:
            matrix_new = deepcopy(matrix)
            self.make_move(Player.PLAYER, move, matrix_new)
            avail_moves_new = self.get_available_moves(matrix_new,
                                                       Player.COMPUTER)

            if len(avail_moves_new) == 0:
                return False

            max_pair = self.__get_max_algorithm(max_depth, depth + 1,
                                                matrix_new, avail_moves_new)
            result_list.append([move, max_pair[1]])

        return self.__get_pair_with_lowest_score(result_list)

    def __get_pair_with_highest_score(self, pair_list):
        """Get pair with highest value

        :pair_list: list of moves and value in format [[x, y] val]
        :returns: pair with highest value in format [[x, y] val]

        """
        i_max = None
        val_max = None

        for i in range(len(pair_list)):
            val = pair_list[i][1]

            if (i_max is None and val_max is None) or (val > val_max):
                i_max = i
                val_max = val

        return pair_list[i_max]

    def __get_pair_with_lowest_score(self, pair_list):
        """Get pair with lowest value

        :pair_list: list of moves and value in format [[x, y] val]
        :returns: pair with lowest value in format [[x, y] val]

        """
        i_min = None
        val_min = None

        for i in range(len(pair_list)):
            val = pair_list[i][1]

            if (i_min is None and val_min is None) or (val < val_min):
                i_min = i
                val_min = val

        return pair_list[i_min]

    def __calc_matrix_val(self, move, current_player, matrix):
        """Calculate the value of given matrix with the given move

        :move: pair of [x, y]
        :current_player: current player
        :matrix: matrix
        :returns: int

        """
        x, y = move[:]
        flip = self.get_valid_moves(x, y, current_player, matrix)

        if len(flip) == 0:
            return 0

        return len(flip) + 1

    def get_valid_moves(self, x, y, current_player, matrix):
        """Get a list of valid moves for the current position

        :x: matrix row
        :y: matrix column
        :returns: List of valid moves for current turn and its tiles to flip

        """

        if matrix[x][y] != 0 or not self.is_on_matrix(matrix, x, y):
            return False

        tile = current_player

        if tile == Player.PLAYER:
            other_tile = Player.COMPUTER
        elif tile == Player.COMPUTER:
            other_tile = Player.PLAYER

        flip = []

        for x_direction, y_direction in [[-1, -1], [-1, 0], [-1, 1],
                                         [0, -1], [0, 1],
                                         [1, -1], [1, 0], [1, 1]]:
            x_start, y_start = x, y
            x_start += x_direction
            y_start += y_direction

            if self.is_on_matrix(matrix, x_start, y_start) \
                    and matrix[x_start][y_start] == other_tile:
                x_start += x_direction
                y_start += y_direction

                if not self.is_on_matrix(matrix, x_start, y_start):
                    continue

                while matrix[x_start][y_start] == other_tile:
                    x_start += x_direction
                    y_start += y_direction

                    if not self.is_on_matrix(matrix, x_start, y_start):
                        break

                if not self.is_on_matrix(matrix, x_start, y_start):
                    continue

                if matrix[x_start][y_start] == tile:
                    while True:
                        x_start -= x_direction
                        y_start -= y_direction

                        if x_start == x and y_start == y:
                            break

                        flip.append([x_start, y_start])

        if len(flip) == 0:
            return False

        return flip

    def is_on_matrix(self, matrix, x, y):
        """
        Check if current position is on matrix

        :x: matrix column
        :y: matrix row
        """
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False

        return True

    def get_available_moves(self, matrix, player):
        """Get available moves for the current player

        :matrix: matrix to check
        :player: current player
        :returns: list of available moves

        """

        moves = []

        for row in range(8):
            for col in range(8):
                if matrix[row][col] != 0:
                    continue

                if self.get_valid_moves(row, col, player, matrix) is not False:
                    moves.append([row, col])

        return moves

    def make_move(self, player, position, matrix):
        """TODO: Make move at the given position to given player

        :player: current player
        :position: list of [x, y]
        :returns: none

        """
        row, col = position[:]

        # Get flip list for current movement
        flip_stack = self.get_valid_moves(row, col, player, matrix)

        if flip_stack is False:
            return False

        # Fill the flip list and player moves in matrix
        for i in range(len(flip_stack)):
            x, y = flip_stack[i][:]
            matrix[x][y] = player

        matrix[row][col] = player

        return len(flip_stack)
