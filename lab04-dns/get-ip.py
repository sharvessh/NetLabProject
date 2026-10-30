import socket

domainname = input('Enter domain name: ').strip()
try:
    addrinfo = socket.getaddrinfo(domainname, 'http')
    for addr in addrinfo:
        if addr[0] == socket.AF_INET:
            print('IPV4:',addr[-1][0])
        else:
            print('IPV6:',addr[-1][0])
except socket.gaierror:
    print(domainname, 'Could not be resolved')
except (OSError, UnicodeEncodeError) as e:
    print('Error:', e)

