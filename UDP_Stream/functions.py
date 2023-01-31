import cv2
import imutils
import socket
import os
import time
import base64
import queue
import os
import pyaudio

# Streamer Functions :


def send_video_stream_gen(q, vid):
    WIDTH = 400
    while (vid.isOpened()):
        try:
            # Recebendo o frame e redimensionando para reduzir o tamanho do pacote para envio
            _, frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player fechado')
    BREAK = True
    vid.release()


def send_video_stream(server_socket, FPS, q, frame):
    global TS
    fps, st, frames_to_count, cnt = (0, 0, 1, 0)
    cv2.namedWindow('Transmitindo video')
    cv2.moveWindow('Transmitindo video', 10, 30)
    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('Conexao estabelecida com ', client_addr)
        WIDTH = 400

        while (True):
            frame = q.get()
            encoded, buffer = cv2.imencode(
                '.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message, client_addr)
            frame = cv2.putText(frame, 'FPS: '+str(round(fps, 1)),
                                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st = time.time()
                    cnt = 0
                    if fps > FPS:
                        TS += 0.001
                    elif fps < FPS:
                        TS -= 0.001
                    else:
                        pass
                except:
                    pass
            cnt += 1

            cv2.imshow('Transmitindo video!', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF
            if key == ord('q'):
                os._exit(1)
                TS = False
                break


#region Ignore - Audio
# Streamer :
# Declarations on the code body

# command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')
# os.system(command)


def send_audio_stream():
    s = socket.socket()
    s.bind((host_ip, (port-1)))
    s.listen(5)
    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')
    p = pyaudio.PyAudio()
    print('server listening at', (host_ip, (port-1)))
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket, addr = s.accept()

    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)

# Put this on executor sending loop
# executor.submit(audio_stream)


# Receiver :
def receive_audio_stream():

    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)

    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port-1)
    print('server listening at', socket_address)
    client_socket.connect(socket_address)
    print("CLIENT CONNECTED TO", socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)  # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)

        except:

            break

    client_socket.close()
    print('Audio closed', BREAK)
    os._exit(1)
# endregion
