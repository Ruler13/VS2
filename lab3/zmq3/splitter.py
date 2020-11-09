
import time
import re
import zmq

import constPipe


context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # how and where to connect
push_socket.bind(address)  # bind socket to address

input("Press Button")
time.sleep(1)

file_to_read = 'text.txt'

with open(file_to_read) as f:
    text = f.read()
sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
for sentence in sentences:
    if sentence != '':
        push_socket.send(sentence.encode())

