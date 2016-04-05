#!/usr/bin/env python3

from reversi.game import Game, Player, Utilities, Field


class Algorithm:

    @staticmethod
    def do_shallow_scan(matrix, player, avail_moves, get_all=False):
        """ Make a shallow scan on the surface of matrix and calculate
        the scores.

        :matrix: Matrix to check
        :player: Current player
        :avail_moves: Available move list for current player
        :get_all: Returning the whole list with scores, can be used to show
        hints on matrix. Default: False.
        :returns: pair with highest value in format [[x, y], val].
        If get_all is enabled, all of the positions in avail_moves with scores
        will be returned instead.

        """
        # Raise exception (unhandled case)
        if not avail_moves:
            raise Exception("Encountered Error!")

        for position in avail_moves:
            val = Game.calc_val_of_move(player, position, matrix)
            result_list.append([position,
                                Utilities.calc_value(player, val)])

        if get_all:
            return result_list

        return Game.get_best_pair(result_list)

    @staticmethod
    def do_minimax(depth, matrix, player, avail_moves):
        """ Do a plain minimax scan on the matrix for best pair.
        CAUTION: Should not use with high depth.

        :depth: Current depth level. Minimum is 0.
        :matrix: Current matrix state.
        :player: Current player.
        :avail_moves: List of available moves for current player.
        :returns: Move in format [[x, y] val] with highest value

        """
        # Raise exception (unhandled case)
        if not avail_moves:
            raise Exception("Encountered Error!")

        result_list = []

        # Determine the opponent
        if player == Player.PLAYER:
            opponent = Player.COMPUTER
        else:
            opponent = Player.PLAYER

        #
        # Reached to the deepest part of the given tree
        #

        if depth == 0:
            # Calculate all of the node's values and return the one
            # with highest value
            for position in avail_moves:
                val = Game.calc_val_of_move(player, position, matrix)
                result_list.append([position,
                                    Utilities.calc_value(player, val)])

            return Game.get_best_pair(result_list)

        for position in avail_moves:
            matrix_virtual = Utilities.clone_matrix(matrix)
            val = Game.make_move(player, position, matrix_virtual)

            # Check for next turn
            opponent_moves = Game.get_available_moves(opponent, matrix_virtual)

            if not opponent_moves:
                # Check if the player has move on the virtual matrix
                player_moves = Game.get_available_moves(player, matrix_virtual)

                if not player_moves:
                    # Both has no move, reached to the end game.
                    player_val, computer_val = \
                        Utilities.calc_matrix_score(matrix_virtual)

                    # TODO recheck fixed value
                    # Set priority of end game with win flag on top
                    if computer_val > player_val:
                        return [position, 64]

                    # TODO recheck fixed value
                    if player_val > computer_val:
                        val = -64

                    result_list.append([
                        position, Utilities.calc_value(player, val)
                    ])
                    continue

                # Opponent has no moves at this point
                # One extra move for current player
                best_move = Algorithm.do_minimax(depth - 1, matrix_virtual,
                                                 opponent, opponent_moves)
                result_list.append([position, best_move[1]])

            # Opponent has move. Process normally.
            best_move = Algorithm.do_minimax(depth - 1, matrix_virtual,
                                             opponent, opponent_moves)
            result_list.append([position, best_move[1]])

        return Game.get_best_pair(result_list)

    @staticmethod
    def do_alpha_beta_pruning(depth, matrix, player, avail_moves):
        """ Do minimax algorithm with alpha-beta pruning to reduce analysis
        time and improve AI level.

        :depth: Current depth level. Minimum is 0.
        :matrix: Current matrix state.
        :player: Current player. Depend on the current player, algorithm
                 used will be switched.
        :avail_moves: List of available moves for current player.
        :returns: Move in format [[x, y] val] with highest value

        """

        # Raise exception (unhandled case)
        if not avail_moves:
            raise Exception("Encountered Error!")

        result_list = []

        # Determine the opponent
        if player == Player.PLAYER:
            opponent = Player.COMPUTER
        else:
            opponent = Player.PLAYER

        #
        # Reached to the deepest part of the given tree
        #

        if depth == 0:
            # Calculate all of the node's values and return the one
            # with highest value
            for position in avail_moves:
                val = Game.calc_val_of_move(player, position, matrix)
                result_list.append([position,
                                    Utilities.calc_value(player, val)])

            return Game.get_best_pair(result_list)

        #
        # On the normal state of tree.
        #

        # Sort input
        avail_moves = Utilities.sort_position_list(avail_moves)

        # Start to check input for actions
        for position in avail_moves:
            # Corner field. Get it at all costs!
            if position in Field.ADVANTAGE:
                val = Game.calc_val_of_move(player, position, matrix)
                return [position, Utilities.calc_value(player, val)]

            # Disadvantage field. Handle with cares.
            if position in Field.DISADVANTAGE:
                # Get player's flips and score
                player_flips = Game.get_flip_traces(player, position, matrix)
                player_flips.append(position)
                matrix_virtual = Utilities.clone_matrix(matrix)
                player_val = Game.make_move(player, position, matrix_virtual)

                # Dig down 1 level
                # Get opponent's possible moves
                opponent_moves = Game.get_available_moves(opponent,
                                                          matrix_virtual)
                max_penalty = None

                # Check if any of player's flip is on the way of opponent
                for p in opponent_moves:
                    # Who cares if opponent doesn't wanna take border?
                    if p not in Field.BORDER:
                        continue

                    opponent_flips = Game.get_flip_traces(opponent, p,
                                                          matrix_virtual)

                    for f in player_flips:
                        if f in opponent_flips:
                            if max_penalty is None or \
                                    max_penalty < (len(opponent_flips) + 1):
                                max_penalty = len(opponent_flips) + 1

                if max_penalty is None:
                    # No danger thread. Take the advantage of border
                    if position in Field.BORDER_DISADVANTAGE:
                        return [position,
                                Utilities.calc_value(player, player_val)]
                    else:
                        # Pass to next case (normal field)
                        pass
                else:
                    result_list.append([
                        position,
                        Utilities.calc_value(player, player_val - max_penalty)
                    ])

            # Normal field
            # Check if opponent has move on the virtual matrix
            matrix_virtual = Utilities.clone_matrix(matrix)
            val = Game.make_move(player, position, matrix_virtual)

            # Check for next turn
            opponent_moves = Game.get_available_moves(opponent, matrix_virtual)

            if not opponent_moves:
                # Check if the player has move on the virtual matrix
                player_moves = Game.get_available_moves(player, matrix_virtual)

                if not player_moves:
                    # Both has no move, reached to the end game.
                    player_val, computer_val = \
                        Utilities.calc_matrix_score(matrix_virtual)

                    # TODO recheck fixed value
                    # Set priority of end game with win flag on top
                    if computer_val > player_val:
                        return [position, 64]

                    # TODO recheck fixed value
                    if player_val > computer_val:
                        val = -64

                    result_list.append([
                        position, Utilities.calc_value(player, val)
                    ])
                    continue

                # Opponent has no moves at this point
                # One extra move for current player
                # Set priority to top.
                # TODO recheck fixed value
                result_list.append([position,
                                    Utilities.calc_value(player, 32)])
                continue

            # Opponent has move. Process normally.
            best_move = Algorithm.do_alpha_beta_pruning(
                depth - 1, matrix_virtual, opponent, opponent_moves
            )
            result_list.append([position, best_move[1]])

        return Game.get_best_pair(result_list)
