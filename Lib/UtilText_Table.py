from typing import *
from .UtilText import UtilText_Component


class UtilText_Table(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# config
		self._separation:	List[int] = [1, 1]  # text: left, right
		self._column_list:	List[int] = []  # need computation per update

		# data
		self._data = {
			"separation": self._separation
		}

		# operation
		self._component_list.append(self)

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# ...


# its parent should only be UtilText_Table
class UtilText_Row(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# ...

		# operation
		# ...

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# ...


# its parent should only be UtilText_Row
class UtilText_Column(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# ...

		# operation
		# ...

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# ...


# its parent should only be UtilText_Table
class UtilText_HorizontalLine(UtilText_Component):

	def __init__(self):
		super().__init__()

		# data
		# ...

		# operation
		# ...

	def __del__(self):
		return

	# Operation
	# ...

	# Protected
	# ...
