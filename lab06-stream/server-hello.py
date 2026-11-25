import socket

# usage: python server-hello.py [port]
SERVER_HOST = '0.0.0.0'      # listen on every network interface
#SERVER_HOST = ''
#SERVER_HOST = '192.168.72.130'
#SERVER_HOST = 'sharvessh.sarolab.my'

SERVER_PORT = 54321
BACKLOG = 5
CLIENT_TIMEOUT = 10          # seconds to wait for a silent client

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((SERVER_HOST, SERVER_PORT))
serv_sock.listen(BACKLOG)
print('Server waiting for a connection request on port', SERVER_PORT, '... (Ctrl+C to stop)')

try:
    while True:
        cli_sock, cli_addr = serv_sock.accept()
        cli_sock.settimeout(CLIENT_TIMEOUT)
        try:
            print('Connected by: ', cli_addr)

            # One recv() is fine for a short greeting.
            # Longer messages need message framing.
            msg = cli_sock.recv(1024)

            if msg:
                print('Received:', msg.decode('utf-8', errors='replace'))
                welcome = 'Hi client, Welcome to Hello Server. Bye!!'
                cli_sock.sendall(welcome.encode('utf-8'))
                print('Sent welcome message to client: ', cli_addr[0])
            else:
                print('No data from', cli_addr[0])

        except OSError as e:     # one except covers timeout, reset, broken pipe
            print('Problem with client', cli_addr[0], ':', e)
        finally:
            cli_sock.close()
except KeyboardInterrupt:
    print('\nServer stopped')

serv_sock.close()