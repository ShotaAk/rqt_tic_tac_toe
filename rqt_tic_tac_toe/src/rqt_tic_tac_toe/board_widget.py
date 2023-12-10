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

from python_qt_binding.QtCore import QPointF
from python_qt_binding.QtCore import QRectF
from python_qt_binding.QtCore import QSizeF
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtGui import QColor
from python_qt_binding.QtGui import QPainter
from python_qt_binding.QtGui import QPen
from python_qt_binding.QtWidgets import QWidget
from rqt_tic_tac_toe_msgs.msg import Marker


class BoardWidget(QWidget):

    def __init__(self, parent=None):
        super(BoardWidget, self).__init__(parent)
        self._INVALID_POINT = QPointF(-1.0, -1.0)
        self._DRAW_METHODS = {
            Marker.O: self._draw_marker_O,
            Marker.X: self._draw_marker_X,
            Marker.NONE: self._draw_marker_none
        }

        self._board_area_size = QSizeF(self.rect().size()) 
        self._mouse_clicked_point = self._INVALID_POINT

        self._board_size = 3
        self._board_markers = numpy.full((self._board_size, self._board_size), Marker.NONE)
        self._winner_line = []

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        # Set background color
        painter.setBrush(QColor('floralwhite'))
        painter.drawRect(self.rect())

        self._draw_board(painter)
        self._draw_markers(painter)
        if self._winner_line:
            self._draw_winner_line(painter)

    def resizeEvent(self, event) -> None:
        self._resize_board_area()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self._mouse_clicked_point = event.localPos()

    def set_board_size(self, board_size: int) -> None:
        self._board_size = board_size

    def set_board_markers(self, board: numpy.ndarray) -> None:
        self._board_markers = board

    def set_winner_line(self, winner_line: list) -> None:
        self._winner_line = winner_line

    def pop_mouse_clicked_pos(self) -> tuple[int, int]:
        INVALID_POS = (-1, -1)

        row = (self._mouse_clicked_point.y() / self._board_area_size.height())
        col = (self._mouse_clicked_point.x() / self._board_area_size.width())
        if row < 0.0 or row >= 1.0 or col < 0.0 or col >= 1.0:
            return INVALID_POS

        self._mouse_clicked_point = self._INVALID_POINT
        return (int(row*self._board_size), int(col*self._board_size))

    def _resize_board_area(self) -> None:
        # Change the board area to fit the widget

        # Board area must be square
        area_size = float(min(self.width(), self.height()))
        self._board_area_size = QSizeF(area_size, area_size)

    def _to_center_of_block(self, row: int, col: int) -> QPointF:
        return QPointF(
            (col + 0.5) * self._board_area_size.width() / self._board_size,
            (row + 0.5) * self._board_area_size.height() / self._board_size
        )

    def _to_line_size(self, size: int) -> int:
        SIZE_RATE = 200.0
        output = int(size * self._board_area_size.width() / SIZE_RATE)
        if output < 1:
            return 1
        return output

    def _draw_board(self, painter: QPainter) -> None:
        COLOR_BACKGROUND = QColor('black')
        COLOR_LINE = QColor('white')

        # Draw the board
        painter.setBrush(COLOR_BACKGROUND)
        rect = QRectF(QPointF(0.0, 0.0), self._board_area_size)
        painter.drawRect(rect)

        for i in range(self._board_size - 1):
            # Draw horizontal lines
            painter.setPen(COLOR_LINE)
            painter.drawLine(
                QPointF(0.0, (i + 1) * self._board_area_size.height() / self._board_size),
                QPointF(self._board_area_size.width(), (i + 1) * self._board_area_size.height() / self._board_size)
            )

            # Draw vertical lines
            painter.setPen(QColor('white'))
            painter.drawLine(
                QPointF((i + 1) * self._board_area_size.width() / self._board_size, 0.0),
                QPointF((i + 1) * self._board_area_size.width() / self._board_size, self._board_area_size.height())
            )

    def _draw_markers(self, painter: QPainter) -> None:
        for (row, col), marker in numpy.ndenumerate(self._board_markers):
            self._DRAW_METHODS[marker](painter, row, col)

    def _draw_marker_none(self, painter: QPainter, row: int, col: int) -> None:
        pass

    def _draw_marker_O(self, painter: QPainter, row: int, col: int) -> None:
        COLOR_LINE = QColor('tomato')
        COLOR_FILL = QColor('white')
        COLOR_FILL.setAlphaF(0.0)
        LINE_SIZE = self._to_line_size(10)

        painter.setPen(QPen(COLOR_LINE, LINE_SIZE))
        painter.setBrush(COLOR_FILL)

        center = self._to_center_of_block(row, col)
        radius = self._board_area_size.width() / self._board_size / 2.0
        painter.drawEllipse(center, radius, radius)

    def _draw_marker_X(self, painter: QPainter, row: int, col: int) -> None:
        COLOR_LINE = QColor('deepskyblue')
        COLOR_FILL = QColor('white')
        COLOR_FILL.setAlphaF(0.0)
        LINE_SIZE = self._to_line_size(10)

        painter.setPen(QPen(COLOR_LINE, LINE_SIZE))
        painter.setBrush(COLOR_FILL)

        start = QPointF(
            col * self._board_area_size.width() / self._board_size,
            row * self._board_area_size.height() / self._board_size
        )
        end = QPointF(
            (col + 1) * self._board_area_size.width() / self._board_size,
            (row + 1) * self._board_area_size.height() / self._board_size
        )
        painter.drawLine(start, end)

        start = QPointF(
            (col + 1) * self._board_area_size.width() / self._board_size,
            row * self._board_area_size.height() / self._board_size
        )
        end = QPointF(
            col * self._board_area_size.width() / self._board_size,
            (row + 1) * self._board_area_size.height() / self._board_size
        )
        painter.drawLine(start, end)

    def _draw_winner_line(self, painter: QPainter) -> None:
        COLOR_LINE = QColor('gold')
        LINE_SIZE = self._to_line_size(20)

        painter.setPen(QPen(COLOR_LINE, LINE_SIZE))

        start = self._to_center_of_block(self._winner_line[0][0], self._winner_line[0][1])
        end = self._to_center_of_block(self._winner_line[1][0], self._winner_line[1][1])
        painter.drawLine(start, end)
