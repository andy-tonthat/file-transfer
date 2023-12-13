from socket import socket as Socket

class Buffer:
    def __init__(self, socket: Socket) -> None:
        self.socket = socket
        self.buffer = b''
        self.BUFFER_SIZE = 2 ** 10
    
    def getBytes(self, n: int) -> bytes:
        data = b''

        while len(self.buffer) < n:
            data = self.socket.recv(self.BUFFER_SIZE)

            if not data:
                data = self.buffer
                self.buffer = b''
                return data
        
            self.buffer += data
        data, self.buffer = self.buffer[:n], self.buffer[n:]

        return data
    
    def putBytes(self, data: bytes) -> None:
        self.socket.sendall(data)
        return
    
    def getUTF8(self) -> str:
        while b'\x00' not in self.buffer:
            data = self.socket.recv(self.BUFFER_SIZE)
            
            if not data:
                return ""
            
            self.buffer += data
        
        data, seperator, self.buffer = self.buffer.partition(b'\x00')
        return data.decode()
    
    def putUTF8(self, string: str) -> None:
        if '\x00' in string:
            raise ValueError("putUTF8 - Error: string contains delimiter (null)")
        
        self.socket.sendall(string.encode() + b'\x00')
        return
