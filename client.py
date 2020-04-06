#Copyright (c) 2020 Derek Frombach
import socket
import random
import time
import pygame
import subprocess

pygame.init()
try:
    joy=pygame.joystick.Joystick(0)
except:
    print('PLEASE PLUG IN YOUR JOYSTICK!')
    exit()
joy.init()
num=joy.get_numaxes()
jg=joy.get_axis
ev=pygame.event.get

def lpad(n,i):
    n=str(n)
    while len(n)<i:
        n='0'+n
    return n

def diffSteer(x,y):
    y=-y
    a=y+x
    b=y-x
    if abs(a)>1 or abs(b)>1:
        c=max(abs(a),abs(b))
        a=a/c
        b=b/c
    return a,b

def doconv():
    q=ev()
    x=-jg(0)
    y=jg(1)
    a,b=diffSteer(x,y)
    #print([a,b])
    a=(int(a*32512.0)+32513).to_bytes(2,'little')
    a=bytes([a[0]])+bytes([a[1]+1])
    b=(int(b*32512.0)+32513).to_bytes(2,'little')
    b=bytes([b[0]])+bytes([b[1]+1])
    return a+b+a+b

def cheks(data):
    o=0
    for i in range(0,len(data)):
        o=o^data[i]
    return bytes([o])

def buildblocky(up):
    blocky=b'\x00\x00\x10'
    tup=blocky+up
    blocky+=cheks(tup)+up
    return blocky

def start_video(ip):
    proc=subprocess.Popen(['python','videoview.py',ip])
    return proc

def stop_video(proc):
    proc.terminate()
    

buff=1400 #Don't change this
host='1.1.1.1' #Change this to your server address
ip='0.0.0.0' #DONT CHANGE THIS!
port=8081 #Change this to your server port
tout=0.5 #Quick Timeout for Reconnect
framerate=1.0/30.0
videoretries=4

#Opening the remote IP and initalizing recieve buffer
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero latency TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Unbind when Done

#Function call speedups
rdwr=socket.SHUT_RDWR
ri=random.randint
ts=time.sleep
tc=time.perf_counter
ste=socket.timeout

#Pre-Connection
rin=lpad(ri(0,9999),4)
s.connect((host,port))
s.sendall(('Passwd: '+rin).encode('utf-8'))
print('Sent: '+rin)
data=s.recv(buff)
print(data.decode('utf-8'))
#ts(None)
s.close()

#Hooked
conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Unbind when Done
conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
conn.bind((ip,port)) #Start Server
conn.listen(1) #Listen for Connections

die=False
stillgood=False
ni=0
lip=False
while True:
    #Ctrl-C Handler
    conn.settimeout(tout)
    try:
        s,raddr=conn.accept()
    except KeyboardInterrupt:
        if stillgood:
            try: stop_video(proc)
            except: pass
        break
    except ste:
        if ni>=(videoretries-1) and stillgood:
            stillgood=False
            ni=0
            stop_video(proc)
        elif stillgood:
            ni+=1
        continue
    conn.settimeout(None)

    #Function call speedups
    ur=s.recv
    us=s.sendall
    s.settimeout(tout)

    #Capture loop
    print('IT HAS CONNECTED TO YOU :)')
    if not stillgood:
        proc=start_video(raddr[0])
        stillgood=True
        lip=raddr[0]
    elif lip!=raddr[0]:
        lip=raddr[0]
        if stillgood:
            stop_video(proc)
        proc=start_video(raddr[0])
    while True:
        try:
            #Send the Controller Signal
            up=doconv()
            blocky=buildblocky(up)
            tta=tc()
            us(blocky)
            #Recieve Video
            rdata=ur(buff) #Recieve information
            ttb=tc()-tta
            if ttb>framerate:
                print(ttb)
            #Video Viewer Stop Command Capture
            if proc.poll() != None:
                die=True
                print('Disconnected')
                break
        except:
            print('Disconnected')
            break
    if die:
        break
conn.close()
