import threading, paramiko
from time import sleep

class ssh:
    shell = None
    client = None
    transport = None
 
    def __init__(self, address, username, password):
        # print("Connecting to server on ip", str(address) + ".")
        self._running = True
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
 
    def closeConnection(self):
        if(self.client != None):
            print("\nClosing ssher...")
            self.client.close()
            self.transport.close()
            self._running = False


 
    def openShell(self):
        self.shell = self.client.invoke_shell()
 
    def sendShell(self, command):
        self.shell = self.client.invoke_shell()
        if(self.shell):
            self.shell.send(command + "\n")
            self.process()
        else:
            print("Shell not opened.")
 
    def process(self):
        global connection
        logss = open("Data/Logs.log", "a")
        print("ssher started")
        while self._running:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                    print("TRaaaappped")
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                strdata.replace('\n', '')
                print(strdata, end = "")
                
                if(strdata.endswith("$ ")):
                    logss.write(strdata)
                    logss.close()
                    print("written!!!!!!!!!!!!!!!1")
                    sleep(2)
                    self.closeConnection()

                if strdata != '\n':
                    logss.write(strdata)
                logss.close()                
                sleep(0.5)
            logss = open("Data/Logs.log", "a")

    def process2(self):
        global connection
        logss = open("Data/Logs.log", "a")
        print("ssher started")
        while self._running:
            # Print data when available
            try:
                if self.shell != None and self.shell.recv_ready():
                    alldata = self.shell.recv(1024)
                    while self.shell.recv_ready():
                        alldata += self.shell.recv(1024)
                    strdata = str(alldata, "utf8")
                    strdata.replace('\r', '')
                    strdata.replace('\n', '')
                    print(strdata, end = "")
                    if(strdata.endswith("$ ")):
                        logss.write(strdata)
                        loggs.close()
                        print("\n$ ", end = "")
                        sleep(0.5)
                        logss = open("Data/Logs.log", "a")
                        break
                    if strdata != '\n':
                        logss.write(strdata)
                    logss.close()
                    sleep(0.5)
                logss = open("Data/Logs.log", "a")
            except Exception as e:
                print(e)
                logss.write(e)
                logss.close()
                logss = open("Data/Logs.log", "a")

 
 

# def start_ssh():
#     sshUsername = "pi"
#     sshPassword = "martineve"
#     sshServer = "192.168.43.153"
#     logss = open("Data/Logs.log", "a")
#     first_l = "Connecting to server on ip", sshServer + "."
#     logss.write(str(first_l)+"\n")
#     try:
#         connection = ssh(sshServer, sshUsername, sshPassword, logss)
#         connection.openShell()
#         connection.sendShell("cd Desktop/Final\ Project/finalyearproject/ && python3 75_text.py")
#     except Exception as e:
#         logss.write(str(e)+"\n")
#         print(e)
#         logss.close()
   
# if __name__=='__main__':
#     start_ssh()
    