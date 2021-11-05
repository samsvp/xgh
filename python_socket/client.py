# %%
import time
import socket

HOST = '192.168.0.56'  # The server's hostname or IP address
PORT = 9003        # The port used by the server

for i in range(10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world\n')
        data = s.recv(1024)

    print('Received', repr(data))
    time.sleep(0.01)
# %%
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'directv\n')
    data = s.recv(1024)

print('Received', repr(data))
# %%
