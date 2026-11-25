import socket, sys

print('Welcome to Simple HTTP Client')
server_host = input('Enter server host: ').strip()
if server_host == '':
    print('No host entered')
    sys.exit(1)

try:
    server_port = int(input('Enter server port: ').strip())
except ValueError:
    print('Port must be a number')
    sys.exit(1)
if server_port < 1 or server_port > 65535:
    print('Port must be between 1 and 65535')
    sys.exit(1)

try:
    sock = socket.create_connection((server_host, server_port), timeout=10)
except OSError as e:                    # name not found, connection refused, timeout, ...
    print('Cannot connect to', server_host, 'port', server_port, ':', e)
    sys.exit(1)

print('Simple HTTP Client: ', sock.getsockname())
print('Connected to: ', sock.getpeername())

# HTTP rule: the Host header must include the port when it is not the default 80
host_header = server_host
if server_port != 80:
    host_header = server_host + ':' + str(server_port)

try:
    print('Requesting to the web content:')
    request = ('GET / HTTP/1.1\r\n' +
               'Host: ' + host_header + '\r\n' +
               'Connection: close\r\n' +
               '\r\n')
    sock.sendall(request.encode('utf-8'))

    # receive until the server closes the connection (recv returns empty bytes)
    response = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    print(response.decode('utf-8', errors='replace'))
except OSError as e:                    # timeout, connection reset, ...
    print('Problem while talking to the server:', e)
finally:
    sock.close()