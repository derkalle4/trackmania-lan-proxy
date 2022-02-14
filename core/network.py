import socket
from .debug import debugmsg

def get_ip_address(networkcheck_ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((networkcheck_ip, 80))
        found_ip = s.getsockname()[0]
        if found_ip is None or found_ip == '':
            raise ValueError('no valid value for found_ip')
        debugmsg('NetworkCheck', 'found public interface {} for incoming connections'.format(found_ip))
        return found_ip
    except:
        debugmsg('NetworkCheck', 'could determine public interface, using fallback 0.0.0.0 instead')
        return '0.0.0.0'

            