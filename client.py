import socket
while True:
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
	host="192.168.43.153"
	port=12346
	s.connect((host, port))
	a = s.recv(1024)
	a = a.decode()
	print("Distance measured is %s", a)
	s.close