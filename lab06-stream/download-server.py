import os,socket

HOST, PORT = "0.0.0.0", 54323

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((HOST, PORT))
serv_sock.listen()
print("File server ready on port " + str(PORT) + " (serving files in this folder)")

try:
    while True:
        cli_sock, cli_addr = serv_sock.accept()
        print("Connected by " + str(cli_addr))
        try:
            # Request: one line with the file name. Keep calling recv() until \n arrives.
            buf = b""
            while b"\n" not in buf:
                data = cli_sock.recv(1024)
                if not data:                   # client closed before sending a full line
                    break
                buf += data

            line = buf.split(b"\n", 1)[0]      # everything before the first \n
            name = line.decode().strip()
            name = os.path.basename(name)      # safety: only files in this folder

            if name == "" or not os.path.isfile(name):
                cli_sock.sendall("ERROR,File not found\n".encode())
                print("Not found: " + name)
            else:
                # Response: header "OK,size\n", then exactly size bytes
                size = os.path.getsize(name)
                header = "OK," + str(size) + "\n"
                cli_sock.sendall(header.encode())
                with open(name, "rb") as file:
                    while chunk := file.read(4096):
                        cli_sock.sendall(chunk)
                print("Sent " + name + " (" + str(size) + " bytes)")
        except OSError as e:                   # client reset, broken pipe, ...
            print("Problem with client " + str(cli_addr) + ": " + str(e))
        finally:
            cli_sock.close()
except KeyboardInterrupt:
    print("Server stopped")
finally:
    serv_sock.close()
