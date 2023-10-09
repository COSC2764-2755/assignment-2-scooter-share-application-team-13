#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/struct.html
import socket, json, struct



#Methods showen in class, send json (sends json data) and recvJson (Receives and turns into dictionary)
def sendJson(socket: socket.socket, object):
    jsonString = json.dumps(object)
    data = jsonString.encode("utf-8")
    jsonLength = struct.pack("!i", len(data))
    socket.sendall(jsonLength)
    socket.sendall(data)

def recvJson(socket: socket.socket):
    buffer = socket.recv(4)
    jsonLength = struct.unpack("!i", buffer)[0]

    # Reference: https://stackoverflow.com/a/15964489/9798310
    buffer = bytearray(jsonLength)
    view = memoryview(buffer)
    while jsonLength:
        nbytes = socket.recv_into(view, jsonLength)
        view = view[nbytes:]
        jsonLength -= nbytes

    jsonString = buffer.decode("utf-8")
    return json.loads(jsonString)  #parses it into a Python dictionary before returning
