from typing import *
from .UtilText_Component import UtilText_Component


class UtilText_List(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# config
		self._indent: 		List[int] = [4]
		self._padding:		List[int] = [1, 0, 0, 1]  # top, left, right, bottom
		self._separation:	List[int] = [1]

		# data
		self._data = {
			"indent":		self._indent,
			"padding":		self._padding,
			"separation":	self._separation
		}

		# operation
		# ...

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# render
	def _getContent_(self) -> List[List[str]]:
		return []

	# update
	def _updateBox_(self) -> None:
		# variable
		cumulative_y: int = 0
		cumulative_x: int = 0
		indent_front: int = self._indent[0] + self._padding[1]

		# padding - top
		cumulative_y += self._padding[0]

		# foreach children component
		for index in range(0, len(self._component_list)):
			component: UtilText_Component = self._component_list[index]

			# separation
			if index != 0:
				cumulative_y += self._separation[0]

			# set component position, then cumulate the height
			# (y, h)
			self._position_list[index] = (indent_front, cumulative_y)
			cumulative_y += component.getSize()[1]

			# get component width
			cumulative_x = max(cumulative_x, component.getSize()[0])

		# padding - bottom
		cumulative_y += self._padding[3]

		# padding - left, right
		# indent
		cumulative_x += self._padding[1] + self._padding[2] + self._indent[0]

		# box dimension
		self._size[0] = cumulative_x
		self._size[1] = cumulative_y
