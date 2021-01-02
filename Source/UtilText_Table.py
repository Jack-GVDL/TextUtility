from typing import *
from .UtilText_Screen import UtilText_Screen
from .UtilText_Component import UtilText_Component


class UtilText_Table(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# config
		# TODO: not yet completed: self._padding
		# self._padding:		List[int] = [0, 0, 0, 0]  # top, left, right, bottom
		self._separation:	List[int] = [0, 1, 1, 0]  # top, left, right, bottom

		# row info
		self._row_list:	List[List[UtilText_Component]] = []

		self._col_length_list:	List[int] = []
		self._row_length_list:	List[int] = []

		# data
		self._data = {
			"separation": self._separation
		}

		# render
		self._buffer_table: UtilText_Screen = UtilText_Screen()

		# operation
		self.addChild(self)

	def __del__(self):
		return

	# Operation
	# column
	def addRow(self, column_list: List[UtilText_Component]) -> bool:
		# row list
		self._row_list.append(column_list)

		# child / component list
		for component in column_list:
			self.addChild(component)

		return True

	# TODO: not yet completed
	def rmRow(self, index: int) -> bool:
		return False

	# TODO: not yet completed
	def resetRow(self) -> bool:
		return False

	# Protected
	def _getContent_(self) -> List[List[str]]:
		# reset table
		self._buffer_table.reset()
		self._buffer_table.expand((0, 0), (self._size[0], self._size[1]))

		# draw line
		# horizontal line
		# currently only one horizontal line
		self._buffer_table.fill(
			(0, self._row_length_list[0] + self._separation[0] + self._separation[3]),
			(self._size[0], 1),
			'-'
		)

		# vertical line
		cumulative_x: int = 0
		for index_col, col in enumerate(self._col_length_list):

			if index_col == len(self._col_length_list) - 1:
				continue

			# += separation - left
			# += width of this col
			# += separation - right
			cumulative_x += self._separation[1]
			cumulative_x += col
			cumulative_x += self._separation[2]

			# draw
			self._buffer_table.fill(
				(cumulative_x, 0),
				(1, self._size[1]),
				'|'
			)

			# vertical line
			cumulative_x += 1

		# intersection
		# currently only one horizontal line
		cumulative_x: int = 0
		for index_col, col in enumerate(self._col_length_list):

			if index_col == len(self._col_length_list) - 1:
				continue

			# += separation - left
			# += width of this col
			# += separation - right
			cumulative_x += self._separation[1]
			cumulative_x += col
			cumulative_x += self._separation[2]

			# draw
			self._buffer_table.fill(
				(cumulative_x, self._row_length_list[0] + self._separation[0] + self._separation[3]),
				(1, 1),
				'*'
			)

			# vertical line
			cumulative_x += 1

		return self._buffer_table.getBuffer(is_copy=False)

	def _updateBox_(self) -> None:
		self._updateLength_()
		self._updatePosition_()
		self._updateSize_()

	def _updateLength_(self) -> None:
		# ----- grid -----
		grid_h: int = 0
		grid_w: int = 0

		# height
		grid_h = len(self._row_list)

		# width
		for row in self._row_list:
			grid_w = max(grid_w, len(row))

		# ----- length list -----
		# first get the max row length and column length
		# row length: max height of each row
		# col length: max width of each row
		self._col_length_list.clear()
		self._row_length_list.clear()

		self._col_length_list = [0 for _ in range(grid_w)]
		self._row_length_list = [0 for _ in range(grid_h)]

		# foreach component in row_list
		for index_row, row in enumerate(self._row_list):
			for index_col, component in enumerate(row):

				self._col_length_list[index_col] = max(self._col_length_list[index_col], component.getSize()[0])
				self._row_length_list[index_row] = max(self._row_length_list[index_row], component.getSize()[1])

	def _updatePosition_(self) -> None:
		# the first one is self (render the table line)
		index: int = 1

		# foreach component in row_list
		cumulative_y: int = 0
		for index_row, row in enumerate(self._row_list):

			# separation - top
			cumulative_y += self._separation[0]

			cumulative_x: int = 0
			for index_col, component in enumerate(row):
				# separation - left
				cumulative_x += self._separation[1]

				# set position
				self._position_list[index] = (cumulative_x, cumulative_y)

				# += width of this col
				# += separation - right
				# += vertical line of the table
				cumulative_x += self._col_length_list[index_col]
				cumulative_x += self._separation[2]
				cumulative_x += 1

				# index of next item
				index += 1

			# += height of this row
			# += separation - bottom
			cumulative_y += self._row_length_list[index_row]
			cumulative_y += self._separation[3]

			# there will be a horizontal line between first and second row
			if index_row == 0:
				cumulative_y += 1

	def _updateSize_(self) -> None:
		# width
		self._size[0] = 0
		self._size[0] += sum(self._col_length_list)
		self._size[0] += max(0, len(self._col_length_list) - 1) * (self._separation[1] + self._separation[2] + 1)
		self._size[0] += self._separation[1] + self._separation[2]

		# height
		self._size[1] = 0
		self._size[1] += sum(self._row_length_list)
		self._size[1] += max(0, len(self._col_length_list) - 1) * (self._separation[0] + self._separation[3])
		self._size[1] += self._separation[0] + self._separation[3]
		self._size[1] += 1
