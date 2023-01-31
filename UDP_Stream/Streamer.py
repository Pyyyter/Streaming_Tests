# This is server code to send video and audio frames over UDP/TCP

import cv2, imutils, socket, queue, os, time, base64, queue, os

# region Criando socket e abrindo a conexão
BUFF_SIZE = 65536

# Criando as definições do socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

# Definindo endereço do socket
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 8080
socket_address = (host_ip,port)

# Ligando socket e notificando
server_socket.bind(socket_address)
print('Enviando de :',socket_address)
#endregion

#region Declarando variaveis importantes para o video
filename =  "../Assets/WarBoat.mp4"
q = queue.Queue(maxsize=10)
vid = cv2.VideoCapture(filename)
FPS = vid.get(cv2.CAP_PROP_FPS)
global TS
TS = (0.5/FPS)
BREAK=False
#endregion


def video_stream_gen():
    WIDTH=400
    while(vid.isOpened()):
        try:
            # Recebendo o frame e redimensionando para reduzir o tamanho do pacote para envio
            _,frame = vid.read()
            frame = imutils.resize(frame,width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player fechado')
    BREAK=True
    vid.release()
	

def video_stream():
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('Transmitindo video')        
    cv2.moveWindow('Transmitindo video', 10,30) 
    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('Conexao estabelecida com ',client_addr)
        WIDTH=400
        
        while(True):
            frame = q.get()
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1
            
            
            
            cv2.imshow('Transmitindo video!', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
                TS=False
                break	
                
# Ignore

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    #executor.submit(audio_stream)
    executor.submit(video_stream_gen)
    executor.submit(video_stream)
