#!/usr/bin/env python3

from reversi.game import Game, Player, Utilities


class Algorithm:

    @staticmethod
    def do_minimax(depth, matrix, player, avail_moves):
        """ Do minimax algorithm to find the best move for computer

        :depth: Current depth level. Minimum is 0.
        :matrix: Current matrix state.
        :player: Current player. Depend on the current player, algorithm
                 used will be switched.
        :avail_moves: List of available moves for current player.
        :returns: Move in format [[x, y] val] with highest value

        """

        # Raise exception (unhandled case)
        if len(avail_moves) == 0:
            raise Exception("Encountered Error!")

        result_list = []

        # Determine the opponent
        if player == Player.PLAYER:
            opponent = Player.COMPUTER
        else:
            opponent = Player.PLAYER

        # Reached to the deepest part of the given tree
        if depth == 0:
            # Calculate all of the node's values and return the one
            # with highest value
            for position in avail_moves:
                val = Game.calc_val_of_move(player, position, matrix)

                # Reverse score to negative if the current player is human
                if player == Player.PLAYER:
                    val = -val

                result_list.append([position, val])

            return Game.get_move_with_highest_score(result_list)

        # In a normal state of tree.
        for position in avail_moves:
            matrix_virtual = Utilities.clone_matrix(matrix)
            val = Game.make_move(player, position, matrix_virtual)

            # Check if opponent has move on the virtual matrix
            opponent_moves = Game.get_available_moves(opponent, matrix_virtual)

            if len(opponent_moves) == 0:

                # Check if the player has move on the virtual matrix
                player_moves = Game.get_available_moves(player, matrix_virtual)

                if len(player_moves) == 0:
                    # Both has no move, reached to the end game.
                    # Calculate the value of the current node and shift
                    # to the next position.
                    # TODO recheck score calculation method
                    # TODO possible to trim down the tree right here
                    result_list.append([position, val + 1])
                    continue

                # Opponent has no moves at this point.
                # One extra move for current player.
                # TODO possible to push the value to next virtual turn
                best_move = Algorithm.do_minimax(depth - 1, matrix_virtual,
                                                 player, player_moves)
                result_list.append(best_move)
                continue

            # Opponent has move. Process normally.
            best_move = Algorithm.do_minimax(depth - 1, matrix_virtual,
                                             opponent, opponent_moves)
            result_list.append(best_move)

        return Game.get_move_with_highest_score(result_list)
