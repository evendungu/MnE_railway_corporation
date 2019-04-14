from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout  
from kivy.logger import Logger
from kivy.config import Config
#from kivy.properties import StringProperty, ListProperty
#from kivy.properties import ObjectProperty
from threading import Thread
import subprocess
import ssher2
import ssher2_running
import ssher2_tester
# import conn_tester
import csver
import csver_run
import sys
# import FChooser
from time import sleep



Config.set('kivy', 'log_level', 'warning')
# Config.write()



class Controller(BoxLayout):
	#item_strings = ListProperty()

	def collect_data(self, *args):
		
		if args[1] == 'down':
			try:
				if self.logging_thread.is_alive():
					print("Logging thread is alive!!!")
					log_to_delete = open("Data/Logs.log", "w")
					log_to_delete.close() 
					self.logs = open("Data/Logs.log", "r")
				else:
					self.logging_thread = Thread(target=self.read_log, daemon=True)
					self.logging_thread.start()
			except:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()

			sshUsername = "pi"
			sshPassword = "martineve"
			sshServer = "192.168.43.153"
			loogs = open("Data/Logs.log", "a")
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
				loogs = open("Data/Logs.log", "a")				
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
				# self.connection.sendShell(chr(3))
				# self.connection_vibr.sendShell(chr(3))

			except Exception as e:
				print(e)
			try:
				self.csver_instance.terminate()
			except Exception as e:
				print(e)
			exit_code = "Quitting data collection..."
			self.log_results.item_strings.append(exit_code)
			print(exit_code)
			
			loogs = open("Data/Logs.log", 'w')
			loogs.close()
			print("Finii")

	def check_sensors(self):
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Data/Logs.log", "w")
				log_to_delete.close()
				self.logs = open("Data/Logs.log", "r") 
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()

		sshUsername = "pi"
		sshPassword = "martineve"
		sshServer = "192.168.43.153"
		loogs = open("Data/Logs.log", "a")
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
			loogs = open("Data/Logs.log", "a")				
			loogs.write(str(e)+"\n")
			loogs.close()
		print("Finii")

	def Graph_deflection(self):
		global FChooser
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Data/Logs.log", "w")
				log_to_delete.write('Opening Grapher in Separate window..')
				log_to_delete.close()
				self.logs = open("Data/Logs.log", "r") 
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()
			log_to_delete = open("Data/Logs.log", "w")
			log_to_delete.write('Opening Grapher in Separate window..')
			log_to_delete.close()
		FChooser = subprocess.Popen('python FChooser.py', shell=True)


	def Train_new(self):
		global Neural_Trainer
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Data/Logs.log", "w")
				log_to_delete.write('Opening Neural net console in Separate window..')
				log_to_delete.close()
				self.logs = open("Data/Logs.log", "r") 
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()
			log_to_delete = open("Data/Logs.log", "w")
			log_to_delete.write('Opening Neural net console in Separate window..')
			log_to_delete.close()
		Neural_Trainer = subprocess.Popen('python Neural_Trainer.py', shell=True)

	def Show_errors(self):
		global error_shower
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Data/Logs.log", "w")
				log_to_delete.write('Opening File selector console in Separate window..')
				log_to_delete.close()
				self.logs = open("Data/Logs.log", "r") 
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()
			log_to_delete = open("Data/Logs.log", "w")
			log_to_delete.write('Opening Neural net console in Separate window..')
			log_to_delete.close()
		error_shower = subprocess.Popen('python show_err.py', shell=True)


	def Check_Connection(self):
		try:
			if self.logging_thread.is_alive():
				print("Logging thread is alive!!!")
				log_to_delete = open("Data/Logs.log", "w")
				log_to_delete.close() 
				self.logs = open("Data/Logs.log", "r")
			else:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()
		except:
			self.logging_thread = Thread(target=self.read_log, daemon=True)
			self.logging_thread.start()
		connection_tester = subprocess.Popen('python conn_tester.py', shell=True)



	def read_log(self):
		logs = open("Data/Logs.log", 'w')
		logs.close()
		self.logs = open("Data/Logs.log", "r")
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
					if line == "\n":
						pass
					else:
						line = "{}".format(line)
						line = line[:-1]
						# print(line)
						self.log_results.item_strings.append(line)
						# self.log_results.item_strings = ''.join(str(e) for e in self.log_results.item_strings)
						# print (self.log_results.item_strings)
			except Exception as e:
				pass

	def Test_run(self, *args):
		
		if args[1] == 'down':
			try:
				if self.logging_thread.is_alive():
					print("Logging thread is alive!!!")
					log_to_delete = open("Data/Logs.log", "w")
					log_to_delete.close() 
					self.logs = open("Data/Logs.log", "r")
				else:
					self.logging_thread = Thread(target=self.read_log, daemon=True)
					self.logging_thread.start()
			except:
				self.logging_thread = Thread(target=self.read_log, daemon=True)
				self.logging_thread.start()

			sshUsername = "pi"
			sshPassword = "martineve"
			sshServer = "192.168.43.153"
			loogs = open("Data/Logs.log", "a")
			first_l = "Connecting to server on ip", sshServer + "."
			loogs.write(str(first_l)+"\n")
			loogs.close()
			try:
				self.connect = ssher2_running.ssh(sshServer, sshUsername, sshPassword)
				self.connect_vibr = ssher2_running.ssh(sshServer, sshUsername, sshPassword)
				self.Collect_data_vibration_run_thread = Thread(target=self.connect_vibr.sendShell, args=("cd Desktop/Final\ Project/finalyearproject/ && python3 vibration_sensor.py",))
				self.Collect_data_run_thread = Thread(target=self.connect.sendShell, args=("cd Desktop/Final\ Project/finalyearproject/ && python3 75_text.py",))
				self.Collect_data_vibration_run_thread.daemon = True
				self.Collect_data_run_thread.daemon = True
				self.Collect_data_vibration_run_thread.start()
				self.Collect_data_run_thread.start()
				print("Both UUUUUUUUUPPPPPPPPPP")
				
				
			except Exception as e:
				print(e)
				# print("HEReeE")
				loogs = open("Data/Logs.log", "a")				
				loogs.write(str(e)+"\n")
				# print("HERE")
				# print(e)
				loogs.close()

			self.csver_instan = csver_run.MyCsver()
			self.csver_data_run_thread = Thread(target=self.csver_instan.run, daemon=True)
			self.csver_data_run_thread.start()

		
		else:
			try:
				# self.connect.sendShell(chr(3))
				self.connect.closeConnection()
				print("Closing ssher...")
				self.connect_vibr.closeConnection()
				print("Closing vibrater...")

			except Exception as e:
				print(e)
			try:
				self.csver_instan.terminate()
				print("Closing csver...")
			except Exception as e:
				print(e)
			exit_code = "Quitting test run collection..."
			self.log_results.item_strings.append(exit_code)
			print(exit_code)
			
			loogs = open("Data/Logs.log", 'w')
			loogs.close()
			print("Finii")




class RailApp(App):
    pass

if __name__ == '__main__':
	RailApp().run()
