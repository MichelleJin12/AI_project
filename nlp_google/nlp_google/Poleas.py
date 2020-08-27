import multiprocessing
import time
from redis import Redis
cli = Redis('localhost')

for bot in ('real_time_face_recognition','transcribe_streaming_mic'):
    p = multiprocessing.Process(target=lambda: __import__(bot))
    p.start()

# time.sleep(4)
while True:

    voice_flag = cli.get('share_mic')
    # face_flag  = cli.get('share_rec')
    voice_flag = voice_flag.decode()
    # face_flag  = face_flag.decode()
    face_flag = '10'
    if voice_flag != '5' and face_flag != '6':
        print("voice_flag = " + voice_flag)
        print("face_flag = " + face_flag)
        #==여기서 문자 메세지가 가야된다==
    elif voice_flag != '5':
        print("voice_flag = " + voice_flag)
    elif face_flag != '6':
        print("face_flag = " + face_flag)
    else:
        pass

    time.sleep(1)


