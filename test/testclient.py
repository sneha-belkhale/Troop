import socket

def Main():
        host = 'localhost'
        port = 54321

        mySocket = socket.socket()
        mySocket.connect((host,port))

        message = input(" -> ")

        while message != 'q':
                mySocket.send(message.encode())
                message = input(" -> ")

        mySocket.close()

if __name__ == '__main__':
    Main()
