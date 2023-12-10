# Copyright 2023 ShotaAk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy
from rqt_tic_tac_toe_msgs.msg import Marker


class Game():

    def __init__(self, board_size: int = 3,
                 markers: list = [Marker.O, Marker.X],
                 first_marker: Marker = Marker.O):

        self._BOARD_SIZE = max(board_size, 2)
        self._MARKERS = markers

        self._board = numpy.full((self._BOARD_SIZE, self._BOARD_SIZE), Marker.NONE)
        self._present_marker = first_marker

    def create_new_game(self, board_size: int, first_marker: Marker) -> 'Game':
        return Game(board_size, self._MARKERS, first_marker)

    def get_board_size(self) -> int:
        return self._BOARD_SIZE

    def get_board_markers(self) -> numpy.ndarray:
        return self._board

    def get_present_marker(self) -> Marker:
        return self._present_marker

    def set_marker(self, row: int, col: int) -> bool:
        # Setting marker on out of range position should fail
        if row < 0 or row >= self._BOARD_SIZE or col < 0 or col >= self._BOARD_SIZE:
            return False

        # Setting marker on already set position should fail
        if self._board[row][col] != Marker.NONE:
            return False

        self._board[row][col] = self._present_marker
        self._switch_present_marker()
        return True

    def board_is_full(self) -> bool:
        return bool(numpy.all(self._board != Marker.NONE))

    def calc_winner(self) -> tuple[Marker, list]:
        winner_line = []  # Start and end positions of the winner line

        # Check rows
        for row in range(self._BOARD_SIZE):
            if self._board[row][0] != Marker.NONE and numpy.all(self._board[row] == self._board[row][0]):
                winner_line = [(row, 0), (row, self._BOARD_SIZE - 1)]
                return self._board[row][0], winner_line

        # Check columns
        for col in range(self._BOARD_SIZE):
            if self._board[0][col] != Marker.NONE and numpy.all(self._board[:, col] == self._board[0][col]):
                winner_line = [(0, col), (self._BOARD_SIZE - 1, col)]
                return self._board[0][col], winner_line

        # Check diagonals
        if self._board[0][0] != Marker.NONE and numpy.all(numpy.diag(self._board) == self._board[0][0]):
            winner_line = [(0, 0), (self._BOARD_SIZE - 1, self._BOARD_SIZE - 1)]
            return self._board[0][0], winner_line

        if self._board[0][self._BOARD_SIZE - 1] != Marker.NONE and numpy.all(numpy.diag(numpy.fliplr(self._board)) == self._board[0][self._BOARD_SIZE - 1]):
            winner_line = [(0, self._BOARD_SIZE - 1), (self._BOARD_SIZE - 1, 0)]
            return self._board[0][self._BOARD_SIZE - 1], winner_line

        return Marker.NONE, winner_line

    def _switch_present_marker(self) -> None:
        self._present_marker = self._MARKERS[
            (self._MARKERS.index(self._present_marker) + 1) % len(self._MARKERS)]