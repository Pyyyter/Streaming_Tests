import socket, cv2, pickle, struct

# Create
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '26.216.222.96' # Aqui fica o IP
port = 9999
client_socket.connect((host_ip,port)) # IP tem que ser uma tupla
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client_socket.recv(1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(64*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	cv2.imshow("RECEIVING VIDEO",frame)
	if cv2.waitKey(1) == '13':
		break
client_socket.close()