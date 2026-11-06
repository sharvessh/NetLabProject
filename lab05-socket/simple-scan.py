import socket
import errno
import os
from datetime import datetime
from unittest import result

#SERVER_PORT = 80
SERVER_PORT = 54321

#SERVER_HOST  = 'scanme.nmap.org'
#SERVER_HOST  = 'sharvessh.sarolab.my'
SERVER_HOST  = 'xxx.yy'

print('Scanning port(s) at: ',SERVER_HOST)
stime = datetime.now()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(20)

try:
    # connect_ex() does NOT raise an error when the connection fails.
    # It returns an error number instead (0 means success).
    result = sock.connect_ex((SERVER_HOST, SERVER_PORT))
    if result == 0:
        print(SERVER_PORT, '--> Open')
    elif result in (errno.EAGAIN, errno.ETIMEDOUT):
        # a timeout is also reported as a return code, not as an exception
        print(SERVER_PORT, '--> No answer (timed out, maybe a firewall)')
    else:
        name = errno.errorcode.get(result, 'UNKNOWN')  # e.g. ECONNREFUSED
        print(SERVER_PORT, '--> Closed :Reason:', name, '-', os.strerror(result))
except OSError as e:      # one except covers unknown host, net...
    print('Error:', e)
finally:
    sock.close()          # always runs, even after an error

print('Port Scanning Completed in: ', datetime.now() - stime)