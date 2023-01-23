# Código para receber o vídeo
import cv2, imutils, socket
import numpy as np
import time, os
import base64
import threading, wave, pyaudio,pickle,struct

# Acessando o socket para receber o vídeo
BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_ip = '26.173.255.200' # Insira o ip do host
port = 8080 # Insira a porta do host

# Ligando e enviando mensagem ao socket server
message = b'Socket Conectado!'
client_socket.sendto(message,(host_ip,port))


def video_stream():
	# Criando janelas e variáveis importantes
	cv2.namedWindow('Recebendo video!')        
	cv2.moveWindow('Recebendo video!', 10,360) 
	fps,st,frames_to_count,cnt = (0,0,20,0)

	# Definindo loop de execução de vídeo
	while True:
		#
		packet, ignore = client_socket.recvfrom(BUFF_SIZE)
		data = base64.b64decode(packet,' /')
		npdata = np.fromstring(data,dtype=np.uint8)
	
		frame = cv2.imdecode(npdata,1)
		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		frame = imutils.resize(frame,width=600)
		cv2.imshow('Recebendo video!',frame)
		key = cv2.waitKey(1) & 0xFF
	
		if key == ord('q'):
			client_socket.close()
			os._exit(1)
			break

		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1
		
			
	client_socket.close()
	cv2.destroyAllWindows()




from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=2) as executor:
	executor.submit(video_stream)
