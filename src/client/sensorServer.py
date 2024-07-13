import socket

class SensorServer:
    OK              = 0x0
    DISCONNECT      = 0x11
    MOTION_DETECTED = 0x12
    def __init__(self, ip_addr: str):
        self.ip_addr = ip_addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip_addr, 20000))
    
    def await_message(self):
        message = int.from_bytes(self.sock.recv(1))
        if message in (self.OK, self.DISCONNECT, self.MOTION_DETECTED):
            if message == self.MOTION_DETECTED:
                self.sock.send(int.to_bytes(self.OK))
            return message
        else:
            self.disconnect()
            return None
    
    def disconnect(self):
        self.sock.close()


        