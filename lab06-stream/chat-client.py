import socket
import sys
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox


HOST, PORT = "127.0.0.1", 54324      # change HOST to the server's IP address

# ---- window ----
root = tk.Tk()
root.geometry("360x520")
name = simpledialog.askstring("Name", "Your name:", parent=root) or "Guest"
root.title("Chat - " + name)

# ---- connect ----
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cli_sock.connect((HOST, PORT))
except ConnectionRefusedError:
    messagebox.showerror("Cannot connect", "Server is not running on port " + str(PORT))
    root.destroy()
    sys.exit(1)
cli_sock.sendall((name + "\n").encode())       # first line = my name

# ---- chat area (green on the right = me, white on the left = others) ----
chat = tk.Text(root, state="disabled", wrap="word", bg="#ece5dd", padx=8, pady=8)
chat.pack(fill="both", expand=True)
chat.tag_configure("me", justify="right", background="#dcf8c6", rmargin=8, spacing3=6)
chat.tag_configure("other", justify="left", background="white", lmargin1=8, lmargin2=8, spacing3=6)
chat.tag_configure("sys", justify="center", foreground="gray", spacing3=6)


def show(text, tag):
    chat.config(state="normal")
    chat.insert("end", text + "\n", tag)
    chat.config(state="disabled")
    chat.see("end")


# ---- bottom bar ----
bar = tk.Frame(root)
bar.pack(fill="x")
entry = tk.Entry(bar)
entry.pack(side="left", fill="x", expand=True, padx=4, pady=4)
entry.focus()


def send(event=None):
    text = entry.get().strip()
    if text:
        try:
            cli_sock.sendall((text + "\n").encode())
        except OSError:                        # server gone: reset, broken pipe, ...
            show("Server is gone, message not sent", "sys")
            return
        show(text, "me")
        entry.delete(0, "end")


entry.bind("<Return>", send)
tk.Button(bar, text="Send", command=send).pack(side="right", padx=4)


# ---- receive in the background so the window never freezes ----
def receive():
    buf = b""                                  # bytes received but not yet shown
    try:
        while True:
            data = cli_sock.recv(1024)
            if not data:                       # b'' = the server closed the connection
                break
            buf += data

            # show every complete line; keep a half line in buf for next time
            while b"\n" in buf:
                raw, buf = buf.split(b"\n", 1)
                sender, text = raw.decode().strip().split("|", 1)
                if sender == "*":
                    root.after(0, show, text, "sys")
                else:
                    root.after(0, show, sender + ": " + text, "other")
    except OSError:
        pass
    root.after(0, show, "Disconnected from server", "sys")


threading.Thread(target=receive, daemon=True).start()
root.mainloop()
cli_sock.close()
