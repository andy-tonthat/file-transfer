#---[ Global Imports ]---------------------------------------------------------
from pathlib import Path

#---[ Global Imports ]---------------------------------------------------------



#---[ Main Function ]----------------------------------------------------------
def main() -> None:
    serverIP = setServerIp()

    print(f"The set server IP address: {serverIP}")
    
    return

#---[ Main Function ]----------------------------------------------------------

def setServerIp() -> None:
    serverIP = ""
    validAddress = False

    print("IPv4 Addresses Only: xxx.xxx.xxx.xxx")

    while not validAddress:
        serverIP = input("Enter the receiving computer's IP address: ")

        ipComponents = serverIP.split(".")
        if len(ipComponents) != 4:
            print("Error: Please try again. Use only four numbers separated by periods.\n")
            continue

        validAddress = True

        for component in ipComponents:
            if not component.isnumeric():
                print("Error: Please try again. Use only numbers.\n")
                validAddress = False
                break
            elif int(component) < 0 or int(component) > 255:
                print("Error: Please try again. Use only numbers in the range [0, 255].\n")
                validAddress = False
                break
    
    serverIPFilePath = Path(__file__).parent.resolve() / "utils" / "server_ip.txt"
    with serverIPFilePath.open("w") as outFile:
        outFile.write(serverIP)

    return serverIP


#---[ Entry ]------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]------------------------------------------------------------------