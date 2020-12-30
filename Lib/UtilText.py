from typing import *


class UtilText_Component:

	def __init__(self):
		super().__init__()

		# data
		# update info
		self._is_updated: bool = False

		# config
		# best to be list (as the pointer)
		self._size:		List[int] = [0, 0]
		self._position:	List[int] = [0, 0]

		# data
		self._data: Dict[str, List] = {}

		# tree
		self._parent				= None
		self._component_list: List 	= []

		# format
		# Tuple[int, int]: y, h
		self._position_list: List[Tuple[int, int]] = []

		# buffer
		# TODO: need buffer disable functionality
		self._is_buffer:	bool = True
		self._buffer: 		List[str] = []

		# operation
		# ...

	def __del__(self):
		return

	# Property
	@property
	def is_updated(self) -> bool:
		return self._is_updated

	@property
	def component_list(self) -> List:
		return self._component_list

	@property
	def parent(self):
		return self._parent

	@property
	def data(self) -> Dict:
		return self.getData()

	@data.setter
	def data(self, data: Dict) -> None:
		self.setData(data)

	# Operation
	# data
	def getData(self) -> Dict:
		return self._data.copy()

	def setData(self, data: Dict) -> None:
		# compare each item in the self._data
		# check if needed to update or not
		# data that not inside self._data will be ignored (no warning or error message)
		for key in data.keys():
			if key not in self._data.keys():
				continue

			# below copy method is wrong demo
			# self._data[key] = data[key]

			# it is assumed that all the data inside self._data is list
			# so instead of copying the pointer of list
			# copying of content inside list is required
			target: List = self._data[key]
			target.clear()
			target.extend(data[key])

		# set update flag
		self._requireUpdate_()

	# children tree
	def addChild(self, child) -> bool:
		# add to component_list
		self._component_list.append(child)

		# set parent
		if child is not self:
			child._parent = self

		# set update flag
		self._requireUpdate_()
		return True

	def rmChild(self, child) -> bool:
		# remove from component_list
		try:
			index = self._component_list.index(child)
		except ValueError:
			return False

		self._component_list.pop(index)

		# reset parent
		if child is not self:
			child._parent = None

		# set update flag
		self._requireUpdate_()
		return True

	# render
	# TODO: start, end
	def render(self, start: int = 0, end: int = -1) -> str:
		# check if needed to update or not
		self.update()

		# get content from buffer
		content: str = ""
		for line in self._buffer:
			content += line
			content += '\n'

		return content

	def getBufferLine(self, line: int) -> str:
		# check if needed to update or not
		self.update()

		# get line
		return self._getBufferLine_(line)

	def getSize(self) -> Tuple[int, int]:
		"""
		get the size of the component (self and children)
		:return: [w, h]
		"""
		self.update()
		return self._size[0], self._size[1]

	def getPosition(self) -> Tuple[int, int]:
		"""
		get the relative position of the component (self and children)
		:return: [x, y]
		"""
		self.update()
		return self._position[0], self._position[1]

	# update
	def update(self) -> bool:
		if self._is_updated:
			return True

		# ----- children -----
		for component in self._component_list:
			if component == self:
				continue
			component.update()

		# ----- self / current level -----
		self._updatePosition_()
		self._updateBox_()
		self._updateBuffer_()

		# update (self and children) is completed
		self._is_updated = True
		return True

	# Protected
	# update
	# self-as-component
	def _getContent_(self, line: int) -> str:
		return ""

	# set update flag
	def _requireUpdate_(self) -> None:
		self._is_updated = False

		parent = self._parent
		while parent is not None:
			parent._is_updated = False
			parent = parent.parent

	# update
	# position
	# - _updatePosition_
	# - _updateComponent_ / aka _updatePosition_Component_ (update a specific component)
	# TODO: may not applicable to complex component
	# update position_list based on component list
	def _updatePosition_(self) -> None:
		# first need to reset the self._position_list
		# must: len(self._position_list) == len(self._component_list)
		self._position_list.clear()
		self._position_list.extend([(0, 0) for _ in range(len(self._component_list))])

		# foreach component in the list
		# update its position
		for index, component in enumerate(self._component_list):

			pos: Tuple[int, int] = self._updateComponent_(index, component)
			self._position_list[index] = pos

	def _updateComponent_(self, index: int, cur) -> Tuple[int, int]:
		"""
		# update structure (relative position) of a component at THIS level

		:param index:
		:param cur:
		:return:
		"""
		raise NotImplementedError

	# box
	# _updateBox_
	def _updateBox_(self) -> None:
		raise NotImplementedError

	# buffer
	# _updateBuffer_
	# _updateLine_ / _updateBufferLine_ (update a specific line)
	# _getBufferLine_
	def _updateBuffer_(self) -> None:
		# clear buffer
		self._buffer.clear()

		# update buffer
		for line in range(self._size[1]):
			content = self._updateLine_(line)
			self._buffer.append(content)

	def _updateLine_(self, line: int) -> str:
		"""
		get the line of content (self and children)

		:param line: index of line
		:return: string of content
		"""
		content: str = ""
		for index, component in enumerate(self._component_list):

			# self
			if component == self:
				content += self._getContent_(line)
				continue

			# children
			# first calculate the relative position (y) / line
			# then check if inside the range (height) or not
			if line < self._position_list[index][0] or \
				line >= self._position_list[index][0] + self._position_list[index][1]:
				continue

			line_child: int = line - self._position_list[index][0]
			content += component._getBufferLine_(line_child)

		return content

	def _getBufferLine_(self, line: int) -> str:
		if line < 0 or line >= len(self._buffer):
			return ""
		return self._buffer[line]
