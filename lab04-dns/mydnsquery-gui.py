import tkinter as tk
from tkinter import scrolledtext
import dns.resolver
import dns.exception

RECORD_TYPES = ('A', 'AAAA', 'CNAME', 'NS', 'MX')


def lookup(event=None):
    domain = entry.get().strip()

    output.config(state='normal')
    output.delete('1.0', tk.END)

    if domain == '':
        output.insert(tk.END, 'Please enter a domain name.\n')
        output.config(state='disabled')
        return

    for rtype in RECORD_TYPES:
        output.insert(tk.END, '--- ' + rtype + ' records ---\n')
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                output.insert(tk.END, rdata.to_text() + '\n')
        except dns.resolver.NoAnswer:
            output.insert(tk.END, 'No ' + rtype + ' record found.\n')
        except dns.exception.DNSException as e:
            output.insert(tk.END, 'Error: ' + str(e) + '\n')
            break

    output.config(state='disabled')


def clear():
    entry.delete(0, tk.END)
    output.config(state='normal')
    output.delete('1.0', tk.END)
    output.config(state='disabled')
    entry.focus()


window = tk.Tk()
window.title('DNS Record Lookup')
window.geometry('520x420')

top = tk.Frame(window)
top.pack(padx=10, pady=10, fill='x')

tk.Label(top, text='Domain name:').pack(side='left')
entry = tk.Entry(top)
entry.pack(side='left', padx=5, fill='x', expand=True)
entry.bind('<Return>', lookup)
tk.Button(top, text='Lookup', command=lookup).pack(side='left')
tk.Button(top, text='Clear', command=clear).pack(side='left', padx=(5, 0))

output = scrolledtext.ScrolledText(window, state='disabled')
output.pack(padx=10, pady=(0, 10), fill='both', expand=True)

entry.focus()
window.mainloop()
