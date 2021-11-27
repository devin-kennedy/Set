import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import base64
import zmq
import numpy as np

HOST=''
PORT=8485


ngrokip = input("Enter given ngrok ip: ")

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind(ngrokip)
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))


"""
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()
"""

#data = b""
#payload_size = struct.calcsize(">L")
#print("payload_size: {}".format(payload_size))
while True:
    """
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    SET Processing here
    
    sendfdata = pickle.dumps(frame, 0)
    sendsize = len(sendfdata)
    conn.send("Hello from server".encode('utf-8'))
    cv2.imshow('ImageWindow (server-side)',frame)
    """

    frame = footage_socket.recv_string()
    img = base64.b64decode(frame)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    cv2.imshow("Stream", source)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
