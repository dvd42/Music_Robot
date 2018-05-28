from __future__ import print_function
import socket
import common


def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


def send_params(params):

    s = connect("192.168.43.86", 8089)
    s = common.send_file(s, params, False, True)
    s.close()
