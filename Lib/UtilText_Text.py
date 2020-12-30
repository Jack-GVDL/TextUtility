from typing import *
from .UtilText import UtilText_Component


class UtilText_Text(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# config
		self._text:	List[str] = [""]

		# data
		self._data = {
			"text":	self._text
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
		return self._text[0]

	# update
	def _updateComponent_(self, index: int, cur: UtilText_Component) -> Tuple[int, int]:
		# this component should only have self component (text component)
		if cur != self:
			return 0, 0
		return 0, len(self._text[0])

	def _updateBox_(self) -> None:
		self._position[0] = 0
		self._position[1] = 0
		self._size[0] = len(self._text[0])
		self._size[1] = 1
