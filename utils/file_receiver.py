#---[ Global Imports ]---------------------------------------------------------
from   socket       import socket as Socket
from   pathlib      import Path
from   collections  import namedtuple as NamedTuple
from   utils.buffer import Buffer

class Server:
    def __init__(self) -> None:
        AuthTup = NamedTuple("Authority", ("host_ip", "port"))
        IP, PORT = "0.0.0.0", 5001
        self.BUFFER_SIZE = 2 ** 12
        
        self.RECEIVE_FILES_DIR = Path(__file__).parent.parent.resolve() / "receive"
        self.AUTH = AuthTup(IP, PORT)
        self.TIMEOUT_LIMIT_IN_SEC = 5

        if not self.RECEIVE_FILES_DIR.exists():
            self.RECEIVE_FILES_DIR.mkdir()
        
        return
    
    def receiveFilesFromClient(self) -> None:
        with Socket() as socket:
            socket.bind(self.AUTH)
            socket.listen(self.TIMEOUT_LIMIT_IN_SEC)
            self.logServer(f"Listening as {self.AUTH.host_ip}:{self.AUTH.port}")

            clientSocket, clientAddress = socket.accept()
            self.logServer(f"Connected from {clientAddress}!")

            buffer = Buffer(clientSocket)

            while True:
                fileName = buffer.getUTF8()
                if not fileName: break
                fileSize = int(buffer.getUTF8())
                if not fileSize and fileSize != 0: break

                fileTypeVal = fileName[-1]
                fileName = fileName[:-1]
                self.logServer(f"Harvesting file: {fileName} | {fileSize} bytes")

                filePath = self.RECEIVE_FILES_DIR / fileName
                if fileTypeVal == '0' and not filePath.exists():
                    filePath.mkdir()
                    continue

                with open(filePath, 'wb') as outFile:
                    numBytes = fileSize

                    while numBytes:
                        chunkSize = self.BUFFER_SIZE if numBytes >= self.BUFFER_SIZE else numBytes
                        chunk = buffer.getBytes(chunkSize)
                        if not chunk: break

                        outFile.write(chunk)
                        numBytes -= chunkSize
                    

                    if numBytes:
                        print(f"File is incomplete: {fileName} is missing {numBytes} bytes")
                    else:
                        print(f"Successfully received {fileName}!")

            clientSocket.close()
        
        return
    
    #---[ Logging ]------------------------------------------------------------
    def logServer(self, message: str, msgEnd: str="\n") -> None:
        print(f"[*] {message}", end=msgEnd)
    
    #---[ Logging ]------------------------------------------------------------
