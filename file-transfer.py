#---[ Global Imports ]---------------------------------------------------------
from utils.file_sender   import Client
from utils.file_receiver import Server

from pathlib import Path

#---[ Global Imports ]---------------------------------------------------------


#---[ Main Function ]----------------------------------------------------------
def main() -> None:
    printBanner("File Transfer")
    print(" 0 -> Send Files")
    print(" 1 -> Receive Files")
    choice = input(" Enter a numeric option from above: ")
    print()

    if choice == '0':
        printBanner("Send Files")
        input("Press [Enter] once the receiver is listening: ")
        serverIP = getServerIPAddress()
        client = Client(serverIP)
        client.sendFilesToServer()
    else:
        server = Server()
        server.receiveFilesFromClient()

    return

#---[ Main Function ]----------------------------------------------------------

def getServerIPAddress() -> str:
    serverIPFilePath = Path(__file__).parent.resolve() / "utils" / "server_ip.txt"
    if not serverIPFilePath.exists():
        print("Error: No server IP address found. Go set it using set_server_ip.py")
        input("Press [Enter] to close the program: ")
        raise SystemExit

    serverIPAddress = ""
    with serverIPFilePath.open("r") as inFile:
        serverIPAddress = inFile.read().strip()

    return serverIPAddress

def printBanner(message: str) -> None:
    divider = "-" * 47
    print(f"{divider}\n{message:^47}\n{divider}")

#---[ Entry ]------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]------------------------------------------------------------------