import socket

# SOLVED version: message framing (see server-hello-solved.py)

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

    # FIX 1: end every greeting with \n so the server can separate them
    for greetings in ['Hi server !!', 'How are you?', 'Bye server']:
        sock.sendall((greetings + '\n').encode('utf-8'))
        print('Sent:', greetings)

    # FIX 2: send the size first, then the big message
    big = b'X' * 100000
    header = 'SIZE ' + str(len(big)) + '\n'
    sock.sendall(header.encode('utf-8'))
    sock.sendall(big)
    print('Sent one message of', len(big), 'bytes')

    # FIX 3: read the reply until the server closes the connection (recv returns b'')
    msg = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        msg += data
    print('Received: ', msg.decode('utf-8', errors='replace'))

except OSError as e:         # one except covers refused, timeout, unknown host, reset
    print('Error:', e)
finally:
    sock.close()
