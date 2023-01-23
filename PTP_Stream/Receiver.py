import socket, cv2, pickle, struct, imutils

# Criar o socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '26.173.255.200' # Aqui fica o IP
port = 9999 # Aqui fica a porta
client_socket.connect((host_ip,port)) # O endereço tem que ser uma tupla

# Definir variável para carga, e o tamanho padrão dela
data = b""
payload_size = struct.calcsize("Q")

# Estabelecer conexão e receber o vídeo
while True:
	
	# Receber dados caso a quantidade de dados recebidos seja menor do que o tamanho de uma palavra decimal
	while len(data) < payload_size:
		packet = client_socket.recv(1024)
		# Ignorar caso o pacote esteja vazio
		if not packet: break
		data += packet

	# Encontrando o tamanho total da mensagem 
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	# Adicionando dados recebidos enquanto não exceder o tamanho da mensagem
	while len(data) < msg_size:
		data += client_socket.recv(64*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	
	# Descompactando e exibindo o frame
	frame = pickle.loads(frame_data)
	frame = imutils.resize(frame,width=720)
	cv2.imshow("Recebendo Vídeo!",frame)
	if cv2.waitKey(1) == '13':
		break

client_socket.close()