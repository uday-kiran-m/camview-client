import socket
import struct
import pickle
import threading
import time
import numpy as np
import cv2
import math
import sys
from django.conf import settings
import django
import os
sys.path.insert(1,'../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'camview.settings'
django.setup()
from gui.models import cams


class camview:
    def __init__(self,email) -> None:
        self.ip =  socket.gethostbyname('cam.uday-server.com')
        self.port = 5999
        self.size = struct.calcsize('I')
        self.cams = {}
        self.status = True
        self.buffer = 2048
        self.email = email
        self.commands = {'udpstream':'soon','udpstreamstop':'soon','statusping':'soon'}
        self.udps = {}
    def camurl(self):
        cam = cams.objects.all()
        for i in cam:
            self.cams[i.id] = i.url
        print(self.cams)

    def structure(self,msg):
        size = len(pickle.dumps(msg))
        size = struct.pack('I',size)
        return size,pickle.dumps(msg)

    def connect(self):#use
        connected = False
        self.camurl()
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(self.ip)
        while not connected:
            try:
                self.server.connect((self.ip,self.port))
                connected = True
                self.status = True
            except:
                pass
        print('connected')
        data = {'auth':'namex','d_id':1,'cams':list(self.cams.keys()),'email':self.email}
        print(data['cams'])
        size,data = self.structure(data)
        try:
            self.server.send(size+data)
            print('sent data')
            data = self.server.recv(1024).decode()
            print('recv data')
        except:
            self.server.close()
            self.connect()
        if data == 'granted':
            print('granted')
            threading.Thread(target=self.standby,daemon=True).start()
        else:
            pass
    def standby(self):
        while self.status:
            data = b''
            # print('hmm')
            while len(data) < self.size:
                data += self.server.recv(1024)
                print('.,.,.')
                if data == b'':
                    print('hmm1')
                    self.status = False
                    print('hm2')
                    self.connect()
                    break
            if self.status:
                print('recving')
                sizereq = data[0:self.size]
                data = data[self.size:]
                sizereq = struct.unpack('I',sizereq)[0]
                while len(data) < sizereq:
                    data+= self.server.recv(1024)
                print('recived')
                command = pickle.loads(data)
                print(command)
                if command[0] in self.commands.keys():
                    if command[0]=='udpstreamstop':
                        cam = command[1]['cam']
                        ev = self.udps[cam]
                        ev.set()
                    elif command[0]=='udpstream':
                        cam = command[1]['cam']
                        port = command[1]['port']
                        udpev = threading.Event()
                        self.udps[cam] = udpev
                        self.server.send(pickle.dumps(True))
                        t = threading.Thread(target=self.udpsend,args=(cam,port,udpev),daemon=True)
                        print('starting udp stream')
                        t.start()
                    elif command[0]=='statusping':
                        self.server.send(pickle.dumps('stillconnected'))
                        print('sent ping')
                    else:
                        pass
    def vid(self,cam,evudp):
        vid = cv2.VideoCapture(self.cams[cam])
        vid.set(cv2.CAP_PROP_FPS,15)
        print(self.cams[cam])
        # print('cap')
        i = 0
        while not evudp.is_set():#change to a variable
            ret ,frame = vid.read()
            if ret:
                yield(frame)
            else:
                i+=1
                if i >=10:
                    vid.release()
                    vid = cv2.VideoCapture(self.cams[cam])
                time.sleep(1)
        else:
            vid.release()
            print('close cam')
    
    def stop(self):
        self.status = False
        self.server.close()
        for i in self.udps:
            ev= self.udps[i]
            ev.set()


    def udpsend(self,cam,port,evudp):
        udpserv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        frames = self.vid(cam,evudp)
        print(port)
        ss = self.splitsend(udpserv,port,self.ip)
        while not evudp.is_set():#change to variable
            frame = next(frames)
            # print('.')
            ss.udp_frame(frame)
            # size,frame= self.structure(frame)
            # udpserv.sendto(size,(self.ip,port))
            # udpserv.sendto(frame,(self.ip,port))
        else:
            print('stop udp')
            try:
                frame = next(frames)
            except:
                pass
            udpserv.close()

    class splitsend:
        
        def __init__(self, sock, port,addr):
            self.MAX_DGRAM = 2**16
            self.MAX_IMAGE_DGRAM = self.MAX_DGRAM - 64
            self.s = sock
            self.port = port
            self.addr = addr
        def udp_frame(self, img):
            compress_img = cv2.imencode('.jpg', img)[1]
            dat = compress_img.tostring()
            size = len(dat)
            num_of_segments = math.ceil(size/(self.MAX_IMAGE_DGRAM))
            array_pos_start = 0
    
            while num_of_segments:
                array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
                self.s.sendto(
                    struct.pack("B", num_of_segments) +
                    dat[array_pos_start:array_pos_end], 
                    (self.addr, self.port)
                    )
                array_pos_start = array_pos_end
                num_of_segments -= 1

