# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle,struct,imutils

# Criar o socket a partir da máquina local.
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
socket_address = (host_ip,port)

print('HOST IP:',host_ip)

# Ligando o socket
server_socket.bind(socket_address)

# Permitir a conexão de 3 receivers ao mesmo tempo
server_socket.listen(3)
print("LISTENING AT:",socket_address)

# Iniciar a transmissão
while True:

	# Aceitar a conexão
	client_socket, address = server_socket.accept()
	print('GOT CONNECTION FROM:', address)
	if client_socket:

		# Carregando o vídeo
		video = cv2.VideoCapture('Assets\WarBoat.mp4')

		# Trasmitindo o vídeo
		while(video.isOpened()):
			
			# Lendo o vídeo
			img,frame = vid.read()

			# Dando resize para diminuir o tamanho do pacote para envio
			frame = imutils.resize(frame,width=200)

			# Empacotando o frame para enviar
			data = pickle.dumps(frame)
			message = struct.pack("Q",len(data))+data
			client_socket.sendall(message)
			
			# Trasmitir a imagem
			cv2.imshow('Trasmitindo video',frame)
			
			# Verificar se devemos fechar
			if cv2.waitKey(1) == 'p':
				client_socket.close()