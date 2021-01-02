from typing import *


class UtilText_Screen:

	def __init__(self):
		super().__init__()

		# data
		# use str instead of chr is for different char format
		self._buffer_list: 	List[List[str]] = []
		self._size:			List[int]		= [0, 0]

	# operation
	# ...

	def __del__(self):
		return

	# Property
	@property
	def buffer(self) -> List[List[str]]:
		return self.getBuffer()

	@property
	def size(self) -> Tuple[int, int]:
		return self.getSize()

	# Operation
	# render
	def render(self) -> str:
		content: str = ""

		for buffer in self._buffer_list:
			for char in buffer:
				content += char
			content += '\n'

		return content

	# content
	def getBuffer(self, is_copy: bool = True) -> List[List[str]]:
		if not is_copy:
			return self._buffer_list

		# require copy
		return self._buffer_list.copy()

	def getSize(self) -> Tuple[int, int]:
		return self._size[0], self._size[1]

	# draw
	def draw(self, position: Tuple[int, int], content: List[List[str]], mask: List[List[int]] = None) -> None:
		# ----- expand -----
		expand_w: int = 0
		expand_h: int = len(content)

		for row in content:
			expand_w = max(expand_w, len(row))

		# actual expand
		self._expand_(position, (expand_w, expand_h))

		# ----- masking -----
		self._draw_(position, content, mask)

	def fill(self, position: Tuple[int, int], size: Tuple[int, int], content: str) -> None:
		# ----- expand -----
		# actual expand
		self._expand_(position, size)

		# ----- masking -----
		self._fill_(position, size, content)

	def expand(self, position: Tuple[int, int], size: Tuple[int, int]) -> None:
		# actual expand
		self._expand_(position, size)

	def reset(self) -> None:
		# actual reset
		self._reset_()

	# Protected
	def _expand_(self, position: Tuple[int, int], size: Tuple[int, int]) -> None:
		# get screen current data
		screen_w: int = self._size[0]
		screen_h: int = self._size[1]

		# ----- row -----
		expand_h: int = 0
		expand_h = position[1] + size[1]
		expand_h = max(0, expand_h - screen_h)

		for _ in range(expand_h):
			self._buffer_list.append([' ' for _ in range(self._size[0])])

		screen_h += expand_h

		# ----- column -----
		# all the row expand to the same width
		expand_w: int = 0
		expand_w = position[0] + size[0]
		expand_w = max(0, expand_w - screen_w)

		for index in range(screen_h):
			self._buffer_list[index].extend([' ' for _ in range(expand_w)])

		screen_w += expand_w

		# ----- size -----
		self._size[0] = screen_w
		self._size[1] = screen_h

	# TODO: not yet completed
	# def _retract_(self) -> None:
	# 	pass

	def _draw_(self, position: Tuple[int, int], content: List[List[str]], mask: List[List[int]]) -> None:
		for index_row in range(len(content)):
			for index_column in range(len(content[index_row])):

				# mask
				# only available when mask is not None
				if mask is not None and not mask[index_row][index_column]:
					continue

				# covering
				self._buffer_list[position[1] + index_row][position[0] + index_column] = \
					content[index_row][index_column]

	def _fill_(self, position: Tuple[int, int], size: Tuple[int, int], content: str) -> None:
		for index_row in range(size[1]):
			for index_column in range(size[0]):
				# covering
				self._buffer_list[position[1] + index_row][position[0] + index_column] = content

	def _reset_(self) -> None:
		self._buffer_list.clear()
		self._size = [0, 0]


if __name__ == '__main__':
	screen = UtilText_Screen()

	# create content
	content_1: List[List[str]] = [["" for x in range(5)] for y in range(5)]

	for y in range(5):
		for x in range(5):
			content_1[y][x] = str(max(x, y))

	# draw on screen
	screen.draw((3, 3), content_1, None)
	screen.fill((1, 1), (3, 3), '5')

	# render
	result: str = screen.render()
	print(result)
