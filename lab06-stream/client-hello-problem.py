import socket
import time

# PROBLEM version: sends 3 greetings, then one big message

#SERVER_HOST = '127.0.0.1'
SERVER_HOST = '10.0.2.15'
SERVER_PORT = 54321
TIMEOUT = 10                 # seconds

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(TIMEOUT)     # applies to connect() and recv()

try:
    sock.connect( (SERVER_HOST, SERVER_PORT) )
    print('Client: ', sock.getsockname())
    print('Connected to:', sock.getpeername())

    # 3 greetings, 3 sendall() calls, no separator between them
    for greetings in ['Hi server !!', 'How are you?', 'Bye server']:
        sock.sendall(greetings.encode('utf-8'))
        print('Sent:', greetings)

    msg = sock.recv(1024)
    print('Received: ', msg.decode('utf-8', errors='replace'))

    # one big message of 100000 bytes
    big = b'X' * 100000
    sock.sendall(big)
    print('Sent one message of', len(big), 'bytes')

except OSError as e:         # one except covers refused, timeout, unknown host, reset
    print('Error:', e)
finally:
    sock.close()
