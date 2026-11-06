import socket
import errno
import os
from datetime import datetime

print('Welcome to Port Scanner')
host = input('Enter IP address/domain name of a host: ').strip()
print('Enter a range of port numbers')
start_port = int(input('Enter a start port: '))
end_port = int(input('Enter an end port: '))

try:
    # Resolve the host name to IP address
    ip = socket.gethostbyname(host)
    print(f'Scanning port(s) at:  {host} ({ip})')

    open_ports = []

    # Capture current time
    stime = datetime.now()

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Short timeout for scanning multiple ports

        result = sock.connect_ex((ip, port))

        if result == 0:
            print(f'{port} --> Open')
            open_ports.append(port)
        elif result in (errno.EAGAIN, errno.ETIMEDOUT):
            print(f'{port} --> No answer (timed out, maybe a firewall)')
        else:
            name = errno.errorcode.get(result, 'UNKNOWN')
            print(f'{port} --> Closed :Reason: {name}')

        sock.close()

    print(f'Open ports: {open_ports}')

except OSError as e:
    print(f'Error: {e}')
finally:
    if 'stime' in locals():
        print('Port Scanning Completed in: ', datetime.now() - stime)