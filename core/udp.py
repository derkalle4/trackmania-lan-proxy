import socket
import threading
from core.debug import debugmsg


class UdpRelay:
    """
    Relay for UDP
    """

    def __init__(self, local_address="127.0.0.1", remote_address="127.0.0.1", remote_port=9987):
        debugmsg('UDP', 'starting UDP proxy')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.knownServer = (remote_address, remote_port)
        self.socket.bind((local_address, remote_port))
        self.knownClient = None

        self.thread = None
        self.run_loop = True

    def disconnect_client(self, addr, socket):
        socket.close()

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()

    def stop_thread(self):
        debugmsg('UDP', 'stopping UDP proxy')
        self.run_loop = False
        # close one socket so that select returns
        self.socket.close()

    def relay(self):
        debugmsg('UDP', 'started UDP proxy')
        while(self.run_loop):
            try:
                while(self.run_loop):
                    data, addr = self.socket.recvfrom(32768)
                    if self.knownClient is None or addr != self.knownServer:
                        self.knownClient = addr
                    if addr == self.knownClient:
                        self.socket.sendto(data, self.knownServer)
                    else:
                        self.socket.sendto(data, self.knownClient)
            except:
                self.knownClient = None
                continue
