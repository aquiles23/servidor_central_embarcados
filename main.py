#!/usr/bin/env python3
from sensor import sensor
from room_devices import Room_devices
import curses
import time
import sys


def salutation(screen):
	screen.addstr(0, 0, "digite 0 para sair do programa")
	screen.addstr(1, 0, "digite 1 para adicionar um novo dispositivo")
	screen.addstr(2, 0, "digite 2 para setar o estado de um dispositivo")
	screen.addstr(3, 0, "digite 3 para parar o alarme")

def input_str(screen, y_pos : int, lenght : int, instructions = "") -> str:
	screen.nodelay(False)
	curses.echo()
	screen.addstr(y_pos - 1, 0, instructions)
	string = screen.getstr(y_pos,0,lenght)
	curses.noecho()
	screen.nodelay(True)
	return string


if __name__ == "__main__":
	try:
		room_devices = Room_devices()
		screen = curses.initscr()
		curses.noecho()
		screen.nodelay(True)
		flag = -1
		while flag != ord("0"):
			
			screen.clear()
			salutation(screen)

			temp, hum = sensor()
			screen.addstr(4, 0, f"cômodo central. Humidade: {hum} Temperatura {temp}")

			if(flag == ord("1")):
				#raise
				pass
			elif (flag == ord("2")):
				device_name = input_str(screen, 7, 50,"digite o nome do cômodo")
				state = bool(
					int(
						input_str(
							screen,
							9,
							1,
							"digite seu estado(1 ou 0)")))
				room_devices.device_set(device_name,state)
			elif (flag == ord("3")):
				pass
			flag = screen.getch()

			time.sleep(0.3)

	except Exception as err:
		curses.endwin()
		raise err
		


	curses.endwin()