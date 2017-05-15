#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Ji Yang <jyang7@ualberta.ca>
# License: MIT
# Version: 1.1.0
# Last Updated: May 15, 2017

import sys
import csv
import random
from functools import reduce

class Game2048:
    """The game 2048.

    Each instance is a unique 2048 game that can be used for training our model later on.

    Parameters
    ----------
    upper_bound : int, optional (default=20)
        This value will be used for generating a mapping for beautiful print of game boards.
        If 20, we will generate a map(dict) contains key-value pair from '2': '2' to '524288': '524288'.
        This value has to be greater than 10 in order to have a minimal map for a 2048 game.

    Attributes
    ----------
    row : int
        The number of rows for the game board.
    col : int
        The number of columns for the game board.
    board : list of lists
        The game board in form of [[row1], [row2], [row3], [row4]] with `row` is set to 4.
    score : int
        The game score.
    end : bool
        Whether the game is ended.
    """

    def __init__(self, upper_bound=20):
        assert upper_bound > 10
        self.row = 4
        self.col = 4
        self.board = self._generate_board()
        self.score = 0
        self.end = False
        self._moves = [0, 1, 2, 3]
        self._mapping = self._generate_mapping(upper_bound)
        self._fill_random_empty_tile()
        self._fill_random_empty_tile()

    def _is_empty_tile(self, tile):
        """Return whether the given tile is empty"""
        return tile == 0

    def _add_score(self, new):
        """Set the score by adding the new score to the current."""
        self.score += new

    def _generate_board(self):
        """Generate a empty game board."""
        return [[0 for _ in range(self.col)] for _ in range(self.row)]

    def _generate_mapping(self, upper_bound):
        """Generate a game value map for printing."""
        # TODO: support customized mapping (not a feature for AI)
        mapping = {str(2 ** power): str(2 ** power) for power in range(1, upper_bound)}
        return reduce(lambda x, y: dict(x, **y), ({'0': '0'}, mapping))

    def _get_empty_tiles(self):
        """Get coordinates of all empty tiles(in format of [col, row])"""
        empty_tiles = []
        for y in range(self.row):
            for x in range(self.col):
                if self._is_empty_tile(self.board[y][x]):
                    empty_tiles.append([y, x])

        return empty_tiles

    def _get_num_empty_tiles(self):
        """Get the number of empty tiles remain on the board"""
        return len(self._get_empty_tiles())

    def _fill_random_empty_tile(self):
        """Randomly fill an empty tile with 2 or 4, prob 90% and 10%, respectively"""
        empty_tiles = self._get_empty_tiles()
        if empty_tiles:
            [i, j] = random.choice(empty_tiles)
            self.board[i][j] = 4 if random.random() > 0.9 else 2

    def _is_mergeable(self):
        """Return whether there exists tiles are mergeable"""

        def is_adjacent_equal(arr):
            """Return whether there exists adjacent tiles have an identical value"""
            if len(arr) is 1:
                return True

            for idx in range(len(arr) - 1):
                if arr[idx] == arr[idx + 1]:
                    return True

            return False

        def check_all_rows_mergeable():
            """Check mergebility for each row"""
            for row_idx in range(self.row):
                row = []
                for i in self.board[row_idx]:
                    if i != 0:
                        row.append(i)
            return is_adjacent_equal(row)

        def check_all_columns_mergeable():
            """Check mergebility for each column"""
            for col_idx in range(self.col):
                col = []
                for i in self.board:
                    if i[col_idx] != 0:
                        col.append(i[col_idx])

            return is_adjacent_equal(col)

        if self._get_num_empty_tiles() != 0:
            return True

        return check_all_rows_mergeable() or check_all_columns_mergeable()

    def _merge(self, arr, direction):
        """Merge tiles in rows and columns by given direction

        Parameters
        ----------
        arr : list
            A list represents a row/column. For example, [2, 2, 0, 0] could represent a row/column.
        direction: bool
            The direction of merging.
            If True, merge a row to the left or merge a column to the top.
            If False, merge a row to the right or merge a column to the bottom.

        Return
        ----------
        tuple
            The first element is the merged row/column.
            The second element represents whether the merge does change the board.
        """

        def squeeze():
            """Get rid of 0s in the row/column"""
            nonlocal store, arr
            for i in arr:
                if i != 0:
                    store.append(i)

        store = []
        squeeze()

        # If there is only 1 non-zero tiles, no need to do further work
        if len(store) is 1:
            result = [0 for _ in range(len(arr))]
            # To the left/top
            if direction:
                result[0] = store[0]
            # To the right/bottom
            else:
                result[-1] = store[0]
            return result, not arr == result

        # Reverse if we are performing a right/downward merge
        if not direction:
            store = store[::-1]
        # Handle special cases where we have [A, A, B, B] in a row/column
        # A and B could be identical
        if len(store) is 4 and store[0] == store[1] and store[2] == store[3]:
            store = [store[0] * 2, store[2] * 2]
        else:
            # Merge identical neighbors
            for idx in range(len(store) - 1):
                if store[idx] == store[idx + 1]:
                    store[idx] *= 2
                    self._add_score(store[idx + 1] * 2)
                    store.pop(idx + 1)
                    break

        # Reverse it back if we are performing a right/downward merge
        if not direction:
            store = store[::-1]
        # Keep a length of 4 for a row/column
        while len(store) < len(arr):
            store.append(0) if direction else store.insert(0, 0)

        return store, not arr == store

    def _horizontally_merge(self, direction):
        """Merge all rows"""
        # Set a flag to tell whether we need to fill an empty tile
        should_fill = False
        for i in range(0, len(self.board)):
            self.board[i], changed = self._merge(self.board[i], direction)
            # If there is any row has been changed after a merge
            if changed:
                should_fill = True
        # Fill an empty tile if this merge changes the game state
        if should_fill:
            self._fill_random_empty_tile()

    def _vertically_merge(self, direction):
        """Merge all columns"""

        def update_column_by_index(idx, col):
            """Update all columns after merging"""
            for row_idx in range(len(self.board)):
                self.board[row_idx][idx] = col[row_idx]

        # Set a flag to tell whether we need to fill an empty tile
        should_fill = False
        for col_idx in range(self.col):
            # Construct columns
            column = [i[col_idx] for i in self.board]
            merged_column, changed = self._merge(column, direction)
            # If there is any column has been changed after a merge
            if changed:
                should_fill = True
            update_column_by_index(col_idx, merged_column)
        if should_fill:
            self._fill_random_empty_tile()

    def perform_move(self, move):
        """Perform a move on the game board"""
        assert move in self._moves
        # 0 for UP, 1 for DOWN, 2 for LEFT, 3 for RIGHT
        if move == 0:
            self._horizontally_merge(True)
        elif move == 1:
            self._horizontally_merge(False)
        elif move == 2:
            self._vertically_merge(True)
        elif move == 3:
            self._vertically_merge(False)

    def save_game_info(self):
        """Save the game info we need for further statistics"""
        tiles = [item for sublist in self.board for item in sublist]
        best_tile = max(tiles)
        with open('result.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow([self.score, best_tile])

    def is_lost(self):
        """Return True if the game is ended"""
        return not self._is_mergeable()

    def print_game(self):
        """Print the game board"""
        for row in self.board:
            print(row)

    def beautiful_print(self):
        """Print the game board gracefully"""
        for row in self.board:
            print('{}-'.format('------' * self.col))
            for entry in row:
                print('|', end='')
                print(self._mapping[str(entry)].center(4, ' '), end=' ')
            print('|')
        print('{}-'.format('------' * self.col))
        print('Score: {}\nEmpty Tiles: {}'.format(
            self.score, self._get_num_empty_tiles()))
        print('{}-'.format('------' * self.col))


def request_move():
    """ONLY for human players"""
    direction = input('Enter a direction: ')
    if direction.upper() == 'Q':
        print('Force quit, bye bye~')
        sys.exit(0)
    else:
        if direction.upper() == 'A':
            game.perform_move(0)
        elif direction.upper() == 'D':
            game.perform_move(1)
        elif direction.upper() == 'W':
            game.perform_move(2)
        elif direction.upper() == 'S':
            game.perform_move(3)


if __name__ == '__main__':
    global game
    game = Game2048()
    while True:
        game.print_game()
        if game.is_lost():
            print('Game ended.')
            break
        else:
            request_move()
