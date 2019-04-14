from __future__ import print_function
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop, Adam
from keras.utils import np_utils
import csv
import sys
from tqdm import tqdm
from math import sqrt

# oldStdout = sys.stdout
# file = open('Data/Logs.log', 'w')
# sys.stdout = file

np.random.seed(1671)  # for reproducibility

# network and training
NB_EPOCH = 15
BATCH_SIZE = 128
VERBOSE = 1
NB_CLASSES = 2   # number of outputs = number of digits
OPTIMIZER = 'RMSprop' # optimizer, explainedin this chapter
N_HIDDEN = 256
VALIDATION_SPLIT=0.2 # how much TRAIN is reserved for VALIDATION
DROPOUT = 0.4


def main():
    # class LoggingCallback(Callback):
    #     """Callback that logs message at end of epoch.
    #     """

    # def __init__(self, print_fcn=print):
    #     Callback.__init__(self)
    #     self.print_fcn = print_fcn


    # def on_epoch_end(self, epoch, logs={}):
    #     msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
    #     self.print_fcn(msg)
    #     error_logs = open("Data/Logs.log", 'a')
    #     error_logs.write(str(msg))
    #     error_logs.close()


    class LoadDialog(FloatLayout):
        load = ObjectProperty(None)
        cancel = ObjectProperty(None)



    class Root(FloatLayout):

        def dismiss_popup(self):
            self._popup.dismiss()

        def show_load(self):
            content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
            self._popup = Popup(title="Select .csv file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

        def load(self, path, filename):
            self.file_name = str(os.path.join(path, filename[0]))
            print(self.file_name)
            self.dismiss_popup()
            self.neural_net()

        def neural_net(self):
            try:
                data=open(self.file_name, "r")
                reader= csv.reader(data)
                xList = []
                labels = []
                names = []
                firstLine = True

                for line in tqdm(data):
                    if firstLine:
                        names = line.strip().split(",")
                        # print(names)
                        firstLine = False
                    else:
                        #split on comma
                        row = line.strip().split(",")
                        # print(row)
                        #put labels in separate array
                        labels.append(float(row[-1]))
                        #remove label from row
                        row.pop()
                        #convert row to floats
                        floatRow = [float(num) for num in row]
                        xList.append(floatRow)


                #Normalize columns in x and labels
                nrows = len(xList)
                ncols = len(xList[0])-1
                # print(nrows, ncols)

                #calculate means and variances
                xMeans = []
                xSD = []
                for i in tqdm(range(ncols)):
                    col = [xList[j][i] for j in range(nrows)]
                    mean = sum(col)/nrows
                    xMeans.append(mean)
                    colDiff = [(xList[j][i] - mean) for j in range(nrows)]
                    sumSq = sum([colDiff[i] * colDiff[i] for i in range(nrows)])
                    stdDev = sqrt(sumSq/nrows)
                    xSD.append(stdDev)

                #Save normalization values for use during testing
                normalized_backup = open('Data/normalized_values.txt', 'w')
                for i in xMeans:
                    normalized_backup.write(str(i)+',')
                normalized_backup.write("\n")
                for j in xSD:
                    normalized_backup.write(str(j)+',')
                normalized_backup.write("\n")
                normalized_backup.close()


                #use calculate mean and standard deviation to normalize xList
                xNormalized = []
                for i in range(nrows):
                    rowNormalized = [(xList[i][j] - xMeans[j])/xSD[j] for j in range(ncols)]
                    rowNormalized.append(xList[i][-1])
                    xNormalized.append(rowNormalized)
                #Normalize labels
                # meanLabel = sum(labels)/nrows
                # sdLabel = sqrt(sum([(labels[i] - meanLabel) * (labels[i] - meanLabel) for i in range(nrows)])/nrows)
                # labelNormalized = [(labels[i] - meanLabel)/sdLabel for i in range(nrows)]
                labelNormalized = labels

                #divide attributes and labels into training and test sets
                indices = range(len(xList))
                X_test = [xNormalized[i] for i in indices if i%7 == 0 ]
                X_train = [xNormalized[i] for i in indices if i%7 != 0 ]
                Y_test = [labelNormalized[i] for i in indices if i%7 == 0]
                Y_train = [labelNormalized[i] for i in indices if i%7 != 0]

                # print(len(X_train), len(X_train[1]))
                # print(len(X_test), len(X_test[1]))

                # convert class vectors to binary class matrices
                Y_train = np_utils.to_categorical(Y_train, NB_CLASSES)
                Y_test = np_utils.to_categorical(Y_test, NB_CLASSES)
                print("Done")


                # x = list(reader)
                # data = numpy.array(x).astype('float')
                RESHAPED = len(X_train[1])
                X_train = np.array(X_train).astype('float32')
                X_test = np.array(X_test).astype('float32')
                Y_train = np.array(Y_train).astype('float32')
                Y_test = np.array(Y_test).astype('float32')

                X_train = X_train.reshape(len(X_train), RESHAPED)
                X_test = X_test.reshape(len(X_test), RESHAPED)


                # M_HIDDEN hidden layers
                # final stage is softmax

                model = Sequential()
                model.add(Dense(N_HIDDEN, input_shape=(RESHAPED,)))
                model.add(Activation('relu'))
                model.add(Dropout(DROPOUT))
                model.add(Dense(N_HIDDEN))
                model.add(Activation('relu'))
                model.add(Dropout(DROPOUT))
                model.add(Dense(NB_CLASSES))
                model.add(Activation('softmax'))
                model.summary()

                model.compile(loss='categorical_crossentropy',
                              optimizer=OPTIMIZER,
                              metrics=['accuracy'])

                history = model.fit(X_train, Y_train,
                                    batch_size=BATCH_SIZE, epochs=NB_EPOCH,
                                    verbose=VERBOSE, validation_split=VALIDATION_SPLIT
                                    )

                # pd.DataFrame(history.history).to_csv("Data/Logs.log")

                score = model.evaluate(X_test, Y_test, verbose=VERBOSE)
                print("\nTest score:", score[0])
                print('Test accuracy:', score[1])

                #save model
                model_json = model.to_json()
                open('Data/rail_track.json', 'w').write(model_json)
                model.save_weights('Data/rail_track.h5', overwrite=True)

                # list all data in history
                # print(history.history.keys())
                # summarize history for accuracy
                plt.plot(history.history['acc'])
                plt.plot(history.history['val_acc'])
                plt.title('model accuracy')
                plt.ylabel('accuracy')
                plt.xlabel('epoch')
                plt.legend(['train', 'test'], loc='upper left')
                plt.show()
                # summarize history for loss
                plt.plot(history.history['loss'])
                plt.plot(history.history['val_loss'])
                plt.title('model loss')
                plt.ylabel('loss')
                plt.xlabel('epoch')
                plt.legend(['train', 'test'], loc='upper left')
                plt.show()
                sys.exit()


            except Exception as e:
                print(e)
                error_logs = open("Data/Logs.log", 'a')
                error_logs.write(str(e))
                error_logs.close()



    class Neural_TrainerApp(App):
        pass


    Factory.register('Root', cls=Root)
    Factory.register('LoadDialog', cls=LoadDialog)
    Neural_TrainerApp().run()


if __name__ == '__main__':
    main()
    