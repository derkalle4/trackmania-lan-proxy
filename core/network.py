import socket


def get_ip_address(networkcheck_ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((networkcheck_ip, 80))
        return s.getsockname()[0]
    except:
        return False