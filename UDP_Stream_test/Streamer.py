# Esse é o arquivo que tentei abordar o problema jogando frames fora, aumentando significativamente o desempenho
import cv2, imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio,pickle,struct
import sys
import queue
import os

#region Definição de variáveis
global TS
q = queue.Queue(maxsize=10)
filename =  'assets/WarBoat.mp4'
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 8080
video_file = cv2.VideoCapture("Assets\WarBoat.mp4")
FPS = video_file.get(cv2.CAP_PROP_FPS)
TS = (0.5/FPS)
BREAK=False
#endregion

#region Criando socket e abrindo a conexão
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Enviando de :',socket_address)
print('FPS:',FPS,TS)
totalNoFrames = int(video_file.get(cv2.CAP_PROP_FRAME_COUNT))
durationInSeconds = float(totalNoFrames) / float(FPS)
d=video_file.get(cv2.CAP_PROP_POS_MSEC)
print(durationInSeconds,d)
#endregion

# Criando a stream de video
def video_stream_gen():
   
    WIDTH=400
    while(video_file.isOpened()):
        try:
            ignore, frame = video_file.read()
            frame = imutils.resize(frame,width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player fechado')
    BREAK=True
    video_file.release()
	

def video_stream():
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('TRANSMITTING VIDEO')        
    cv2.moveWindow('TRANSMITTING VIDEO', 10,30) 
    while True:
        msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
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
            
            
            
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
                TS=False
                break	
                



from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(video_stream_gen)
    executor.submit(video_stream)
