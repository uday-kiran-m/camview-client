import threading
import clientmod
import socket
import pickle
import mysql.connector
import time


conn = mysql.connector.connect(host = 'localhost', user="camview", passwd="Camview@123",database="camview",auth_plugin='mysql_native_password')
cursor = conn.cursor()
cursor.execute('select email from auth_user where is_superuser = 1')
for i in cursor:
    email = i[0]
print(email)

def daemontalk(ev):
    commands = {}
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('127.0.0.1',5998))
    s.listen()
    client = ''
    while not ev.is_set():
        try:
            s.settimeout(5)
            client,addr = s.accept()
        except:
            pass
        s.settimeout(None)
        if client != '':
            try:
                data = pickle.loads(client.recv(2048))
                if data[0] in commands:
                    if len(data) == 1:
                            ret = exec(commands[data])
                            client.send(ret)
                            client.close()
                            client = ''

                else:
                    client.send(pickle.dumps([False]))
                    client.close()
                    client = ''
            except:
                client.close()
                client = ''
    else:
        s.close()
        print('server close')
if __name__=="__main__":
    ev = threading.Event()
    daemon = clientmod.camview(email)
    t = threading.Thread(target=daemontalk,daemon=True,args=(ev,))
    d = threading.Thread(target=daemon.connect,daemon=True)
    t.start()
    print('start talk')
    d.start()
    print('daemon start')
    try:
        while not ev.is_set():
            time.sleep(5)
    except KeyboardInterrupt:
        print('stopping')
        ev.set()
        t.join()
        daemon.stop()
        d.join()
    except Exception as e:
        print(e)