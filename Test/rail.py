from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout  
from kivy.logger import Logger
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import matplotlib.pyplot as plt
import os
#from kivy.properties import StringProperty, ListProperty
#from kivy.properties import ObjectProperty
from threading import Thread
# import ssher2
# import ssher2_tester
# import conn_tester
# import csver
# import FChooser
from time import sleep


Config.set('kivy', 'log_level', 'warning')
# Config.write()


class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class Roto(FloatLayout):
	def dismiss_popup(self):
		self._popup.dismiss()
	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		self.file_name = str(os.path.join(path, filename[0]))
		print(self.file_name)
		self.dismiss_popup()
		self.grapher()

	def grapher(self):
		try:
			data=open(self.file_name, "r")
			reader= csv.reader(data)
			firstLine = True
			deflection = []
			Distance_cov = []

			for line in data:
				if firstLine:
					firstLine = False
				else:
					row = line.strip().split(",")
					Distance = int(row[-1])
					deflection_value = abs(float(row[0]) - float(row[1]))
					if deflection_value > 10:
						pass
					else:
						Distance_cov.append(Distance)
						deflection.append(deflection_value)

			# print(deflection)
			print(len(Distance_cov))
			print(len(deflection))
			plt.plot(Distance_cov,deflection)
			plt.xlabel('Distance covered')
			plt.ylabel('Vertical Deflection')
			plt.title('Deflection along rail track')
			plt.show()
		except Exception as e:
			print(e)
			error_logs = open("Logs.log", 'a')
			error_logs.write(str(e))
			error_logs.close()

Factory.register('Roto', cls=Roto)
Factory.register('LoadDialog', cls=LoadDialog)

class Controller(BoxLayout):
	#item_strings = ListProperty()

	def collect_data(self, *args):
		
		if args[1] == 'down':
			try:
				if self.logging_thread.is_alive():
					print("Logging thread is alive!!!")
					log_to_delete = open("Logs.log", "w")
					log_to_delete.close() 
					self.logs = open("Logs.log", "r")
				else:
					self.logging_thread = Thread(target=self.read_log, daemon=True)
					self.logging_thread.start()
			except:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()

			sshUsername = "pi"
			sshPassword = "martineve"
			sshServer = "192.168.43.153"
			loogs = open("Logs.log", "a")
			first_l = "Connecting to server on ip", sshServer + "."
			loogs.write(str(first_l)+"\n")
			loogs.close()
			try:
				self.connection = ssher2.ssh(sshServer, sshUsername, sshPassword)
				self.connection_vibr = ssher2.ssh(sshServer, sshUsername, sshPassword)
				self.Collect_data_vibration_thread = Thread(target=self.connection_vibr.sendShell, args=("cd Desktop/Final\ Project/finalyearproject/ && python3 vibration_sensor.py",))
				self.Collect_data_thread = Thread(target=self.connection.sendShell, args=("cd Desktop/Final\ Project/finalyearproject/ && python3 75_text.py",))
				self.Collect_data_vibration_thread.daemon = True
				self.Collect_data_thread.daemon = True
				self.Collect_data_vibration_thread.start()
				self.Collect_data_thread.start()
				print("Both UUUUUUUUUPPPPPPPPPP")
				
				
			except Exception as e:
				print(e)
				# print("HEReeE")
				loogs = open("Logs.log", "a")				
				loogs.write(str(e)+"\n")
				# print("HERE")
				# print(e)
				loogs.close()

			self.csver_instance = csver.MyCsver()
			self.csver_data_thread = Thread(target=self.csver_instance.run, daemon=True)
			self.csver_data_thread.start()

		
		else:
			try:
				self.connection.closeConnection()
				self.connection_vibr.closeConnection()

			except Exception as e:
				print(e)
			try:
				self.csver_instance.terminate()
			except Exception as e:
				print(e)
			exit_code = "Quitting data collection..."
			self.log_results.item_strings.append(exit_code)
			print(exit_code)
			
			loogs = open("Logs.log", 'w')
			loogs.close()
			print("Finii")

	def check_sensors(self):
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Logs.log", "w")
				log_to_delete.close()
				self.logs = open("Logs.log", "r") 
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()

		sshUsername = "pi"
		sshPassword = "martineve"
		sshServer = "192.168.43.153"
		loogs = open("Logs.log", "a")
		first_l = "Connecting to server on ip", sshServer + "."
		loogs.write(str(first_l)+"\n")
		loogs.close()
		try:
			self.connection = ssher2_tester.ssh(sshServer, sshUsername, sshPassword)
			self.Collect_data_thread = Thread(target=self.connection.sendShell, args=("cd Desktop/Final\ Project/finalyearproject/ && python3 75_text_tester.py",))
			self.Collect_data_thread.daemon = True
			self.Collect_data_thread.start()	
		except Exception as e:
			print(e)
			loogs = open("Logs.log", "a")				
			loogs.write(str(e)+"\n")
			loogs.close()
		print("Finii")

	# def Graph_deflection(self):
	# 	try:
	# 		if self.logging_thread.is_alive():
	# 			print("Logging thread is alive!!!")
	# 			log_to_delete = open("Logs.log", "w")
	# 			log_to_delete.close()
	# 			self.logs = open("Logs.log", "r") 
	# 		else:
	# 			self.logging_thread = Thread(target=self.read_log, daemon=True)
	# 			self.logging_thread.start()
	# 	except:
	# 		self.logging_thread = Thread(target=self.read_log, daemon=True)
	# 		self.logging_thread.start()
	# 	Thread(target=FChooser.main, daemon=True).start()



	def Check_Connection(self):
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Logs.log", "w")
				log_to_delete.close() 
				self.logs = open("Logs.log", "r")
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()

		try:
			self.check_connection = conn_tester.MyConnTester()
			self.check_connection_thread = Thread(target=self.check_connection.run, daemon=True)
			self.check_connection_thread.start()
			# print("Started conn tester thread")

		except Exception as e:
			print(e)
			pass



	def read_log(self):
		logs = open("Logs.log", 'w')
		logs.close()
		self.logs = open("Logs.log", "r")
		while True:
			try:
				where = self.logs.tell()
				line = self.logs.readline()
				if not line:
					# sleep(0.1)
					logs.seek(where)
				else:
					# #newest logs on top
					#self.item_strings = '%s%s' %(line, self.item_strings)
					line = "{}".format(line)
					line = line[:-1]
					# print(line)
					self.log_results.item_strings.append(line)
					# self.log_results.item_strings = ''.join(str(e) for e in self.log_results.item_strings)
					# print (self.log_results.item_strings)
			except Exception as e:
				pass





class RailApp(App):
    pass

if __name__ == '__main__':
    RailApp().run()
