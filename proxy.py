import yaml
import time
from core.trackmania import Trackmania
from core.tcp import TcpRelay
from core.udp import UdpRelay
from core.debug import debugmsg
from core.network import get_ip_address
from core.header import print_header

worker = True
config = {}


if __name__ == '__main__':
    # print header
    print_header()
    try:
        with open("config.yaml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                quit()
    except EnvironmentError:
        debugmsg('MAIN', 'could not find config.yaml - is it there?')
        quit()
    try:
        clientIP = str(config['client']['ip'])
        networkCheckIP = str(config['client']['networkCheck'])
        remoteHost = str(config['server']['ip'])
        remotePort = int(config['server']['port'])
    except:
        debugmsg('MAIN', 'could not find sever IP and / or PORT - is it defined in the config?')
        quit()
    # check for IP address if automatic
    if clientIP == "automatic":
        clientIP = get_ip_address(networkCheckIP)
    debugmsg('MAIN', 'starting trackmania proxy and redirecting local port {} to {}'.format(remoteHost, remotePort))
    tcp = TcpRelay(clientIP, remoteHost, remotePort)
    tcp.start_thread()
    udp = UdpRelay(clientIP, remoteHost, remotePort)
    udp.start_thread()
    tm = Trackmania(clientIP, remotePort)
    tm.start_thread()
    try:
        debugmsg('MAIN', 'startup complete - run game and search for local servers')
        while(True):
            time.sleep(.5)
    except KeyboardInterrupt:
        debugmsg('MAIN', 'stopping proxy')
        worker = False
        tcp.stop_thread()
        udp.stop_thread()
        tm.stop_thread()
        quit()
    