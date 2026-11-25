import socket

# SOLVED version: message framing
#   FIX 1: every greeting ends with \n (delimiter)       -> like the chat server
#   FIX 2: the big message is sent after "SIZE n\n"      -> like download and Content-Length
#   FIX 3: the client reads until the server closes      -> like send-http-request.py

SERVER_HOST = '0.0.0.0'      # listen on every network interface
#SERVER_HOST = ''
#SERVER_HOST = '192.168.72.130'
#SERVER_HOST = 'zanida.netprogram.my'

SERVER_PORT = 54321
BACKLOG = 5
CLIENT_TIMEOUT = 10          # seconds to wait for a silent client

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((SERVER_HOST, SERVER_PORT))
serv_sock.listen(BACKLOG)
print('SOLVED server waiting on port', SERVER_PORT, '... (Ctrl+C to stop)')

try:
    while True:
        cli_sock, cli_addr = serv_sock.accept()
        cli_sock.settimeout(CLIENT_TIMEOUT)
        try:
            print('Connected by: ', cli_addr)

            # FIX 1: keep calling recv() and cut out one line (one message) at a time
            buf = b''                      # bytes received but not used yet
            size = None
            count = 0
            while size is None:
                data = cli_sock.recv(1024)
                if not data:               # b'' = the client closed
                    break
                buf += data
                while b'\n' in buf:
                    line, buf = buf.split(b'\n', 1)
                    text = line.decode('utf-8', errors='replace')
                    if text.startswith('SIZE '):      # header: the big message comes next
                        size = int(text[5:])
                        break
                    count += 1
                    print('Received message', count, ':', text)

            # FIX 2: we know the size, so keep calling recv() until we have it all
            big = buf                      # part of the big message may already be in buf
            calls = 0
            while size is not None and len(big) < size:
                data = cli_sock.recv(4096)
                if not data:
                    break
                big += data
                calls += 1
            print('Received big message:', len(big), 'of', size, 'bytes in', calls, 'recv() calls')

            welcome = 'Hi client, Welcome to Hello Server. I got ' + str(count) + ' messages and ' + str(len(big)) + ' bytes. Bye!!'
            cli_sock.sendall(welcome.encode('utf-8'))
            print('Sent welcome message to client: ', cli_addr[0])

        except OSError as e:     # one except covers timeout, reset, broken pipe
            print('Problem with client', cli_addr[0], ':', e)
        finally:
            cli_sock.close()     # FIX 3: closing marks the end of the reply
        print()
except KeyboardInterrupt:
    print('\nServer stopped')

serv_sock.close()
