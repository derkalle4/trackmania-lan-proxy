import select
import socket
import threading
import time
from core.debug import debugmsg


class Trackmania:
    """
    LAN reply for Trackmania
    """

    def __init__(self, local_address="127.0.0.1", remote_port=2350):
        debugmsg('TM', 'starting Trackmania LAN reply')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((local_address, remote_port + 1))
        self.thread = None
        self.run_loop = True

    def disconnect_client(self, addr, socket):
        socket.close()

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()

    def stop_thread(self):
        debugmsg('TM', 'stopping Trackmania LAN reply')
        self.run_loop = False
        # close one socket so that select returns
        self.socket.close()

    def relay(self):
        debugmsg('TM', 'started Trackmania LAN reply')
        while(self.run_loop):
            time.sleep(.1)
            try:
                self.socket.setblocking(0)
                ready = select.select([self.socket], [], [], 1)
                if not ready[0]:
                    time.sleep(.1)
                    continue
                m = self.socket.recvfrom(4096)
                if not m[1]:
                    break
                message = m[0].decode('UTF-8', 'replace')
                client_ip = m[1][0]
                client_port = m[1][1]
                if 'ManiaPlanet' not in message:
                    break
                data = bytes.fromhex("80000b4d616e6961506c616e657403333937533b2e000000")
                self.socket.sendto(data, (client_ip, client_port))
                debugmsg('TM', 'sent game reply')
            except:
                continue
