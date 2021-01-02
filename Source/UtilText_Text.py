from typing import *
from .UtilText_Component import UtilText_Component


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
		self.addChild(self)

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# render
	def _getContent_(self) -> List[List[str]]:
		content: List[str] = []
		for c in self._text[0]:
			content.append(c)

		# text should only have one line
		return [content]

	def _updateBox_(self) -> None:
		# position_list
		self._position_list[0] = (0, 0)

		# size
		self._size[0] = len(self._text[0])
		self._size[1] = 1
