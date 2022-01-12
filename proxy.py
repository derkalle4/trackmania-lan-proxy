import socket
import time
import threading
import select
from core.trackmania import Trackmania
from core.tcp import TcpRelay
from core.udp import UdpRelay
from core.debug import debugmsg

worker = True


if __name__ == '__main__':
    remoteHost = '157.90.229.248'
    remotePort = 2350
    debugmsg('MAIN', 'starting proxy and redirecting local port {} to {}'.format(remoteHost, remotePort))
    tcp = TcpRelay(remoteHost, remotePort)
    tcp.start_thread()
    udp = UdpRelay(remoteHost, remotePort)
    udp.start_thread()
    tm = Trackmania(remotePort)
    tm.start_thread()
    try:
        debugmsg('MAIN', 'startup complete')
        while(True):
            time.sleep(.5)
    except KeyboardInterrupt:
        debugmsg('MAIN', 'stopping proxy')
        worker = False
        tcp.stop_thread()
        udp.stop_thread()
        tm.stop_thread()
        quit()
    