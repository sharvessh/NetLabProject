import os
import socket

pid = os.getpid()
print('Pid of this process:', pid)

hostname = socket.gethostname()
print('Host name:', hostname)