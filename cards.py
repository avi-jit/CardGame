import random
import curses
from curses import textpad

distance = 20
char_map = {-1:('  ','  '),
			2:('2 ',' 2'),
			3:('3 ',' \u025B'),
			4:('4 ',' \u02AB'),
			5:('5 ',' 5'),
			6:('6 ',' 9'),
			7:('7 ',' L'),
			8:('8 ',' 8'),
			9:('9 ',' 6'),
			10:('10','01'),
			11:('J ',' \u027E'),
			12:('Q ',' \u2941'),
			13:('K ',' \u029E'),
			14:('A ',' \u15C4')
			#14:('A ',' \u2200')
			}
symbol_map = {1:'\u2660', 2:'\u2661', 3:'\u2662', 4:'\u2663',-1:' '}

def new_card():
	c = random.randint(2,14)
	s = random.randint(1,4)
	return [c,s]

def new_layer(rows, x):
	cards = []
	for i in range(rows):
		cards.append(new_card())
	return [x,cards]

def erase_layer(stdscr, box, x):
	for y in range(box[0][0]+1, box[1][0]):
		stdscr.addstr(y, x, ' '*5)

def show_card(stdscr, c,s,x,y):
	# adds card c, symbol s starting at x,y
	c0 = char_map[c][0]
	c1 = char_map[c][1]
	first = '\u250C\u2501\u2501\u2501\u2510'
	second = '\u2502'+c0+' \u2502'
	third = '\u2502 '+symbol_map[s]+' \u2502'
	fourth = '\u2502 '+c1+'\u2502'
	fifth = '\u2514\u2501\u2501\u2501\u2518'
	stdscr.addstr(y, x, first)
	stdscr.addstr(y+1, x, second)
	stdscr.addstr(y+2, x, third)
	stdscr.addstr(y+3, x, fourth)
	stdscr.addstr(y+4, x, fifth)

def show_layer(stdscr, box, layer):
	# (x,[list of card (c,s)])
	for row,card in enumerate(layer[1]):
		show_card(stdscr, card[0],card[1],layer[0],box[0][0]+row*7+2)

def show_player(stdscr, box, player):
	stdscr.addstr(box[0][0] + player*7 + 3, 6, '@')

def erase_player(stdscr, box, player):
	stdscr.addstr(box[0][0] + player*7 + 3, 6, ' ')

def main(stdscr):
	# initial settings
	curses.curs_set(0)
	stdscr.nodelay(1)
	stdscr.timeout(50)

	# create a game box
	sh, sw = stdscr.getmaxyx()
	pad = 2
	rows = (sh-pad-3)//7 # 3 is for dashboard, 7 per card height
	dash = sh - rows*7 - pad
	box = [[dash,pad], [sh-pad, sw-pad]]  # [[ul_y, ul_x], [dr_y, dr_x]]
	textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

	player = rows//2
	show_player(stdscr, box, player)

	lives = 10
	lives_text = "Lives Remaining: {}  ".format(lives)
	stdscr.addstr(1, sw//2 - len(lives_text)//2, lives_text)

	hit = [-1,-1]
	#card_text="Last Card: {}, {}".format(char_map[hit[0]][0],symbol_map[hit[1]])
	#stdscr.addstr(2, sw//2 - len(lives_text)//2, card_text)

	# Instructions. Wait for Enter any Key.
	msg1 = "Navigate with Up/Down arrow keys."
	msg2 = "Hitting the same card twice adds 3 lives."
	msg3 = "Hitting the same color card twice adds 1 life."
	msg4 = "Hitting any other card loses 1 life."
	stdscr.addstr(sh//2-3, sw//2-len(msg1)//2, msg1)
	stdscr.addstr(sh//2-2, sw//2-len(msg2)//2, msg2)
	stdscr.addstr(sh//2-1, sw//2-len(msg3)//2, msg3)
	stdscr.addstr(sh//2, sw//2-len(msg4)//2, msg4)
	stdscr.nodelay(0)
	stdscr.getch()
	stdscr.nodelay(1)
	stdscr.timeout(100)

	layers = [  ] # (x,[list of card (c,s)])
	layers.append(new_layer(rows, sw-pad-pad*3))

	for layer in layers:
		show_layer(stdscr, box, layer)

	counter = 0
	while 1:
		counter += 1
		key = stdscr.getch() # non-blocking input

		erase_player(stdscr, box, player)
		if key == curses.KEY_DOWN and player < rows-1:
			player += 1
		elif key == curses.KEY_UP and player > 0:
			player -= 1
		elif key==curses.KEY_EXIT or key==curses.KEY_EIC:
			break
		show_player(stdscr, box, player)

		# erase all layers on screen
		for layer in layers:
			erase_layer(stdscr, box, layer[0])

		# shift all layers
		for layer in layers:
			layer[0]-=1

		# add a layer
		if counter == distance:
			counter = 0
			layers.insert(0, new_layer(rows, sw-pad-pad*3))

		# remove a layer
		if layers[-1][0] == 6:
			old_hit = hit[:]
			hit = layers[-1][1][player]
			if old_hit[0] != -1: # first wall
				if old_hit[0] == hit[0]:
					lives += 3
				elif old_hit[1] == hit[1]:
					lives += 1
				else:
					lives -= 1
					if lives == 0:
						msg = "Game Over!"
						stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
						stdscr.nodelay(0)
						stdscr.getch()
						break
			lives_text = "Lives Remaining: {}  ".format(lives)
			stdscr.addstr(1, sw//2 - len(lives_text)//2, lives_text)
			card_text="Last Card: {}, {}".format(char_map[hit[0]][0],symbol_map[hit[1]])
			stdscr.addstr(2, sw//2 - len(lives_text)//2, card_text)
			layers.pop()

		# render layers on screen
		for layer in layers:
			show_layer(stdscr, box, layer)

curses.wrapper(main)
