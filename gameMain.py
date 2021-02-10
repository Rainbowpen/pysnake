from pkg.snakeGame import *
import time
from tkinter import *
from pynput import keyboard
import threading
import random

redCandy = candy


class greenSnake(snake):
	def setup():
		greenSnake.head.last_x = greenSnake.head.x
		greenSnake.head.last_y = greenSnake.head.y
		mainWD.gp.greenSnake = mainWD.gp.create_rectangle(
					mainWD.unit*greenSnake.head.x,
					mainWD.unit*greenSnake.head.y,
					mainWD.unit*(greenSnake.head.x + 1),
					mainWD.unit*(greenSnake.head.y + 1),
					fill='green')
		mainWD.gp.greenSnake_tail = []

	def grow():
		greenSnake.eat += 1

	def addPosition():
		if (greenSnake.head.last_x != greenSnake.head.x
		or greenSnake.head.last_y != greenSnake.head.y):
			greenSnake.body.position.insert(0,
										[greenSnake.head.x,
										greenSnake.head.y])
			for i in range(greenSnake.eat+1, len(greenSnake.body.position)):
				greenSnake.body.position.pop()
			greenSnake.head.last_x = greenSnake.head.x
			greenSnake.head.last_y = greenSnake.head.y

	def creadBody():
		if len(greenSnake.body.position) > 1:
			for i in range(len(greenSnake.body.position)):
				mainWD.gp.greenSnake_tail.append(mainWD.gp.create_rectangle(
					mainWD.unit*greenSnake.body.position[i-1][0],
					mainWD.unit*greenSnake.body.position[i-1][1],
					mainWD.unit*(greenSnake.body.position[i-1][0]+1),
					mainWD.unit*(greenSnake.body.position[i-1][1]+1),
					fill='green'))

	def deleteBody():
		if len(greenSnake.body.position) > 1:
			for i in range(len(greenSnake.body.position)):
				mainWD.gp.itemconfig(mainWD.gp.greenSnake_tail[i-1], fill="white")
				mainWD.gp.delete(mainWD.gp.greenSnake_tail[i-1])
		mainWD.gp.greenSnake_tail.clear()

	def die():
		isdie = False
		if (greenSnake.head.x < 0 or
		greenSnake.head.x > mainWD.width or
		greenSnake.head.y < 0 or greenSnake.head.y > mainWD.height):
				isdie = True
		if len(greenSnake.body.position) > 1:
			for i in range(len(greenSnake.body.position)):
				if i>1 and [greenSnake.head.x, greenSnake.head.y] == greenSnake.body.position[i]:
						isdie = True
						print(greenSnake.head.x,greenSnake.head.y, greenSnake.body.position[i])
		if 	isdie:
			branch.control.stop_timeFlow = True
	




class mainWD:
	width = 80
	height = 60
	unit = 10
	window = None
	gp = None
	quit = False
	freshDone = True

	def __init__(self):
		mainWD.window = Tk()
		mainWD.window.title('Game')
		mainWD.window.geometry('{0}x{1}+560+240'.format(
			mainWD.width*mainWD.unit,
			mainWD.height*mainWD.unit+30))
		mainWD.window.resizable(width=FALSE, height=FALSE)
		mainWD.gp = Canvas(
			bg='white',
			height=mainWD.height*mainWD.unit+30,
			width=mainWD.width*mainWD.unit)
		reset()
		greenSnake.setup()
		candySetup()
		statusBarSetup()
		middle_infoSetup()
		mainWD.gp.pack()

	def freshScreen():
		if eat():
			greenSnake.grow()
			resetCandy()
			greenSnake.speed *= 0.9
		greenSnake.addPosition()
		mainWD.gp.coords(
			mainWD.gp.greenSnake,
			mainWD.unit*greenSnake.head.x,
			mainWD.unit*greenSnake.head.y,
			mainWD.unit*(greenSnake.head.x+1),
			mainWD.unit*(greenSnake.head.y+1))
		mainWD.gp.coords(
			mainWD.gp.candy,
			mainWD.unit*redCandy.x,
			mainWD.unit*redCandy.y,
			mainWD.unit*(redCandy.x+1),
			mainWD.unit*(redCandy.y+1))
		greenSnake.creadBody()
		statusBarSetup()
		mainWD.window.update()
		greenSnake.deleteBody()
		greenSnake.die()
		print('eat = {0}  position = {1}  speed = {2}'.format(greenSnake.eat,
										greenSnake.body.position, greenSnake.speed))
		mainWD.freshDone = True


class branch():
	threading_timeFlow = None
	threading_keypress = None

	stop_timeFlow = False
	kill_timeFlow = False
	stop_keypress = False
	kill_keypress = False

	def done():
			branch.control.kill_keypress, branch.control.kill_timeFlow = True, True

	def __init__(self,):
		branch.threading_timeFlow = threading.Thread(target=timeFlow)
		branch.threading_keypress = threading.Thread(target=keypress)
		branch.threading_timeFlow.start()
		branch.threading_keypress.start()


def candySetup():
	mainWD.gp.candy = mainWD.gp.create_rectangle(
				mainWD.unit*redCandy.x,
				mainWD.unit*redCandy.y,
				mainWD.unit*(redCandy.x+1),
				mainWD.unit*(redCandy.y+1),
				fill='red')


def statusBarSetup():
	mainWD.gp.btm = mainWD.gp.create_rectangle(
				mainWD.unit*0,
				mainWD.unit*mainWD.height,
				mainWD.unit*mainWD.width,
				mainWD.unit*mainWD.height+30,
				fill='pink')

	mainWD.gp.btm_txt = mainWD.gp.create_text(
					mainWD.unit*(mainWD.width/2),
					mainWD.unit*mainWD.height+15,
					text='Apple : ' + str(greenSnake.eat),
					font=("Arial bold", 15),
					fill='black')

	mainWD.gp.info_Ltxt = mainWD.gp.create_text(
					mainWD.unit*(15),
					mainWD.unit*mainWD.height+15,
					text='ESC->Quit    R->Reset', font=("Arial bold", 10),
					fill='black', anchor=E)

	mainWD.gp.info_Ltxt = mainWD.gp.create_text(
				mainWD.unit*(mainWD.width-2),
				mainWD.unit*mainWD.height+15,
				text='←/A  ↑/W  →/D  ↓/S', font=("Arial bold", 10),
				fill='black', anchor=E)


def middle_infoSetup():
	mainWD.gp.gover = mainWD.gp.create_text(
				mainWD.unit*(mainWD.width/2),
				mainWD.unit*(mainWD.height/2),
				text='',
				font=("Arial bold", 50),
				fill='black')


def timeFlow():
	while True:
		if branch.control.kill_timeFlow:
			break
		time.sleep(greenSnake.speed)
		if branch.control.stop_timeFlow:
			greenSnake.isMove = False
		elif mainWD.freshDone:
			if greenSnake.direction == 1:
				# NOTE: go up
				greenSnake.head.y -= 1
			elif greenSnake.direction == 2:
				# NOTE: go down
				greenSnake.head.y += 1
			elif greenSnake.direction == 3:
				# NOTE: go left
				greenSnake.head.x -= 1
			elif greenSnake.direction == 4:
				# NOTE: go right
				greenSnake.head.x += 1
			greenSnake.isMove = True
			mainWD.freshDone = False


def on_press(key):
	if branch.control.kill_keypress:
		return False
	try:
		if greenSnake.isMove:
			if((('{0}'.format(key)) == "Key.up"
				or ('{0}'.format(key)) == "'w'")
				and greenSnake.direction != 2):
				greenSnake.direction = 1
			elif((('{0}'.format(key)) == "Key.down"
				or ('{0}'.format(key)) == "'s'") and greenSnake.direction != 1):
				greenSnake.direction = 2
			elif((('{0}'.format(key)) == "Key.left"
				or ('{0}'.format(key)) == "'a'") and greenSnake.direction != 4):
				greenSnake.direction = 3
			elif((('{0}'.format(key)) == "Key.right"
				or ('{0}'.format(key)) == "'d'")
				and greenSnake.direction != 3):
				greenSnake.direction = 4
			greenSnake.isMove = False
	except AttributeError:
		pass


def on_release(key):
	# NOTE: print('{0} released'.format(key))
	if key == keyboard.Key.esc:
		print("quit game")
		mainWD.quit = True
		# Stop listener
		return False
	elif((('{0}'.format(key)) == "'R'")
			or (('{0}'.format(key)) == "'r'")):
			reset()


def keypress():
	with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
		listener.join()


def eat():
	if greenSnake.head.x == redCandy.x and greenSnake.head.y == redCandy.y:
		return True


def reset():
	greenSnake.head.x = random.randint(20, mainWD.width-20)
	greenSnake.head.y = random.randint(20, mainWD.height-20)
	greenSnake.head.y = random.randint(20, mainWD.height-20)
	# NOTE: greenSnake start x, y
	greenSnake.head.last_x = greenSnake.head.x
	greenSnake.head.last_y = greenSnake.head.y
	greenSnake.direction = random.randint(1, 4)
	resetCandy()
	# NOTE: candy start x, y
	greenSnake.eat = 0
	greenSnake.speed = 0.15
	greenSnake.isMove = False
	branch.control.stop_timeFlow = False
	branch.control.stop_keypress = False
	print('snake = {0},{1}  candy = {2},{3}'.format(
											greenSnake.head.x,
											greenSnake.head.y,
											redCandy.x,
											redCandy.y
											))


def resetCandy():
	while True:
		redCandy.x = random.randint(1, mainWD.width-2)
		redCandy.y = random.randint(1, mainWD.height-2)
		if redCandy.x != greenSnake.head.x or redCandy.y != greenSnake.head.y:
			break


def main():
	mainWD()
	branch()
	while True:
		if mainWD.quit:
			break
		mainWD.freshScreen()
	branch.control.done()


if __name__ == '__main__':
	main()
