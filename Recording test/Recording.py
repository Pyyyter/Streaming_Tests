import cv2, time

# 0 = Webcam 1
video_source = cv2.VideoCapture(0)
running = True

# Codec de vídeo para MP4
codec_code = cv2.VideoWriter_fourcc('M','P','4','V')

Path = "Recordings/Record "+ time.strftime("%d-%b (%H.%M)") + '.mp4'

# Definindo parâmetros para a gravação
videoWriter = cv2.VideoWriter(Path, codec_code, 30.0, (640,480))


# Loop de gravação
while running:
    # Ler o vídeo e o frame.
    ret, frame = video_source.read()

    # Caso o vídeo exista, mostre o frame, e salve.
    if ret:
        cv2.imshow('video', frame)
        videoWriter.write(frame)

    # Definindo o critério de parada
    actual_key = cv2.waitKey(1)
    if actual_key & 0xFF == ord('q'):
        running = not running


#region Liberando os dispositivos e a memória que estão sendo usada
video_source.release()
videoWriter.release()
cv2.destroyAllWindows()
#endregion
