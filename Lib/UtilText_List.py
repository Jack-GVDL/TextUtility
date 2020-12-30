from typing import *
from .UtilText import UtilText_Component


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
		self._component_list.append(self)

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# render
	def _getContent_(self, line: int) -> str:
		return ' ' * (self._indent[0] + self._padding[1])

	# update
	def _updateComponent_(self, index: int, cur: UtilText_Component) -> Tuple[int, int]:
		# the first one should be self (indent component)
		if cur == self:
			return 0, 0

		# ----- update component -----
		# rest (children component)
		# it should be noticed that the position of prev component is already configured in self._position_list
		# and can be used now

		# y -> padding and separation
		# index == 1: 								first non-self component (child component)
		# index == len(self._component_list) - 1: 	last child component
		y: int = self._position_list[index - 1][0] + self._position_list[index - 1][1]

		if index == 1:
			y += self._padding[0]
		else:
			y += self._separation[0]

		# h -> component height
		h: int = cur.getSize()[1]

		# ----- update self size -----
		# not sure should the update be here or not
		# ...

		return y, h

	def _updateBox_(self) -> None:
		self._position[0] = 0
		self._position[1] = 0

		self._size[0] = 0
		self._size[1] = 0

		# get width
		for index, component in enumerate(self._component_list):
			if component is self:
				continue
			self._size[0] = max(self._size[0], component.getSize()[0])

		# get height
		# it is noticed that padding-top and separation already inside position_list[-1][0], i.e. y
		self._size[1] += self._position_list[-1][0] + self._position_list[-1][1]
		self._size[1] += self._padding[3]

		# indent and padding
		self._size[0] += self._indent[0]
		self._size[0] += self._padding[1]
