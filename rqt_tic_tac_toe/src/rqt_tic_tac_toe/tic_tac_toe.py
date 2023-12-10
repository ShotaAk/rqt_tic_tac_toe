#!/usr/bin/env python

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

import os

from ament_index_python.packages import get_package_share_directory
from python_qt_binding import loadUi
from python_qt_binding.QtCore import QTimer
from python_qt_binding.QtWidgets import QWidget
from rqt_gui_py.plugin import Plugin
from rqt_tic_tac_toe.board_widget import BoardWidget
from rqt_tic_tac_toe.game import Game
from rqt_tic_tac_toe_msgs.msg import Marker


class TicTacToe(Plugin):

    def __init__(self, context):
        super(TicTacToe, self).__init__(context)
        self.setObjectName('TicTacToe')

        self._node = context.node
        self._logger = self._node.get_logger()

        self._widget = QWidget()
        ui_file = os.path.join(get_package_share_directory('rqt_tic_tac_toe'),
                               'resource', 'TicTacToeWidget.ui')
        loadUi(ui_file, self._widget, {'BoardWidget': BoardWidget})  # Need to set custom widget

        # Add widget to rqt window
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

        self._game = Game(board_size=3, first_marker=Marker.O)
        self._widget.BoardWidget.set_board_size(self._game.get_board_size())

        self._widget.ResetButton.clicked.connect(self._reset_game)

        # Update board_widget at 60 Hz
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_game)
        self._timer.timeout.connect(self._widget.BoardWidget.update)
        self._timer.timeout.connect(self._update_ui)
        self._timer.start(16)

    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        pass

    def _update_ui(self):
        self._widget.GameStatusLabel.setText(
            self._game_status_text())

    def _update_game(self):
        winner, winner_line = self._game.calc_winner()
        if winner != Marker.NONE:
            self._widget.BoardWidget.set_winner_line(winner_line)
        self._widget.BoardWidget.set_board_markers(self._game.get_board_markers())

        if winner != Marker.NONE or self._game.board_is_full():
            return

        clicked_pos = self._widget.BoardWidget.pop_mouse_clicked_pos()
        if clicked_pos[0] < 0 or clicked_pos[1] < 0:
            return
        self._game.set_marker(clicked_pos[0], clicked_pos[1])

    def _game_status_text(self):
        winner, winner_line = self._game.calc_winner()
        if winner != Marker.NONE:
            return 'Winner: {}'.format(winner)

        if self._game.board_is_full():
            return 'Draw'

        present_marker = self._game.get_present_marker()

        return 'Present: {}'.format(present_marker)

    def _reset_game(self):
        self._game = self._game.create_new_game(board_size=3, first_marker=Marker.O)
        self._widget.BoardWidget.set_board_size(self._game.get_board_size())
        self._widget.BoardWidget.set_board_markers(self._game.get_board_markers())
        self._widget.BoardWidget.reset_winner_line()
        self._widget.BoardWidget.pop_mouse_clicked_pos()

