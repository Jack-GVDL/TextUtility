from typing import *
from .UtilText_Screen import UtilText_Screen


class UtilText_Component:

	def __init__(self):
		super().__init__()

		# data
		# update info
		self._is_updated: bool = False

		# config
		# best to be list (as the pointer)
		self._size: List[int] = [0, 0]

		# data
		self._data: Dict[str, List] = {}

		# tree
		self._parent				= None
		self._component_list: List 	= []

		# format
		# Tuple[int, int]: x, y
		self._position_list: List[Tuple[int, int]] = []

		# buffer
		# TODO: need buffer disable functionality
		self._is_buffer:	bool 			= True
		self._buffer:		UtilText_Screen = UtilText_Screen()

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
		return self._component_list.copy()

	@property
	def position_list(self) -> List[Tuple[int, int]]:
		return self._position_list.copy()

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
		self._position_list.append((0, 0))

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
		self._position_list.pop(index)

		# reset parent
		if child is not self:
			child._parent = None

		# set update flag
		self._requireUpdate_()
		return True

	# render
	def render(self) -> str:
		# check if needed to update or not
		self.update()

		# get content
		return self._buffer.render()

	def getSize(self) -> Tuple[int, int]:
		"""
		get the size of the component (self and children)
		:return: [w, h]
		"""
		self.update()
		return self._size[0], self._size[1]

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
		self._updateBox_()
		self._updateBuffer_()

		# update (self and children) is completed
		self._is_updated = True
		return True

	# Protected
	# set update flag
	def _requireUpdate_(self) -> None:
		self._is_updated = False

		parent = self._parent
		while parent is not None:
			parent._is_updated = False
			parent = parent.parent

	# content
	# _getContent_
	def _getContent_(self) -> List[List[str]]:
		raise NotImplementedError

	# box
	# _updateBox_
	def _updateBox_(self) -> None:
		raise NotImplementedError

	# buffer
	# _updateBuffer_
	def _updateBuffer_(self) -> None:
		# resize
		self._buffer.expand((0, 0), (self._size[0], self._size[1]))

		# draw
		for index, component in enumerate(self._component_list):

			# ----- position -----
			position: Tuple[int, int] = self._position_list[index]

			# ----- content -----
			content: List[List[str]] = []

			# if component is self
			# then it should not get the content from _buffer
			# it should instead get the content from _getContent_ function
			if component is self:
				content = self._getContent_()
			else:
				content = component._getBuffer_()

			# ----- draw -----
			self._buffer.draw(position, content, mask=None)

	def _getBuffer_(self) -> List[List[str]]:
		return self._buffer.getBuffer(is_copy=False)
