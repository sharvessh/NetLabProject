import socket
import time

# PROBLEM version: shows two TCP problems
#   1. Message boundaries: 3 sendall() calls can arrive in ONE recv()
#   2. Partial receive: a big message does not arrive in ONE recv()

SERVER_HOST = '0.0.0.0'      # listen on every network interface
#SERVER_HOST = '10.0.2.15'
SERVER_PORT = 54321
BACKLOG = 5
CLIENT_TIMEOUT = 10          # seconds to wait for a silent client

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((SERVER_HOST, SERVER_PORT))
serv_sock.listen(BACKLOG)
print('PROBLEM server waiting on port', SERVER_PORT, '... (Ctrl+C to stop)')

try:
    while True:
        cli_sock, cli_addr = serv_sock.accept()
        cli_sock.settimeout(CLIENT_TIMEOUT)
        try:
            print('Connected by: ', cli_addr)

            # PROBLEM 1: the client sent 3 greetings with 3 sendall() calls.
            # Wait 1 second so all of them have arrived, then call recv() ONCE.
            time.sleep(1)
            msg = cli_sock.recv(1024)
            print('PROBLEM 1: one recv() returned:', msg)
            print('  -> 3 messages joined together: TCP does not keep message boundaries')

            welcome = 'Hi client, Welcome to Hello Server. Bye!!'
            cli_sock.sendall(welcome.encode('utf-8'))
            print('Sent welcome message to client: ', cli_addr[0])

            # PROBLEM 2: the client now sends ONE message of 100000 bytes.
            msg = cli_sock.recv(4096)
            print('PROBLEM 2: one recv() returned only', len(msg), 'of 100000 bytes')

        except OSError as e:     # one except covers timeout, reset, broken pipe
            print('Problem with client', cli_addr[0], ':', e)
        finally:
            cli_sock.close()
        print()
except KeyboardInterrupt:
    print('\nServer stopped')

serv_sock.close()
