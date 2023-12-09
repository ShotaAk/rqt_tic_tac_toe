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
from python_qt_binding.QtWidgets import QWidget
from rqt_gui_py.plugin import Plugin


class TicTacToe(Plugin):

    def __init__(self, context):
        super(TicTacToe, self).__init__(context)
        self.setObjectName('TicTacToe')

        self._node = context.node
        self._logger = self._node.get_logger()

        self._widget = QWidget()
        ui_file = os.path.join(get_package_share_directory('rqt_tic_tac_toe'),
                               'resource', 'TicTacToeWidget.ui')
        loadUi(ui_file, self._widget)  # Need to set custom widget

        # Add widget to rqt window
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)

    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        pass
