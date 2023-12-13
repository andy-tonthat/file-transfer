#---[ Global Imports ]---------------------------------------------------------
import os
from   socket       import socket as Socket
from   collections  import namedtuple
from   pathlib      import Path
from   utils.buffer import Buffer

class Client:
    def __init__(self, serverIP: str) -> None:
        SERVER_IP, PORT = serverIP, 5001
        AuthTup = namedtuple("AuthTup", ("server_ip", "port"))

        self.SEND_FILES_DIR = Path(__file__).parent.parent.resolve() / "send"
        self.AUTH = AuthTup(SERVER_IP, PORT)
    
    def sendFilesToServer(self) -> None:
        with Socket() as socket:
            buffer = self.getBuffer(socket)

            snipPos = len(str(self.SEND_FILES_DIR))
            for subtreeRootPath, dirNameList, fileNameList in os.walk(self.SEND_FILES_DIR):
                for dirName in dirNameList:
                    dirPath = str(Path(subtreeRootPath) / dirName)[snipPos+1:]
                    self.sendFile(dirPath, buffer, isFile=False)

                for fileName in fileNameList:
                    filePath = str(Path(subtreeRootPath) / fileName)[snipPos+1:]
                    self.sendFile(filePath, buffer)
        
        return

    #---[ Socket Operations ]--------------------------------------------------
    def getBuffer(self, socket: Socket) -> Buffer:
        self.connectToServer(socket)
        return Buffer(socket)
    
    def connectToServer(self, socket: Socket) -> None:
        self.logClient(f"Looking for {self.AUTH.server_ip}:{self.AUTH.port}")
        socket.connect(self.AUTH)
        self.logClient(f"Connected to {self.AUTH.server_ip}:{self.AUTH.port}")

        return

    def sendFile(self, fileName: str, buffer: Buffer, isFile: bool=True) -> None:
        filePath = self.SEND_FILES_DIR / fileName
        fileSize = os.path.getsize(filePath)

        self.logClient(f"Sending {fileName} | {fileSize} bytes")
        fileName += "1" if isFile else "0"
        buffer.putUTF8(fileName)
        buffer.putUTF8(str(fileSize))
        fileName = fileName[:-1]

        if not isFile: return

        with open(filePath, 'rb') as inFile:
            buffer.putBytes(inFile.read())
        self.logClient(f"Sent {fileName}!", msgEnd="\n\n")

        return
    
    #---[ Socket Operations ]--------------------------------------------------

    #---[ Logging ]------------------------------------------------------------
    def logClient(self, message: str, msgEnd="\n") -> None:
        print(f"[+] {message}", end=msgEnd)
    
    #---[ Logging ]------------------------------------------------------------
