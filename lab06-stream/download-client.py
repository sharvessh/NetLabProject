import os,sys,socket

SERVER_HOST, SERVER_PORT = "127.0.0.1", 54323

name = input("File to download: ").strip()
if name == "":
    print("No file name entered")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((SERVER_HOST, SERVER_PORT))
except ConnectionRefusedError:
    print("Server is not running on port " + str(SERVER_PORT))
    sys.exit(1)

# Request: the file name on one line
request = name + "\n"
sock.sendall(request.encode())

# Response header: keep calling recv() until the \n arrives
buf = b""
while b"\n" not in buf:
    data = sock.recv(4096)
    if not data:                    # server closed before sending a full header
        break
    buf += data

if b"\n" not in buf:
    print("Server closed the connection")
    sock.close()
    sys.exit(1)

# Split: the header line, and the rest (the start of the file, if any came with it)
header, buf = buf.split(b"\n", 1)
status, value = header.decode().strip().split(",", 1)
if status != "OK":
    print("Server says: " + value)
    sock.close()
    sys.exit(1)

# Save the file: first the bytes already in buf, then recv() the rest
size = int(value)
save_as = "downloaded_" + os.path.basename(name)
with open(save_as, "wb") as out:
    out.write(buf)                  # do not lose the bytes that came with the header
    remaining = size - len(buf)
    while remaining > 0:
        chunk = sock.recv(min(4096, remaining))
        if not chunk:               # server closed early
            break
        out.write(chunk)
        remaining -= len(chunk)

sock.close()
print("Saved " + save_as + " (" + str(size - remaining) + " of " + str(size) + " bytes)")
