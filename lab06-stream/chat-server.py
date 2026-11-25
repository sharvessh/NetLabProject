import socket
import threading

HOST, PORT = "0.0.0.0", 54324
clients = []                 # all connected cli_sock
lock = threading.Lock()


def broadcast(line, sender=None):
    """Send one line to everybody except the sender."""
    with lock:
        for c in clients:
            if c is not sender:
                try:
                    c.sendall(line.encode())
                except OSError:
                    pass


def handle(cli_sock, cli_addr):
    name = None
    buf = b""                                  # bytes received but not yet used
    try:
        while True:
            data = cli_sock.recv(1024)
            if not data:                       # b'' = the client closed the connection
                break
            buf += data

            # buf may now hold 0, 1 or many complete lines: handle each one
            while b"\n" in buf:
                raw, buf = buf.split(b"\n", 1)     # one line = one message
                text = raw.decode(errors="ignore").strip()
                if not text:
                    continue
                if name is None:               # first line is the user's name
                    name = text.replace("|", "")
                    print(name, "joined from", cli_addr)
                    broadcast("*|" + name + " joined the chat\n", cli_sock)
                else:
                    broadcast(name + "|" + text + "\n", cli_sock)
    except OSError:
        pass
    finally:
        with lock:
            clients.remove(cli_sock)
        cli_sock.close()
        if name:
            print(name, "left")
            broadcast("*|" + name + " left the chat\n")


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((HOST, PORT))
serv_sock.listen()
print("Chat server running on port " + str(PORT))

try:
    while True:
        cli_sock, cli_addr = serv_sock.accept()
        with lock:
            clients.append(cli_sock)
        threading.Thread(target=handle, args=(cli_sock, cli_addr), daemon=True).start()
except KeyboardInterrupt:
    print("Server stopped")
finally:
    serv_sock.close()
