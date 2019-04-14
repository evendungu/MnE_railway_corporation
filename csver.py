import socket
import random
import os
import datetime
# from texttable import Texttable
from time import sleep

class MyCsver:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
		print("Closing csver...")
	def run(self):
		# os.chdir("F:\Class Work\Fifth Year\Project\Data")
		# import datetime
		# vers = datetime.datetime.now()
		# vers = str(vers)
		# vers = vers[0:10]+"_"+vers[11:19]
		print("csver started")
		# vers = str(random.random())[2:]

		now = datetime.datetime.now()
		vers = now.strftime("%Y-%m-%d-%H-%M-%S")
		name = "Data/raw_data_"+vers+".csv"
		data = open(name, "w")
		TitleRow = "Distance1, Distance2, Temperature, X_Axis, Y_Axis, Z_Axis, Vibration_state, Position\n"
		data.write(TitleRow)


		# table = Texttable()
		# table.set_deco(Texttable.HEADER)
		# table.set_cols_dtype(['t',
		# 					  't',
		# 					  't',
		# 					  't',
		# 					  't',
		# 					  't',
		# 					  't'])
		# table.set_cols_align(["l", "r", "r", "r", "r", "r", "r"])
		# table.add_rows([["Distance1", "Distance2", "Temperature", "X_Axis", "Y_Axis", "Z_Axis", "Vibration_state"]])

		# print(table.draw())

		# s=socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
		host="192.168.43.153"
		port=12346
		sleep(12)

		while self._running:
			try:
				s=socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
				s.connect((host, port))
				a = s.recv(1024)
				a = a.decode()
				# print(a)
				b = a[1:-1] + "\n"
				data.write(b)
				a = a[1:-1].split(",")
				# table.add_rows([[a[0][:5], a[1][:6], a[2], a[3], a[4], a[5], a[6]]])
				# print(table.draw())
			except Exception as e:
				print(e)
				# table.add_rows([["Null", "Null", "Null", "Null", "Null", "Null", "Null"]])
				# print(table.draw())
				# print("----NO SERVER DETECTED----")
				sleep(2)
			data.close()
			name = "Data/raw_data_"+vers+".csv"
			data = open(name, "a")
			s.close
			
		
		data.close()
