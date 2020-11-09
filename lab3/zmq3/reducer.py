import pickle
import sys
import time

import zmq

import constPipe

me = 'Reducer ' + str(sys.argv[1])
address1 = "tcp://" + constPipe.SRCMAP + ":" + constPipe.PORTMAP1
address2 = "tcp://" + constPipe.SRCMAP + ":" + constPipe.PORTMAP3


context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket

if me == "Reducer 1":
    pull_socket.bind(address1)  # connect to task source 1
else:
    pull_socket.bind(address2)  # connect to task source 1

print("{} started".format(me))

wordsAndCount = {}
lastWord = ""
while True:
    #receive = pickle.loads(pull_socket.recv())  # receive work from a source
    receive = pull_socket.recv().decode()
    if(receive == "AEND" or receive == "OEND"):
        break
    if receive not in wordsAndCount:
        wordsAndCount[receive] = 1
    else:
        wordsAndCount[receive] = wordsAndCount[receive] + 1


for i in wordsAndCount:
    print("Received Word: "+i + ". Number counted:")
    print(wordsAndCount[i])
    print("**************************")
