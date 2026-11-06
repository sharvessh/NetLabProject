import socket

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

    greetings = 'Hi server !!'
    sock.sendall(greetings.encode('utf-8'))
    print('Sent greetings to server:', sock.getpeername())

    # One recv() is fine for a short message.
    # Longer messages need message framing.
    msg = sock.recv(1024)
    if msg:
        print('Received: ', msg.decode('utf-8', errors='replace'))
    else:
        print('The server closed the connection without replying')

except OSError as e:         # one except covers refused, timeout, unknown host, reset
    print('Error:', e)
finally:
    sock.close()