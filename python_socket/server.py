# %%
import sys
import socket
import multiprocessing
from pynput import keyboard


HOST = '192.168.0.8'  # Standard loopback interface address (localhost)
PORT = 9002        # Port to listen on (non-privileged ports are > 1023)

ACK = bytearray([1])

def server():
    print("Server started. Press esc to quit")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    print(data.decode("utf-8"))
                    if not data:
                        break
                    conn.sendall(ACK)
                    with open(f"{addr[0]}.txt", "wb") as f:
                        f.write(data)


def on_press(key):
    if key == keyboard.Key.esc:
        print("Termination process")
        proc.terminate()
        sys.exit()


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    proc = multiprocessing.Process(target=server, args=())
    proc.start()
    listener.join()

# %%
