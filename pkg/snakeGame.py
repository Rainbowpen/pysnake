'''
import sys
import os
import time
from pynput import keyboard
import threading
import random
sys.path.append(os.path.abspath('../gameMain'))
#from gameMain import mainWD
'''


class snake():
	speed = 0.15
	direction = 1
	isMove = False
	eat = 0

	def timedirection(direction, x, y):
			return True

	def grow():
		pass

	class head():
		x = None
		y = None
		last_x = None
		last_y = None

	class body():
		position = []


class candy():
	x = None
	y = None
