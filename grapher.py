import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv


def main():	
	try:
		file_name_chooser = open('file_name_log.log', 'r')
		chosen_file_name = file_name_chooser.readline() 
		# print(chosen_file_name)
		file_name_chooser.close()
		data=open(chosen_file_name, "r")
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
		error_logs = open("Logs.log", 'a')
		error_logs.write(str(e))
		error_logs.close()

if __name__ == '__main__':
	main()
