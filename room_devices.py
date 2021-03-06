import RPi.GPIO as GPIO
import time
# from multiprocessing import Process, Pipe
from threading import Thread
import subprocess
import paho.mqtt.client as mqtt
import json

class RoomDevices():
	alarm_handle : subprocess.Popen
	inn : list
	out : list
	room_esp : dict
	gpio_in_device : dict
	esp_in_device : dict
	esp_out_device : dict
	gpio_out_device : dict
	total_device : dict

	
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.out = [17, 18] 
		self.inn = [25, 26, 5, 6, 12, 16]
		self.total_device = {}
		#self.esp_device = {}
		self.esp_defined_device = {}
		self.esp_in_device = {}
		self.esp_out_device = {}
		self.room_esp = {}
		self.gpio_in_device = {
			"sala": (25, "sensor_presenca_1"),
			"cozinha": (26, "sensor_presenca_2"),
			"porta_cozinha": (5, "sensor_abertura_1"),
			"janela_cozinha": (6, "sensor_abertura_2"),
			"porta_sala": (12, "sensor_abertura_3"),
			"janela_sala": (16, "sensor_abertura_4")

		}
		self.gpio_out_device = {
			"cozinha": (17, "lampada_1"),
			"sala": (18, "lampada_2")
		}
		GPIO.setup(self.inn, GPIO.IN)
		GPIO.setup(self.out, GPIO.OUT)

	def polling(self):
		def alarm(room, state : int, device):
			if state:
				with open("log.csv", "a") as fp:
					fp.write(f"\nalarm, {room}, {device}, 1")
					self.alarm_handle = subprocess.Popen(["omxplayer","--no-keys", "All_Megaman_X_WARNING.mp3","&"])
					self.alarm_handle.wait()

		while(True):
			for room,(pin, device) in self.gpio_in_device.items():
				alarm(room, GPIO.input(pin), device)
			for room,(state, device) in self.esp_in_device.items():
				alarm(room, state, device)
				
			time.sleep(0.5)

	def print_device(self, screen):
		# dict compreension
		self.total_device.update({k:(GPIO.input(v), z) for z, (v, k) in self.gpio_out_device.items() })
		self.total_device.update({k:(GPIO.input(v), z) for z, (v, k) in self.gpio_in_device.items()})
		for enum, (device, (value, room)) in enumerate(self.total_device.items()):
			screen.addstr(enum, 60, f"comodo: {room}; dispositivo: {device}; estado: {value}")
		return len(self.total_device)

	def device_set(self, name, state: bool):
		if name in self.gpio_out_device:
			GPIO.output(self.gpio_out_device[name][0], state)
		elif name in self.esp_out_device:
			client = mqtt.Client("set_output")
			broker = "mqtt.eclipseprojects.io"
			client.connect(broker)
			if(not self.client.publish(room_esp.get(name), json.dumps(state))):
				raise Exception(f"Failed to send message to topic {device}")
			with open("log.csv", "a") as fp:
				fp.write(f"\noutput, {name}, {self.esp_out_device.get(name)[1]}, {state}")
			# mqtt.publish(state)

	def run_polling(self):
		polling = Thread(target=self.polling ,daemon=True)
		polling.start()
		return polling

# i'm import the instace instead of importing the class
room_devices = RoomDevices()