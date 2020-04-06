#Copyright (c) 2020 Derek Frombach
#must be run in windows with at least python3.6, must have libjpegturbo installed in c:\\libjpeg-turbo-gcc
import cv2
import numpy as np
import socket
from turbojpeg import TurboJPEG
import time
import argparse

host='1.1.1.1'
port=8082
tout=5.0
buff=1500

jpeg=TurboJPEG('C:\\libjpeg-turbo-gcc\\bin\\libturbojpeg.dll')

#parsement paper
parser=argparse.ArgumentParser(description='A Remote Video Viewer')
parser.add_argument('IP',metavar='IP',type=str,nargs=1,help='The Remote IP Address')
args=parser.parse_args()
host=args.IP[0]

#Function call speedups
show=cv2.imshow
dec=jpeg.decode
waitK=cv2.waitKey
flip=cv2.flip
tp=time.perf_counter
ts=time.sleep
rdwr=socket.SHUT_RDWR
ste=socket.timeout
se=socket.error


#Opening the remote IP and initalizing recieve buffer
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
die=False
while True:
    try:
        s.connect((host,port))
    except ste as e:
        #print(e)
        cv2.destroyAllWindows()
        ts(0.1)
        continue
    except se as e:
        #print(e)
        cv2.destroyAllWindows()
        ts(0.1)
        continue
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        s.close()
        break
    print('connected')
    sr=s.recv
    ss=s.send
    c=b''
    s.settimeout(tout)
    ss(b'GET /video HTTP/1.1\r\n\r\n')
    while True:
        try:
            c+=sr(buff)
        except ste:
            s.shutdown(rdwr)
            s.close()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
            #cv2.destroyAllWindows()
            print('disconnected timeout')
            break
        except se as e:
            s.shutdown(rdwr)
            s.close()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
            #cv2.destroyAllWindows()
            print('disconnected error')
            #print(e)
            break
        except KeyboardInterrupt:
            s.shutdown(rdwr)
            s.close()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
            #cv2.destroyAllWindows()
            print('disconnected')
            break
        #Check for JPEG beginning and end
        a = c.find(b'\xff\xd8') 
        b = c.find(b'\xff\xd9')
        if a != -1 and b != -1: #Found JPEG beginning and end
            ta=tp()
            try:
                ss(b'GET /video HTTP/1.1/r/n/r/n')
            except ste:
                s.shutdown(rdwr)
                s.close()
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
                #cv2.destroyAllWindows()
                print('disconnected timeout')
                break
            except se as e:
                s.shutdown(rdwr)
                s.close()
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
                #cv2.destroyAllWindows()
                print('disconnected error')
                #print(e)
                break
            except KeyboardInterrupt:
                s.shutdown(rdwr)
                s.close()
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
                #cv2.destroyAllWindows()
                print('disconnected')
                break
            #Decoding
            jpg = c[a:b+2]
            c = c[b+2:] #Clear Buffer
            try:
                i = dec(jpg,flags=2048)
            except:
                continue
            #Displaying
            #chopit(i.flatten().tobytes())
            show('i',i)
            if waitK(1) == ord('q'): #EXIT KEY IS 'q'
                s.shutdown(rdwr)
                s.close()
                cv2.destroyAllWindows()
                print('disconnected')
                die=True
                break
            tb=tp()
            tc=tb-ta
            print(1.0/tc)
    if die:
        break
