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


from python_qt_binding.QtCore import QPointF
from python_qt_binding.QtCore import QRectF
from python_qt_binding.QtCore import QSizeF
from python_qt_binding.QtGui import QColor
from python_qt_binding.QtGui import QPainter
from python_qt_binding.QtWidgets import QWidget


class BoardWidget(QWidget):

    def __init__(self, parent=None):
        super(BoardWidget, self).__init__(parent)

        self._board_area_size = QSizeF(self.rect().size()) 


    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        # Set background color
        painter.setBrush(QColor('floralwhite'))
        painter.drawRect(self.rect())

        self._draw_board(painter)

    def resizeEvent(self, event) -> None:
        self._resize_board_area()

    def _resize_board_area(self) -> None:
        # Change the board area to fit the widget

        # Board area must be square
        area_size = float(min(self.width(), self.height()))
        self._board_area_size = QSizeF(area_size, area_size)

    def _draw_board(self, painter: QPainter) -> None:
        # Draw the board
        painter.setBrush(QColor('black'))
        rect = QRectF(QPointF(0.0, 0.0), self._board_area_size)
        painter.drawRect(rect)
