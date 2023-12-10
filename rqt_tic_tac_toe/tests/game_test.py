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
import pytest

from rqt_tic_tac_toe.game import Game
from rqt_tic_tac_toe_msgs.msg import Marker


def test_initialize_board_size():
    game = Game(board_size=3)
    assert game.get_board_size() == 3

    game = Game(board_size=0)
    assert game.get_board_size() == 2


def test_set_marker():
    game = Game(board_size=2, first_marker=Marker.O)
    assert game.get_present_marker() == Marker.O

    # Setting marker on out of range position should fail
    assert game.set_marker(-1, 0) is False
    assert game.set_marker(0, 2) is False
    assert game.get_present_marker() == Marker.O

    assert game.set_marker(0, 0) is True
    assert game.get_present_marker() == Marker.X
    # Setting marker on already set position should fail
    assert game.set_marker(0, 0) is False
    assert game.get_present_marker() == Marker.X

    assert game.set_marker(1, 0) is True
    assert game.get_present_marker() == Marker.O

    assert game.set_marker(0, 1) is True
    assert game.set_marker(1, 1) is True


def test_create_new_game():
    game = Game(board_size=2, first_marker=Marker.O)

    game.set_marker(0, 0)
    game.set_marker(1, 0)
    game.set_marker(1, 1)
    game.set_marker(0, 1)

    game = game.create_new_game(board_size=2, first_marker=Marker.X)

    expected = numpy.array([[Marker.NONE, Marker.NONE], [Marker.NONE, Marker.NONE]])
    assert numpy.array_equal(game.get_board_markers(), expected)
    assert game.get_present_marker() == Marker.X


def test_get_board_markers():
    game = Game(board_size=2, first_marker=Marker.O)

    # Board markers should be:
    # O X
    # X O
    game.set_marker(0, 0)
    game.set_marker(1, 0)
    game.set_marker(1, 1)
    game.set_marker(0, 1)

    expected = numpy.array([[Marker.O, Marker.X], [Marker.X, Marker.O]])
    assert numpy.array_equal(game.get_board_markers(), expected)


def test_calc_winner():
    game = Game(board_size=2, first_marker=Marker.O)

    assert game.calc_winner()[0] == Marker.NONE

    game.set_marker(0, 0)
    assert game.calc_winner()[0] == Marker.NONE

    game.set_marker(1, 0)
    assert game.calc_winner()[0] == Marker.NONE

    game.set_marker(1, 1)
    assert game.calc_winner()[0] == Marker.O


def test_winner_line():
    # Row line
    # X
    # O O
    game = Game(board_size=2, first_marker=Marker.O)
    game.set_marker(1, 0)
    game.set_marker(0, 0)
    game.set_marker(1, 1)
    assert game.calc_winner()[1] == [(1, 0), (1, 1)]

    # Column line
    #   O
    # X O
    game = game.create_new_game(board_size=2, first_marker=Marker.O)
    game.set_marker(0, 1)
    game.set_marker(1, 0)
    game.set_marker(1, 1)
    assert game.calc_winner()[1] == [(0, 1), (1, 1)]

    # Diagonal line
    # 0 X
    #   O
    game = game.create_new_game(board_size=2, first_marker=Marker.O)
    game.set_marker(1, 1)
    game.set_marker(0, 1)
    game.set_marker(0, 0)
    assert game.calc_winner()[1] == [(0, 0), (1, 1)]

    # Diagonal line
    # X O
    # O
    game = game.create_new_game(board_size=2, first_marker=Marker.O)
    game.set_marker(1, 0)
    game.set_marker(0, 0)
    game.set_marker(0, 1)
    assert game.calc_winner()[1] == [(0, 1), (1, 0)]


def test_board_is_full():
    game = Game(board_size=2)

    assert game.board_is_full() is False

    game.set_marker(0, 0)
    game.set_marker(1, 0)
    game.set_marker(1, 1)
    game.set_marker(0, 1)

    assert game.board_is_full() is True
