import constRPC
import time
import threading
from context import lab_channel
import logging

class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None
        self.logger = logging.getLogger("vs2lab.lab2.rpc.client")
        self.logger.info("init client")

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')


    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        ret = None
        if msgrcv[1] == "ACK":
            print("ACK received. Waiting for Data from Server")
            msgrcv = self.chan.receive_from(self.server)
            ret = msgrcv[1]
        # return ret  # pass it to caller
        print("Result: {}".format(ret.value))

    def run_append(self, data, db_list, on_success, on_error):
        assert isinstance(db_list, DBList)
        self.logger.info("start myAppend")
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        if msgrcv[1] == "ACK":
            self.logger.info(msgrcv[1])
            print("ACK received. Waiting for Data from Server")
            wait = WaitThread(self, on_success)
            wait.start()
        else:
            on_error("NO ACK")
            self.logger.info("finish myAppend")
        return


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                self.chan.send_to({client}, "ACK")
                time.sleep(10)
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore


class WaitThread(threading.Thread):
    def __init__(self,client, on_success ):
        threading.Thread.__init__(self)
        self.client = client
        self.success = on_success
        self.msgrcv = None

    def run(self):
        self.msgrcv = self.client.chan.receive_from(self.client.server)
        self.client.logger.info("Got Message From Server")
        self.success(self.msgrcv[1])


