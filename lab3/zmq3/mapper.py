import pickle
import sys
import time
import string
import zmq

import constPipe

me = 'Mapper ' + str(sys.argv[1])
address = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  # 1st task src
address1 = "tcp://" + constPipe.SRCMAP + ":" + constPipe.PORTMAP1
address2 = "tcp://" + constPipe.SRCMAP + ":" + constPipe.PORTMAP3

context = zmq.Context()

pull_socket = context.socket(zmq.PULL)  # connect to splitter
pull_socket.connect(address)  # connect to splitter

push_socket = context.socket(zmq.PUSH) # to reducer 1
push_socket_2 = context.socket(zmq.PUSH) # to reducer 2
push_socket.connect(address1)
push_socket_2.connect(address2)

print("{} started".format(me))

time.sleep(1)
while True:
    receive = pull_socket.recv().decode() # receive work from a source
    for word in receive.split():
        if word[0].lower() in string.ascii_lowercase[0:14]:
            push_socket.send(word.encode())
        else:
            push_socket_2.send(word.encode())




