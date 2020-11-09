import logging
import socket

import constCS
from context import lab_logging

lab_logging.setup()  # init loging channels for the lab


class Server:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Server")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((constCS.HOST, constCS.PORT))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        telefonDB = {'AAA': '123123',
                     'BBB': '321321',
                     'CCC': '123245'}
        self.sock.listen(1)
        (connection, address) = self.sock.accept()  # returns new socket and address of client
        while True:  # forever
            data = connection.recv(1024)  # receive data from client
            if not data:
                break  # stop if client stopped
            self.logger.info("Messages received.")
            if data != b'ALL':
                name = data
                name_str = str(name,'ascii')
                if name_str in telefonDB:
                    connection.send(" Telefonnummer von ".encode('ascii')+ name + " : ".encode('ascii') + telefonDB[name_str].encode('ascii'))
                else:
                    connection.send(" Name nicht gefunden !!! ".encode('ascii'))
            else:
                ret = ''
                ret += ' Alle Telefonnummern: \n'
                for name in telefonDB:
                    ret += 'Name: ' + name + ' Tel: ' + telefonDB[name] + '\n'
                connection.send(ret.encode('ascii'))

        connection.close()  # close the connection
        self.sock.close()
        self.logger.info("Server down.")


class Client:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self,msg_in="GETALL"):
        send = msg_in
        if msg_in.startswith('GET '):
            send = msg_in.strip('GET ')
        elif msg_in == "GETALL":
            send = "ALL"
        else:
            print(" ERROR: WRONG MESSAGE")
            self.sock.close()
            self.logger.info("Socket close.")
            self.logger.info("Client down.")
        self.sock.send(send.encode('ascii'))
        self.logger.info("Messages sent.")
        data = self.sock.recv(1024)
        msg_out = data.decode('ascii')
        print(msg_out)
        self.sock.close()
        self.logger.info("Client down.")
        return msg_out


