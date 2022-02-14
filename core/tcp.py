import select
import socket
import threading
import uuid
import time
from core.debug import debugmsg


class TcpClient:
    def __init__(self, socket, addr):
        self._socket = socket
        self.addr = addr
        self.last_seen = time.time()

    def fileno(self):
        return self._socket.fileno()

    @property
    def socket(self):
        self.last_seen = time.time()
        return self._socket

class TcpRelay:
    """
    Relay for TCP
    """

    def __init__(self, local_address="127.0.0.1", remote_address="127.0.0.1", remote_port=9987):
        debugmsg('TCP', 'starting TCP proxy')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((local_address, remote_port))
        self.socket.listen()
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.clients = {}

        self.thread = None
        self.run_loop = True

    def start_thread(self):
        self.thread = threading.Thread(target=self.relay)
        self.thread.start()

    def stop_thread(self):
        debugmsg('TCP', 'stopping TCP proxy')
        self.run_loop = False
        # close one socket so that select returns
        self.socket.close()

    def relay(self):
        debugmsg('TCP', 'started TCP proxy')
        while True:
            readable, writable, exceptional = select.select(list(self.clients.values()) + [self.socket], [], [], 1)
            if not self.run_loop:
                # stop thread
                break
            for s in readable:
                # if ts3 server answers to a client or vice versa
                if isinstance(s, TcpClient):
                    try:
                        data = s.socket.recv(4096)
                        if len(data) != 0:
                            self.clients[s.addr].socket.send(data)
                        else:
                            raise Exception
                    except:
                        # get second socket from list
                        addr = self.clients[s.addr].addr
                        try:
                            # close other socket
                            self.clients[s.addr].socket.close()
                        except:
                            pass
                        try:
                            # close own socket, too
                            self.clients[addr].socket.close()
                        except:
                            pass
                        del self.clients[s.addr]
                        del self.clients[addr]
                else:
                    conn, addr = s.accept()
                    data = conn.recv(4096)
                    tmpuid = str(uuid.uuid4())
                    self.clients[addr] = TcpClient(conn, tmpuid)
                    self.clients[tmpuid] = TcpClient(socket.socket(socket.AF_INET, socket.SOCK_STREAM), addr)
                    self.clients[tmpuid].socket.connect((self.remote_address, self.remote_port))
                    self.clients[tmpuid].socket.send(data)
