# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle,struct,imutils

# Criar o socket a partir da máquina local.
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Ligando o socket
server_socket.bind(socket_address)

# Permitir a conexão de 3 receivers ao mesmo tempo
server_socket.listen(3)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture('WarBoat.mp4')
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = imutils.resize(frame,width=1080)
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			
			cv2.imshow('TRANSMITTING VIDEO',frame)
			if cv2.waitKey(1) == '13':
				client_socket.close()