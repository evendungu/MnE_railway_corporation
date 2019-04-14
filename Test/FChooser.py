from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import matplotlib.pyplot as plt
import csv
# import grapher

import os

def main():

    class LoadDialog(FloatLayout):
        load = ObjectProperty(None)
        cancel = ObjectProperty(None)



    class Root(FloatLayout):

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



    class FChooserApp(App):
        pass


    Factory.register('Root', cls=Root)
    Factory.register('LoadDialog', cls=LoadDialog)
    FChooserApp().run()


if __name__ == '__main__':
    main()
    